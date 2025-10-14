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

load_config()
run_command("parted -s /dev/sda mklabel gpt")


#def disk_parted():
#    commands = [
#        f"parted -s /dev/sda mklabel gpt",
#        f"parted -s ",
#    ]







duration = time.time() - start_time
print(f"{duration:.2f}")

