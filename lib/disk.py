import sys

from lib.utils import run_command

def create_partitions(config):
    disk = config['disk']
    if disk['create_gpt']:
        run_command(f"sgdisk -Z {disk['device']}")
        run_command(f"sgdisk -o {disk['device']}")
    for partition in disk['partitions']:
        if partition['create_partition']:
            part_name = partition['name']
            part_number = partition['part'][-1]
            part_size = partition['size']
            if part_name == "efi":
                part_flag = "ef00"
            elif part_name == "root":
                part_flag = "8304"
            elif part_name == "home":
                part_flag = "8302"
            else:
                print("Раздел не поддерживается! Завершение работы скрипта")
                sys.exit(1)
            part_filesystem = partition['filesystem']
            
            run_command(f"sgdisk {disk['device']} -n {part_number}:0:{part_size} -t {part_number}:{part_flag} -c {part_number}:{part_name}")

def format_partitions(config):
    disk = config['disk']
    for partition in disk['partitions']:
        if partition['create_partition']:
            part_device = partition['part']
            part_filesystem = partition['filesystem']
            if part_filesystem == 'fat32':
                run_command(f"mkfs.fat -F32 {part_device}")
            elif part_filesystem == 'ext4':
                run_command(f"mkfs.ext4 -F {part_device}")
            else:
                print("Файловая система не найдена!")

