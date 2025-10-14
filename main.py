import yaml

import os
import sys
import subprocess

import time

start_time = time.time()

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


config = load_config()

def create_partitions(config):
    disk = config['disk']
    run_command(f"parted -s {disk['device']} mklabel gpt")
    for i, part in enumerate(disk['partitions'], 1):
        label = part['label']
        start = part['start']
        end = part['end']
        filesystem = part['filesystem']
        run_command(f"parted -s {disk['device']} mkpart {label} {filesystem} {start} {end}")
        if part.get('efi', False):
            run_command(f"parted -s {disk['device']} set {i} esp on")

 
#def disk_parted():
#    commands = [
#        f"parted -s /dev/sda mklabel gpt",
#        f"parted -s ",
#    ]


create_partitions(config)




duration = time.time() - start_time
print(f"{duration:.2f}")

