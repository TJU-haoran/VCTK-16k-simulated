- # MIMO-DoAnet: Multi-channel Input and Multiple Outputs DoA Network with Unknown Number of Sound Sources

## Citation
Please cite the following papers if you use our dataset:
1. Yin, H., Ge, M., Fu, Y., Zhang, G., Wang, L., Zhang, L., Qiu, L., Dang, J. (2022) MIMO-DoAnet: Multi-channel Input and Multiple Outputs DoA Network with Unknown Number of Sound Sources. Proc. Interspeech 2022, 891-895, doi: 10.21437/Interspeech.2022-10493
```bibtex
@inproceedings{yin22b_interspeech,
  author={Haoran Yin and Meng Ge and Yanjie Fu and Gaoyan Zhang and Longbiao Wang and Lei Zhang and Lin Qiu and Jianwu Dang},
  title={{MIMO-DoAnet: Multi-channel Input and Multiple Outputs DoA Network with Unknown Number of Sound Sources}},
  year=2022,
  booktitle={Proc. Interspeech 2022},
  pages={891--895},
  doi={10.21437/Interspeech.2022-10493}
}
```

## Usage

### 1. Download our simulated dataset 

- VCTK_16k_simulated_data.zip (8.11G)
  - Download link1: https://drive.google.com/file/d/1x9xDPsoAMxB8JohBltgirUCRqbBxLorF/view?usp=sharing
  - Download link2：https://pan.baidu.com/s/1Pg3BqeQbFMgCTlBIAjZHHw  Extraction code：2023 (Due to file size limitation, we divided train_50_rooms_4s into 3 compressed packages train_50_rooms_4s_group1.zip, train_50_rooms_4s_group2.zip, and train_50_rooms_4s_group3.zip. After downloading, please put the files in the compressed package in the train_50_rooms_4s folder)
- The content in the VCTK_16k_simulated_data.zip

|  simulated_room   |                         description                          | simulated_json |                         description                          |
| :---------------: | :----------------------------------------------------------: | :------------: | :----------------------------------------------------------: |
| train_50_rooms_4s | 6-channel single source speech data for training, including 89 angles each room |     train      | 50rooms_4w_json_4s_2speaker<br>50rooms_4w_json_4s_3speaker<br>50rooms_4w_json_4s_4speaker |
| valid_50_rooms_4s | 6-channel single source speech data for validation, including 9 angles each room |     valid      | 50rooms_1k_json_4s_2speaker<br/>50rooms_1k_json_4s_3speaker<br/>50rooms_1k_json_4s_4speaker |
| test_50_rooms_4s  | 6-channel single source speech data for testing, including 9 angles each room |      test      | 50rooms_1k_json_4s_2speaker<br/>50rooms_1k_json_4s_3speaker<br/>50rooms_1k_json_4s_4speaker |

Due to there are too many speeches in our training set, so we don't mix the multiple speeches of multiple sources beforehand. We save the wave path, angle, SIR, and vad_label in JSON and mix these speeches in our dataloader.

### 2. Replace the old wave path with your path

- We save the absolute wave path in JSON, so you can replace the old wave path with your path using our `replace_path.py`.

### 3. Train your model with our dataloader

- You can train your model using our `dataloader.py`.



## Simulation process

- VCTK corpus (version 0.92) includes 44455 48k Hz 2-channel speech data uttered by 110 English speakers, the length of data is between 2 seconds and 17 second, mainly in 3 seconds to 4 seconds, so we choose all the first channel of 4-second length speech data as original single channel speech, 15450 in total. Moreover, we downsample the sampling rate to 16k Hz.

<div align=center>
<img src="https://github.com/TJU-haoran/VCTK-16k-simulated/blob/main/Table1.png" width="500"/>
</div>

- We simulate 6-channel speech data from original single channel data through pyroomacoustics, the spacing of 6 microphones is 0.04 m, 0.04 m, 0.12 m, 0.04 m, 0.04 m. The parameters of simulated rooms are shown in Tabel 1, the length of room is a random number between 4 m and 15 m, the width of room is a random number between 3 m and length of room, the height of room is a random number between 3 m and 3.5 m. There are small, middle, large 3 types of room according to the length of the room, the RT60 is a random number between 0.2 and 0.3, 0.3 and 0.6, 0.4 and 0.7 respectively.

<div align=center>
<img src="https://github.com/TJU-haoran/VCTK-16k-simulated/blob/main/Figure1.png" width="500"/>
</div>

- As shown in Figure 1, the microphone array is located in the middle of the wall, at a distance of 0.5 m from the wall and 2 m from the ground. In order to make sound sources cover the area in rooms better, we first set the angle of the sound source, then we leave 0.5 m between the sound source and the microphone array and between the sound source and the wall, divide the rest range into near, medium and far range, the distance between microphone array and sound source is a random number in 3 types of range, so we simulate one original single channel speech data at near, medium, far distance simultaneously.
- We divide the 110 speakers into 90, 10 and 10 as the training speakers, validation speakers, testing speakers. We simulated 50 training rooms, validation rooms and testing rooms respectively. In training rooms, we divide 1° to 179° into 79 parts at 2° intervals and set one sound source in each part. In validation and testing rooms, divide 1° to 179° into 9 parts at 20° intervals, so there are 9 sources in each room. The reason we demarcate the angle spacing is to make the speakers different for each angle in the room, so that multiple speakers can be arbitrarily combined later.
- Then we generate 3 sets of training, validation set, and testing set from simulated rooms for 2, 3, and 4 sources respectively. We randomly select the angles and the near, medium, and far distance of sound sources, and keep the sound sources are at least 5° apart from each other. The training set contains 40,000 utterances (44.44 hours, 90 speakers), the validation set and the testing set contain 1,000 utterances (1.11 hours, 10 speakers) separately.

## Environments

- Python 3.8.8
- Pytorch 1.8.0

## Contact information

- Since this work was done during my internship at Huawei, I cannot open source the code due to confidentiality requirement, but please contact me if you have any questions about the experimental details.
- Email: fuyanjie@tju.edu.cn, haoran_yin@tju.edu.cn
