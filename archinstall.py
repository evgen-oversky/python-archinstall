from lib.utils import *
from lib.disk import *
from lib.base_install import *

import time

if __name__ == "__main__":
    start_time = time.time()

    config = load_config()

    create_partitions(config)
    format_partitions(config)
    create_subvolumes(config)
    mount_subvolumes(config)
    mount_partitions(config)
    install_base_system(config)
    gen_fstab()
    set_time(config)

    duration = time.time() - start_time
    print(f"{duration:.2f}")

