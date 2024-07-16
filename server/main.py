import argparse
import logging

import config

from server import start_server
from utils import print_startup_message

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', type=str, required=False)
    args = parser.parse_args()
    if args.directory:
        config.DIRECTORY = args.directory

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s - %(levelname)s] %(message)s')
    print_startup_message()
    parse_arguments()
    start_server()