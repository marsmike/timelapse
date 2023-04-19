import os
import cv2
import numpy as np
from PIL import Image
from tqdm import tqdm
import multiprocessing as mp

# Class for creating time-lapse videos from a directory of images
class Timelapse:
    def __init__(self, config):
        self.config = config

    def process_image(self, filename):
        # Load image and resize to 1920x1080
        im = Image.open(os.path.join(self.config.input_dir, filename))
        im = im.resize((1920, 1080))

        # Check if current frame should be slowed down
        if str(filename) in self.config.slow.split(','):
            frames = int(self.config.duration * self.config.fps)
        else:
            frames = int(self.config.duration * self.config.fps)

        # Create output frames
        frames_list = []
        for j in range(frames):
            frames_list.append(cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR))

        # Return frames for this image
        return frames_list

    def process_output_frames(self, frames_list):
    
        # Create output video file
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(self.config.output_file, fourcc, self.config.fps, (1920, 1080))

        # Write frames to output video file
        for frames in frames_list:
            for frame in frames:
                out.write(frame)
            out.release()

        # Release output video file
        out.release()

    def run(self):
        # Get list of input image files
        file_list = self.config.get_input_files()
        # Calculate number of cores to use
        cores = mp.cpu_count()
        # Divide input files into equal batches for each core
        file_batches = np.array_split(file_list, cores)
        # Create a pool of processes and map each process to a file batch
        pool = mp.Pool(processes=cores)
        results = []
        for batch in file_batches:
            results.append(pool.apply_async(self.process_image, args=(batch,)))
        # Get output frames from each process
        output_frames = []
        for res in tqdm(results, desc='Processing images', total=len(results)):
            output_frames.extend(res.get())
        # Close pool of processes
        pool.close()
        # Sort output frames by order of input files
        output_frames.sort(key=lambda x: int(os.path.splitext(x[0])[0]))
        # Split output frames into equal batches for each core
        frame_batches = np.array_split(output_frames, cores)
        # Create a pool of processes and map each process to a frame batch
        pool = mp.Pool(processes=cores)
        results = []
        for batch in frame_batches:
            results.append(pool.apply_async(self.process_output_frames, args=(batch,)))
        # Wait for all processes to finish
        for res in tqdm(results, desc='Writing video'):
            res.get()
        # Close pool of processes
        pool.close()
        # Output completion message
        print('\nTime-lapse video created successfully! Output file: {}'.format(self.config.output_file))