from lib.utils import run_command

def install_base_system(config):
    pkgs = " ".join(config['system']['pkgs'])
    run_command(f"pacstrap -K /mnt {pkgs}")

def gen_fstab():
    run_command("genfstab -U /mnt >> /mnt/etc/fstab")  

def network_setting(config):

    run_command("systemctl enable systemd-networkd.service")
    run_command("systemctl start systemd-networkd.service")
    

# Сеть

# Новый пользователь

# Права sudo

# Загрузчик

# Клонирование репозитория

def set_root_password(config):
    root_password = config['system']['root_password']
    run_command(f"echo 'root:{root_password}' | chpasswd", chroot=True)


# Перезагрузка