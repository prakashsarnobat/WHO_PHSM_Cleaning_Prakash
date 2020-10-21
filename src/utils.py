import os
import shutil

def create_dir(dir: str):
    """Function to create or replace a "tmp" directory"""

    if os.path.exists(dir):

        shutil.rmtree(dir)

    os.mkdir(dir)
