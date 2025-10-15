from lib.utils import run_command

def create_partitions(config):
    disk = config['disk']
    if disk['create_gpt']:
        run_command(f"parted -s {disk['device']} mklabel gpt")
    for partition in disk['partitions']:
        if partition['create_partition']:
            part_name = partition['name']
            part_number = int(partition['part'][-1])
            part_start = partition['start']
            part_end = partition['end']
            part_filesystem = partition['filesystem']
            run_command(f"parted -s {disk['device']} mkpart {part_name} {part_filesystem} {part_start} {part_end}")
            if part_name == "esp":
                run_command(f"parted -s {disk['device']} set {part_number} esp on")

def format_partitions(config):
    disk = config['disk']
    for part in disk['partitions']:
        part_device = part['part']
        filesystem = part['filesystem']
        if filesystem == 'fat32':
            run_command(f"mkfs.fat -F32 {part_device}")
        elif filesystem == 'ext4':
            run_command(f"mkfs.ext4 -F {part_device}")
        else:
            print("Файловая система не найдена!")