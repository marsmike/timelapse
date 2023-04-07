import os
import cv2
from PIL import Image
import argparse

# Define command-line arguments
parser = argparse.ArgumentParser(description='Create a time-lapse video from a directory of JPG images.')
parser.add_argument('input_dir', type=str, help='The directory containing the JPG images.')
parser.add_argument('output_file', type=str, help='The path and filename for the output video file.')
parser.add_argument('-fps', type=int, default=24, help='The frame rate of the output video.')
parser.add_argument('-start', type=int, default=0, help='The starting index of the input JPG images.')
parser.add_argument('-end', type=int, default=None, help='The ending index of the input JPG images.')
parser.add_argument('-duration', type=float, default=1, help='The duration of each frame in seconds.')
parser.add_argument('-slow', type=str, default='', help='The indices of the frames to slow down. Example: "1,3,5"')
args = parser.parse_args()

# Get list of input image files
file_list = os.listdir(args.input_dir)
file_list.sort()
file_list = file_list[args.start:args.end]

# Create output video file
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(args.output_file, fourcc, args.fps, (1920, 1080))

# Iterate through input images and add to video
for i, filename in enumerate(file_list):
    # Load image and resize
    im = Image.open(os.path.join(args.input_dir, filename))
    im = im.resize((1920, 1080))

    # Check if current frame should be slowed down
    if str(i) in args.slow.split(','):
        for j in range(int(args.duration*args.fps)):
            out.write(cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR))
    else:
        for j in range(int(args.duration*args.fps)):
            out.write(cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR))

# Release output video file
out.release()
