import sys 
import time

from lib.utils import *

def disk_preparation(config):
    disk = config['disk']
    if disk['new_partition_table'] == True:
        run_command(f"sgdisk -Z {disk['device']}")
        run_command(f"sgdisk -o {disk['device']}")     
    for partition in disk['partitions']:
        if partition['create_partition'] == True:
            part_label = partition['label']
            part_dev = partition['dev']
            part_number = partition['dev'][-1]
            part_flag = partition['flag']
            part_size = partition['size']
            part_fs = partition['fs']
            run_command(f"sgdisk {disk['device']} -n {purt_number}:0:{part_size} -t {part_number}:{part_flag} -c {part_number}:{part_label}")
            if part_fs == "fat32":
                run_command(f"mkfs.fat -F32 {part_dev}")
            elif part_fs == "btrfs":
                # Форматирование раздела в btrfs
                run_command(f"mkfs.btrfs -f {part_dev}")
                
                # Создание btrfs подтомов
                run_command(f"mount {part_dev} /mnt")
                for subvolume in partition['subvolumes']:
                    vol_name = subvolume['name']
                    run_command(f"btrfs subvolume create /mnt/{vol_name}")
                run_command("umount /mnt")


                # Необходимо вынести монтирование бтрфс поскольку если создание раздела отключено btrfs тома не смонтируются
                # А нужно чтобы монтирование было несмотря на отключенный флаг созданиие раздела


                # Монтирование btrfs подтомов. Первым монтируется подтом / а то жопа
                for subvolume in partition['subvolumes']:
                    vol_name = subvolume['name']
                    vol_mount_point = "/mnt" + subvolume['mount_point']
                    vol_mount_args = "subvol=" + subvol_name + "," + disk['mount_args']
                    run_command(f"mkdir -p {mount_point}")
                    run_command(f"mount -o {mount_args} {part_dev} {mount_point}")
      
      # Монтирование остальных разделов ибо первым должен быть смонтирован корень
      for partition in disk['partitions']:
        if partition['part_label'] == 'btrfs':
            continue
        else:
            part_dev = partition['part_dev']
            part_mount_point = "/mnt" + partition['mount_point']
            run_command(f"mkdir -p {part_mount_point}")
            run_command(f"mount {part_dev} {part_mount_point}")





def install_base_pkgs(config):
    pkgs = " ".join(config['system']['pkgs'])
    run_command(f"pacstrap -K /mnt {pkgs}")

def gen_fstab():
    run_command("genfstab -U /mnt >> /mnt/etc/fstab")

def set_geolocation(config):
    
    time_zone = config['system']['time_zone']
    locales = "\n".join(config['system']['locales']) + "\n"
    language = "LANG=" + config['system']['language']
    
    # set timezone
    run_command(f"ln -sf /usr/share/zoneinfo/{time_zone} /etc/localtime", chroot=True)
    
    run_command("hwclock --systohc", chroot=True)
    
    with open("/mnt/etc/locale.gen", "a") as f:
        f.write(f"{locales}")
    with open("/mnt/etc/locale.conf", "w") as f:
        f.write(f"{language}")
    run_command("locale-gen", chroot=True)

def set_network():
    run_command("cp files/systemd-networkd/20-wired.network /mnt/etc/systemd/network")
    run_command("cp files/systemd-networkd/25-wireless.network /mnt/etc/systemd/network")
    run_command("cp files/iwd/main.conf /mnt/etc/iwd")
    run_command("cp files/hostname /mnt/etc")
    run_command("cp files/hosts /mnt/etc")
    run_command("systemctl enable systemd-networkd.service", chroot=True)
    run_command("systemctl start systemd-networkd.service", chroot=True)
    run_command("systemctl enable systemd-resolved.service", chroot=True)
    run_command("systemctl start systemd-resolved.service", chroot=True)
    run_command("systemctl enable iwd.service", chroot=True)
    run_command("systemctl start iwd.service", chroot=True)
    run_command("ln -sf /mnt/run/systemd/resolve/stub-resolv.conf /mnt/etc/resolv.conf")

def set_root_password(config):
    root_password = config['system']['root_password']
    run_command(f"echo 'root:{root_password}' | chpasswd", chroot=True)

def create_user(config):
    user_name = config['user']['user_name']
    user_groups = ",".join(config['user']['user_groups'])
    user_password = config['user']['user_password']
    user_shell = config['user']['user_shell']
    run_command(f"useradd -m -G {user_groups} -s {user_shell} {user_name}", chroot=True)
    run_command(f"echo '{user_name}:{user_password}' | chpasswd", chroot=True)
    run_command(r"sed -i 's/^#\s*\(%wheel\s*ALL=(ALL:ALL)\s*ALL\)/\1/' /mnt/etc/sudoers")

def install_boot_loader(config):
    for partition in config['disk']['partitions']:
        if partition['part_label'] == 'efi':
            esp_mount_point = partition['mount_point']
            break
    run_command("bootctl install", chroot=True)
    run_command(f"cp files/systemd-boot/loader.conf /mnt{esp_mount_point}/loader")
    run_command(f"cp files/systemd-boot/arch.conf /mnt{esp_mount_point}/loader/entries")


if __name__ == "__main__":
    start_time = time.time()

    config = load_config()

    disk_preparation(config)
#    install_base_pkgs(config)
#    gen_fstab()
#    set_geolocation(config)
#    set_network()
#    set_root_password(config)
#    create_user(config)
#    install_boot_loader(config)
    
    duration = time.time() - start_time
    print(f"{duration:.2f}")
