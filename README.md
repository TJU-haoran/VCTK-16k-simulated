# VCTK-16k-simulated

### Usage

##### 1. Download our simulated dataset 

- VCTK_16k_simulated_data.zip (8.47G)
  - Download link: https://drive.google.com/drive/folders/1DtT1C01q6jALRmMBa02qaKKLP50PQoQV?usp=sharing
- The content in the VCTK_16k_simulated_data.zip

|  simulated_room   |                         description                          | simulated_json |                       description                        |
| :---------------: | :----------------------------------------------------------: | :------------: | :------------------------------------------------------: |
| train_50_rooms_4s | 6-channel single source speech data for training, including 79 angles each room |     train      |  including 2, 3, and 4 sources training data using JSON  |
| valid_50_rooms_4s | 6-channel single source speech data for validation, including 9 angles each room |     valid      | including 2, 3, and 4 sources validation data using JSON |
| test_50_rooms_4s  | 6-channel single source speech data for testing, including 9 angles each room |      test      |  including 2, 3, and 4 sources testing data using JSON   |

Due to there are too much speech in our training set, so we don't mix the multiple speech of multiple sources beforeahand. We save the wave path, angle, SIR, and vad_label in JSON and mix these speech in our dataloader.

##### 2. Replace the old wave path by your path

- We save the absolute wave path in json, so you can replace the old wave path by your path using our replace_path.py

##### 3. Train your model with our dataloader

- You can train your model using our dataloader.py



### Simulation process

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

### Environments

- Python 3.8.8
- Pytorch 1.8.0

### Contact us

- Since this work was done during my internship at Huawei, I cannot open source the code due to confidentiality requirements, but please contact me if you have any questions about the experimental details.
- Email: haoran_yin@tju.edu.cn
