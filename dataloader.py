import os
import json
import librosa
import numpy as np
import multiprocessing as mp
import soundfile as sf
import torch
import torch.utils.data as tud
from torch.utils.data import Dataset


def audioread(path, fs = 16000):
    wave_data, sr = sf.read(path)
    if sr != fs:
        wave_data = librosa.resample(wave_data,sr,fs)
    return wave_data

def activelev(data):
    eps = np.finfo(np.float32).eps
    max_val = (1. + eps) / (np.std(data)+eps)
    data = data * max_val
    return data

def parse_scp(scp, path_list):
    with open(scp, encoding='utf-8-sig') as fid:
        for line in fid:
            path_list.append(line.strip())

# convert multiple input angles into output SPS separately
def convert_SPS(input_angle_list, output_angle_dimention):
    SPS = []
    for angle in range(output_angle_dimention):
        SPS_angle = 0
        for input_angle in input_angle_list:
            SPS_angle += np.exp(-1 * np.square(angle - input_angle)/8 **2)
        SPS.append(SPS_angle)
    return SPS

class TFDataset(Dataset):
    def __init__(self, wav_scp, n_mics = 6, sample_rate= 16000):
        mgr = mp.Manager()
        self.file_list = mgr.list()
        self.noise_list = mgr.list()
        self.index = mgr.list()
        self.sr = sample_rate
        self.n_mics = n_mics
        self.SPS_dimension = 210
        self.time_bins = 250
        self.speaker_num = 3
        pc_list = []
        p = mp.Process(target = parse_scp, args=(wav_scp,self.file_list))
        p.start()
        pc_list.append(p)
        for p in pc_list:
            p.join()
        self.index = [idx for idx in range(len(self.file_list))]

    def __len__(self):
        return len(self.index)
    
    def __getitem__(self, idx):
        item = self.index[idx]
        file_index = item
        file_path = self.file_list[file_index]

        # load json into metadata
        with open(file_path + os.sep + 'sample_log.json') as json_file:
            metadata = json.load(json_file)
        all_sources, doa_sps_array = self.get_mixture_ang_gt(metadata)
        all_sources = torch.stack(all_sources,dim=0)
        mixed_data = torch.sum(all_sources,dim=0)
        channel_num, _ = mixed_data.size()
        
        # scale the maximum value of mixture waveform to 0.5
        scale = 0.5
        for channel_idx in range(channel_num):
            mix_single_channel_wav = mixed_data[channel_idx,:]
            max_amp = torch.max(torch.abs(mix_single_channel_wav))
            if max_amp == 0:
                max_amp =1
            mix_scale = 1/max_amp*scale
            mixed_data[channel_idx,:] = mixed_data[channel_idx,:] * mix_scale

        return mixed_data, doa_sps_array
    
    def get_mixture_ang_gt(self, metadata):
        all_sources = []
        source_index = 0
        sps_dict = dict([])
        doa_angle_array = np.zeros([self.time_bins, self.speaker_num]) # 250 × 3, time_bins × speaker_num
        doa_sps_array = np.zeros([self.time_bins, self.speaker_num, self.SPS_dimension]) # 250 × 3 × 210, time_bins × speaker_num × dimension of SPS
        
        # load and mix the single source speech data
        for key in metadata.keys():
            if "source" in key:
                channel_index_list = np.arange(self.n_mics)
                flag = metadata[key]['wave_path']
                gt_audio_files = [flag + '_'+ str(channel_index) + '.wav' for channel_index in channel_index_list]
                gt_waveforms = []

                # load the multi-channel spech
                for _, gt_audio_file in enumerate(gt_audio_files):
                    gt_waveform = audioread(gt_audio_file)
                    single_channel_wav = activelev(gt_waveform)
                    gt_waveforms.append(torch.from_numpy(single_channel_wav))
                shifted_gt = np.stack(gt_waveforms)
                perturbed_source = shifted_gt
                perturbed_source = torch.from_numpy(perturbed_source)
                perturbed_source = perturbed_source.to(torch.float32)
                if source_index !=0:
                    # adjust the SIR between diffrent speakers
                    SIR = 0 # SIR = metadata[key]['SIR']
                    change_weight = 10 ** (SIR/20)
                    perturbed_source = perturbed_source * change_weight
                all_sources.append(perturbed_source)
                voice_angle = int(metadata[key]['angle'])

                # convert angle into SPS coding
                SPS = convert_SPS([voice_angle + 15], self.SPS_dimension)
                if not voice_angle in sps_dict:
                    sps_dict[voice_angle] = SPS
                vad_label = metadata[key]['vad_label']

                # -1 denote silent sound source in this frame
                for vad_index in range(len(vad_label)-1):
                    if vad_label[vad_index] == 1:
                        doa_angle_array[vad_index, source_index] = voice_angle
                    else:
                        doa_angle_array[vad_index, source_index] = -1
                source_index = source_index + 1
        
        # Angle sorting
        for time_idx in range(0, self.time_bins-1):
            angles = doa_angle_array[time_idx,:]
            sort_angles = np.sort(angles)
            doa_angle_array[time_idx,:] = sort_angles
        for source_idx in range(0, source_index):
            for time_idx in range(0,self.time_bins-1):
                if doa_angle_array[time_idx,source_idx] == -1:
                    doa_sps_array[time_idx,source_idx,:] = np.zeros(self.SPS_dimension)
                else:
                    sps = sps_dict[doa_angle_array[time_idx,source_idx]]
                    doa_sps_array[time_idx,source_idx,:] = sps
        return all_sources, doa_sps_array


class Sampler(tud.sampler.Sampler):
    def __init__(self, data_source, batch_size):
        it_end = len(data_source) - batch_size +1
        self.batches = [range(i,i+batch_size) for i in range(0, it_end, batch_size)]
        self.data_source = data_source
    
    def __iter__(self):
        return (i for b in self.batches for i in b)
    
    def __len__(self):
        return len(self.data_source)

def static_loader(clean_scp, batch_size = 8, num_workers = 15, sample_rate = 16000):
    '''
    clean_scp: a ".lst" including the absolute paths of all the training/validation/testing json
    batch_size: 8
    num_workers: 15
    sample_rate: 16000
    '''
    dataset = TFDataset(
        wav_scp= clean_scp,
        sample_rate = sample_rate
    )
    sampler = Sampler(dataset, batch_size)
    loader = tud.DataLoader(
        dataset,
        batch_size = batch_size,
        num_workers = num_workers,
        sampler = sampler,
        drop_last = False
    )
    return loader