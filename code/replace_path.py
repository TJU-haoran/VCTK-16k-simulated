import json
import os

def replace(room_path, json_path):
    jsons = os.listdir(json_path)
    total_num = len(jsons)
    finish_num = 0
    for json_temp in jsons:
        load_path = os.path.join(json_path,json_temp)
        with open(load_path + os.sep + 'sample_log.json') as json_file:
            old_metadata = json.load(json_file)
            for key in old_metadata.keys():
                if "source" in key:
                    wave_path = old_metadata[key]['wave_path']
                    back_part = wave_path.split("simulated_room")[1]
                    front_part = room_path.split("/simulated_room")[0]
                    new_wave_path = front_part + "/simulated_room" + back_part
                    old_metadata[key]['wave_path'] =  new_wave_path

        with open(load_path + os.sep + 'sample_log.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(old_metadata, ensure_ascii=False))
            finish_num +=1
        print('Finish: {}/{}'.format(finish_num,total_num))

if __name__ == '__main__':
    '''
    We concatenate the front part of your new room path and the back part of old wave path.
    old wave path = /Work21/2020/yinhaoran/simulated_room/test_50_rooms_4s/room_15_5.63_3.45_rt60_0.66/speech/30/p280_2.15m_far_multichannel
    back part = /test_50_rooms_4s/room_15_5.63_3.45_rt60_0.66/speech/30/p280_2.15m_far_multichannel
    your new room path = /Work22/2020/yinhaoran/simulated_room/
    front part = /Work22/2020/yinhaoran
    new wave path = front part + "/simulated_room" + back part
                  = /Work22/2020/yinhaoran/simulated_room/test_50_rooms_4s/room_15_5.63_3.45_rt60_0.66/speech/30/p280_2.15m_far_multichannel
    '''
    room_path = r'/Work22/2020/yinhaoran/simulated_room/' # absolute path of simulated_room data
    json_path = r'/Work21/2020/yinhaoran/simulated_json/test/50rooms_1k_json_4s_2speaker' # absolute path of 2 or 3 or 4 sources json
    replace(room_path, json_path)
