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

def create_subvolumes(config):
    disk = config['disk']
    for partition in disk['partitions']:
        if partition['part_label'] == 'btrfs':
            part_btrfs = partition['part_dev']
            break
    run_command(f"mount {part_btrfs} /mnt")
    for subvolume in disk['subvolumes']:
        vol_name = subvolume['vol_name']
        run_command(f"btrfs subvolume create /mnt/{vol_name}")
    run_command(f"umount /mnt")

def mount_subvolumes(config):
    disk = config['disk']
    main_mount_point = disk['main_mount_point']
    for partition in disk['partitions']:
        if partition['part_label'] == 'btrfs':
            for subvolume in disk['subvolumes']:
                subvol_name = subvolume['vol_name']
                subvol_mount_point = main_mount_point + subvolume['mount_point']
                subvol_mount_args = "subvol=" + subvol_name + "," + disk['subvol_mount_args']
                run_command(f"mkdir -p {subvol_mount_point}")
                run_command(f"mount -o {subvol_mount_args} {partition['part_dev']} {subvol_mount_point}")
        else:
            continue

def mount_partitions(config):
    disk = config['disk']
    main_mount_point = disk['main_mount_point']
    for partition in disk['partitions']:
        if partition['part_label'] == 'btrfs':
            continue
        else:
            part_dev = partition['part_dev']
            part_mount_point = main_mount_point + partition['mount_point']
            run_command(f'mkdir -p {part_mount_point}')
            run_command(f'mount {part_dev} {part_mount_point}')
