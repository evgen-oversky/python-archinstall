from lib.utils import run_command

def install_base_system(config):
    pkgs = " ".join(config['system']['pkgs'])
    run_command(f"pacstrap -K /mnt {pkgs}")

def gen_fstab():
    run_command("genfstab -U /mnt >> /mnt/etc/fstab")  

def set_time(config):
    time_zone = config['system']['time_zone']
    run_command(f"ln -sf /ust/share/zoneinfo/{time_zone} /etc/localtime", chroot=True)
    run_command("hwclock --systohc", chroot=True)

def set_root_password(config):
    root_password = config['system']['root_password']
    run_command(f"echo 'root:{root_password}' | chpasswd", chroot=True)

def create_user(config):
    pass

# Сеть

# Новый пользователь

# Права sudo

# Загрузчик

# Клонирование репозитория

# Перезагрузка