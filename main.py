import argparse
from config import Config
from timelapse import Timelapse

def main(param_file):
    # Read parameter file
    config = Config(param_file)

    # Create timelapse and run
    timelapse = Timelapse(config)
    timelapse.run()

# Run main function if this file is run as a script

if __name__ == '__main__':
    # Define command-line arguments
    parser = argparse.ArgumentParser(description='Create a time-lapse video from a directory of JPG images.')
    parser.add_argument('param_file', type=str, help='The parameter file containing input and output paths, durations, etc.')
    args = parser.parse_args()

    # Run program
    main(args.param_file)

