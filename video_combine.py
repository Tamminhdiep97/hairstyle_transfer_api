import os
from os.path import join as opj
import time

from natsort import natsorted
import cv2
from tqdm import tqdm
from loguru import logger


input_folder = opj(os.getcwd(), 'experiment_3', 'output') 
for folder_ in tqdm(os.listdir(input_folder)):
    # if "image" in  folder_:
    #     continue
    for ex_ in tqdm(os.listdir(opj(input_folder, folder_))):
        case_path = opj(input_folder, folder_, ex_)
        input_case = opj(case_path, 'interp')

        os.makedirs(opj(case_path, 'video'), exist_ok=True)

        capture = cv2.imread(opj(input_case, os.listdir(input_case)[0]))
        frame_width = int(capture.shape[1])
        frame_height = int(capture.shape[0])
        video = cv2.VideoWriter(
                opj(case_path, 'video', 'captured_video.mp4'),
                cv2.VideoWriter_fourcc(*'mp4v'),
                60, (frame_width, frame_height)
            )
        # file_list = os.listdir(input_case)
        # print(natsorted(file_list))
        # print(sorted(os.listdir(input_case)))
        logger.info('processing folder: {}'.format(opj(input_folder, folder_, ex_)))
        t1 = time.time()
        for file in natsorted(os.listdir((input_case))):
            # print(file)
            frame = cv2.imread(opj(input_case, file))
            video.write(frame)
        t2 = time.time()
        logger.info('proccess done: {} s'.format(round(t2-t1, 5)))
        video.release()
