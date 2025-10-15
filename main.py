import yaml

import os
import sys
import subprocess

import time

def load_config(config_file="config.yml"):
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        print("Файл конфигурации не найден")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Ошибка парсинга YAML: {e}")
        sys.exit(1)

def run_command(cmd):
    cmd = cmd.split()
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return result
    except subprocess.CalledProcessError as e:
        print(f"{e}")
        print(f"{e.stderr}")
        sys.exit(1)

def check_internet():
    pass

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




if __name__ == "__main__":
    start_time = time.time()

    config = load_config()


    create_partitions(config)
    #format_partitions(config)

    duration = time.time() - start_time
    print(f"{duration:.2f}")

