from lib.utils import run_command

def install_base_system(config):
    pkgs = " ".join(config['system']['pkgs'])
    run_command(f"pacstrap -K /mnt {pkgs}")

def gen_fstab():
    run_command("genfstab -U /mnt >> /mnt/etc/fstab")    

# Сеть

# Пароль root

# Новый пользователь

# Загрузчик

# Клонирование репозитория

# Перезагрузка