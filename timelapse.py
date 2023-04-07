import os
import cv2
import numpy as np
from PIL import Image
import configparser
import argparse

# Define command-line arguments
parser = argparse.ArgumentParser(description='Create a time-lapse video from a directory of JPG images.')
parser.add_argument('param_file', type=str, help='The parameter file containing input and output paths, durations, etc.')
args = parser.parse_args()

# Read parameter file
config = configparser.ConfigParser()
config.read(args.param_file)

input_dir = config.get('input', 'input_dir')
output_file = config.get('output', 'output_file')
fps = config.getint('output', 'fps')
start = config.getint('input', 'start', fallback=0)
end = config.getint('input', 'end', fallback=None)
duration = config.getfloat('output', 'duration', fallback=1)
slow = config.get('output', 'slow', fallback='')

# Get list of input image files
file_list = os.listdir(input_dir)
file_list.sort()
file_list = file_list[start:end]

# Create output video file
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_file, fourcc, fps, (1920, 1080))

# Iterate through input images and add to video
for i, filename in enumerate(file_list):
    # Load image and resize
    im = Image.open(os.path.join(input_dir, filename))
    im = im.resize((1920, 1080))

    # Check if current frame should be slowed down
    if str(i) in slow.split(','):
        for j in range(int(duration*fps)):
            out.write(cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR))
    else:
        for j in range(int(duration*fps)):
            out.write(cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR))

# Release output video file
out.release()

