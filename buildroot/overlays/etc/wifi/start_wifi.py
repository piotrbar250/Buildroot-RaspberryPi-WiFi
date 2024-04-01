#start_wifi.py
import subprocess
import time

def check_brcmfmac_loaded():
    # Check if brcmfmac module is loaded
    module_loaded = subprocess.run(['lsmod'], capture_output=True, text=True)
    if 'brcmfmac' in module_loaded.stdout:
        print('brcmfmac module is loaded')
    else:
        print('brcmfmac module is not loaded')
        return False

    # Check dmesg for firmware load messages
    dmesg_output = subprocess.run(['dmesg'], capture_output=True, text=True)
    if 'brcmfmac: brcmf_fw_alloc_request' in dmesg_output.stdout and 'Firmware' in dmesg_output.stdout:
        print('brcmfmac firmware has been loaded')
    else:
        print('brcmfmac firmware loading issue detected')
        return False

    # Check if the wireless interface is present
    ip_link = subprocess.run(['ip', 'link'], capture_output=True, text=True)
    if 'wlan0: ' in ip_link.stdout:
        print('Wireless interface is present')
    else:
        print('Wireless interface is not present')
        return False

    return True

# Load brcmfmac module
subprocess.run('modprobe brcmfmac', shell=True)

# The main loop that checks for the brcmfmac configuration
max_iteration = 3
iteration = 0
while iteration < max_iteration:
    if check_brcmfmac_loaded():
        print('brcmfmac was fully loaded and configured')
        break
    else:
        print('There was a problem loading or configuring brcmfmac')
    print('Trying again in 1 second...')
    time.sleep(1)
    iteration += 1

# Once brcmfmac is loaded and configured, start the Wi-Fi connection
subprocess.run('wpa_supplicant -B -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf', shell=True)
subprocess.run('udhcpc -i wlan0', shell=True)

print("Finished configuring Wi-Fi")
