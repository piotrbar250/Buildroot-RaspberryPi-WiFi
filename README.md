# Buildroot Setup for Raspberry Pi with WiFi

This guide provides instructions for setting up Buildroot for the Raspberry Pi with WiFi support. Buildroot is a simple, efficient, and customizable tool for generating embedded Linux systems through cross-compilation.

## Prerequisites

Ensure you have `git`, `ccache`, and `wget` installed on your system. Additionally, you should have a Raspberry Pi with an SD card reader.

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