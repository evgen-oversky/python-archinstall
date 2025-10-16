import sys

from lib.utils import run_command

def create_partitions(config):
    disk = config['disk']
    if disk['new_table']:
        run_command(f"sgdisk -Z {disk['device']}")
        run_command(f"sgdisk -o {disk['device']}")
    for partition in disk['partitions']:
        if partition['create_partition']:
            part_label = partition['part_label']
            part_number = partition['part_dev'][-1]
            part_flag = partition['part_flag']
            part_size = partition['part_size']
            part_fs = partition['part_fs']
            run_command(f"sgdisk {disk['device']} -n {part_number}:0:{part_size} -t {part_number}:{part_flag} -c {part_number}:{part_label}")

def format_partitions(config):
    disk = config['disk']
    for partition in disk['partitions']:
        if partition['create_partition']:
            part_dev = partition['part_dev']
            part_fs = partition['part_fs']
            if part_fs == 'fat32':
                run_command(f"mkfs.fat -F32 {part_dev}")
            elif part_fs == 'btrfs':
                run_command(f"mkfs.btrfs -f {part_dev}")



