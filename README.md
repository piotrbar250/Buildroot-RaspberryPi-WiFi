# Buildroot Setup for Raspberry Pi with WiFi

This guide provides instructions for setting up Buildroot for the Raspberry Pi with WiFi support. Buildroot is a simple, efficient, and customizable tool for generating embedded Linux systems through cross-compilation.

## Setup Instructions

1. **Clone the Repository**

   First, clone the Buildroot-RaspberryPi-WiFi repository to your local machine.

   ```bash
   git clone https://github.com/piotrbar250/Buildroot-RaspberryPi-WiFi.git
   cd Buildroot-RaspberryPi-WiFi
   ./scripts/prepare_directory.sh
   cd buildroot
   ```

2. **Configure Buildroot**

   Before building, you need to configure Buildroot.

   - Run `make menuconfig`.
   - Provide the absolute path for the compiler cache directory (`ccache-br`).

3. **Build the System**

   Compile Buildroot by simply running:

   ```bash
   make
   ```

   This process might take some time as it compiles the entire Linux system for your Raspberry Pi.

4. **Prepare the SD Card Image**

   After the build process completes, locate the `sdcard.img` file in `buildroot/output/images`. This image file can be flashed onto your SD card.

   Example:

   ```bash
   sudo dd if='output/images/sdcard.img' of='/dev/mmcblk0' bs=4M status=progress
   ```

   Replace `/dev/mmcblk0` with the correct device for your SD card.

## Updating the Raspberry Pi remotely

If you have a Raspberry Pi already running and want to update the system image remotely, follow these steps:

1. **Run a HTTP Server**

   On your workstation, navigate to the directory containing the new system image and start a simple HTTP server.

   ```bash
   cd path/to/image
   python3 -m http.server
   ```

2. **Update the System Image on Raspberry Pi**

   On your Raspberry Pi, mount the boot partition, download the new image, and reboot.

   ```bash
   mount /dev/mmcblk0p1 /mnt
   cd /mnt
   rm Image && wget http://192.168.0.xxx:8000/Image
   reboot
   ```

   Replace `192.168.0.xxx` with your workstation's IP address.

## Manual configuration

To configure Buildroot for your Raspberry Pi with WiFi on your own:

- Run `make menuconfig` to start the configuration menu.
- Set the toolchain type to **External toolchain**.
- Select **Arm AArch64 12.2.rel1** for the toolchain.
- Enable **Compiler cache** and provide the absolute path for the compiler cache directory (`ccache-br`).
- Choose **ext2/3/4 root filesystem** with the exact size set to **1500M**.
- Ensure the initial RAM filesystem is linked into the Linux kernel and select **gzip compression** for the cpio filesystem.
- Set the root password to `qwerty`.
- You can also configure the system banner under this menu.

### Target Packages

Include the following packages for a comprehensive environment:

- Python3, Nano, Dropbear, Gesftpserver, NTP, Wpa_supplicant (with nl80211), Brcmfmac-sdio-firmware-rpi, Brcmfmac-sdio-firmware-rpi-wifi, and CA-certificates.

## Additional Configuration Details

- **File System Size**: Set in `board/raspberrypi4-64/genimage.cfg.in` to **256M** for optimal performance.
- **BusyBox and Init.d**: The system uses BusyBox with `/etc/init.d`. Includes custom daemons like `S60mnt` for mounting the boot partition and SSH setup, and `S99wifi` for WiFi configuration.
- **WiFi Setup**: Modify `buildroot/overlays/etc/wpa_supplicant/wpa_supplicant.conf.template` with your WiFi credentials and remove the `.template` extension for the WiFi to function correctly.
- **/etc/wifi/start_wifi.py**: It loads brcmfmac driver, starts wpa_supplicant for the wireless interface wlan0 and tries to obtain an IP address and other network configuration details from a DHCP server.


With these instructions, you can successfully set up Buildroot for your Raspberry Pi with WiFi support, creating a lightweight, customizable Linux environment for your embedded projects.