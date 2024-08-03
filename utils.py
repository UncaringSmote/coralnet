import logging
import os

from logdecorator import log_on_end


fileDir = os.path.dirname(os.path.realpath('__file__'))

def make_output_directory(state_id):
    output_dir = os.path.join(fileDir, f"output\\{state_id}")
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

@log_on_end(logging.INFO, "Save Location Generated: {result:s}")
def generate_save_location(state_id,filename):
    return os.path.join(fileDir, f"output\\{state_id}\\{filename}")

