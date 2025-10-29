from lib.utils import load_config
from lib.disk import *

import time

def check_internet():
    pass


if __name__ == "__main__":
    start_time = time.time()

    config = load_config()

    create_partitions(config)
    format_partitions(config)
    create_subvolumes(config)
    mount_subvolumes(config)
    mount_partitions(config)

    duration = time.time() - start_time
    print(f"{duration:.2f}")

