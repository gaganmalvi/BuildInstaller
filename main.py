'''
Copyright (C) 2021 Gagan Malvi

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
import urllib.request as r
import subprocess, pip, json, os, time

try:
    from tqdm import tqdm
except ModuleNotFoundError:
    pip.main(['install','tqdm'])

class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

# Definitions.
def getDeviceCodename():
    result = subprocess.run(['adb', 'shell', 'getprop', 'ro.product.vendor.device'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    return result.strip()

def rebootToBootloader():
    subprocess.run(['adb','reboot','bootloader'])

def fastbootImgFlash(part, img):
    subprocess.run(['fastboot','flash',part,img])

def checkForTeracube():
    if (getDeviceCodename() == "yk673v6_lwg62_64" or getDeviceCodename() == "2e"):
        print("Connected to Teracube 2e successfully.")
        return True
    else:
        print("Device not connected, or wrong device connected.")
        return False

def fastbootPkgFlash(name):
    subprocess.run(['fastboot','-w'])
    result = subprocess.run(['fastboot','update', name])
    print(result)

def downloadFile(url, output_path, silent = False):
    if silent:
        r.urlretrieve(url, filename=output_path)
    else:
        print('Beginning download...')
        with DownloadProgressBar(unit='B', unit_scale=True,
                                 miniters=1, desc=url.split('/')[-1]) as t:
            r.urlretrieve(url, filename=output_path, reporthook=t.update_to)

def downloadAndFlashLatestLineageRelease():
    downloadFile('https://raw.githubusercontent.com/2e-dev/releases/master/fastboot.json', 'lineage.json', silent = True)
    with open('lineage.json') as f:
        dl = json.load(f)
        l = dl['fbootpkg']
        print('Downloading fastboot package...')
        if os.path.isfile("lineage-18.1-fastboot.zip"):
            print("File downloaded already. Skipping new download...")
        else:
            downloadFile(l,"lineage-18.1-fastboot.zip")
        print("\nFlashing fastboot package...")
        fastbootPkgFlash("lineage-18.1-fastboot.zip")

def downloadAndFlashLineageRecovery():
    if os.path.isfile('recovery.img'):
        print("Continuing with previously downloaded image...")
    else:
        downloadFile('https://sourceforge.net/projects/malvibuilds/files/losrec.img/download','recovery.img')
    fastbootImgFlash('recovery','recovery.img')

def ifBootloaderUnlocked():
    rebootToBootloader()
    time.sleep(50)
    f = subprocess.check_output(['fastboot','getvar','unlocked'], stderr=subprocess.STDOUT).decode('utf-8').split("\r\n")
    if f[0].split(": ")[1] == "yes":
        return True
    else:
        return False

def unlockBootloader():
    print("Please wait...")
    rebootToBootloader()
    time.sleep(50)
    print("You will be prompted to press VOLUME UP to unlock the bootloader, on the device.")
    x = input("Are you sure you want to continue unlocking your device? (Y/N) ")
    if x.lower() == 'y':
        subprocess.run(['fastboot','flashing','unlock'])
        print('Bootloader successfully unlocked.')
    else:
        print('Bootloader unlock aborted.')

def mainscr():
    print("================================================")
    print("Welcome to the LineageOS for Teracube installer!")
    print("================================================")
    print("Current supported devices: Teracube 2e (yk673v6_lwg62_64/Teracube_2e/2e)")
    print("\nREAD ALL INSTRUCTIONS BEFORE PROCEEDING.")
    print("\nPlease install Google's Platform tools before proceeding.")
    print("\nAfter installation of Google's Platform tools (adb and fastboot),")
    print("please enable USB debugging on your Teracube 2e, connect to PC, and grant all necessary permissions.")
    print("\nAfter connecting, please confirm if you want to continue flashing LineageOS. This will")
    print("wipe ALL userdata, so please back up before continuing.")
    x = input("\nAre you sure you want to continue? (Y/N) ")
    if x.lower() == 'y':
        if checkForTeracube() == True:
            secondscr()
        else:
            print("The device is not a Teracube 2e. Aborting installation.")
            exit()
    else:
        exit()

def secondscr():
    print("\nUnlocking the bootloader")
    print("========================")
    print("Please wait till the tool checks if your bootloader is unlocked...")
    print("\nNote: If the tool fails at this point, please re-run the tool again.")
    print("THIS STEP WILL WIPE YOUR DATA.\n")
    if ifBootloaderUnlocked() == True:
        print("Bootloader is already unlocked.")
        thirdscr()
    elif ifBootloaderUnlocked() == False:
        unlockBootloader()
        thirdscr()

def thirdscr():
    print("\nLineageOS recovery installation.")
    print("================================")
    print("Now LineageOS recovery will be installed on your device, to ensure OTA updates are flashed")
    print("correctly. You will still be able to flash TWRP.")
    print("\nFor now, proceeding to flash LineageOS recovery...")
    downloadAndFlashLineageRecovery()
    fourthscr()

def fourthscr():
    print("\nLineageOS installation.")
    print("=======================")
    print("Now the tool will proceed to install LineageOS on your Teracube 2e.")
    print("As of now, the device should be in fastboot mode.")
    downloadAndFlashLatestLineageRelease()
    finalscr()

def finalscr():
    print("\nWelcome to LineageOS!")
    print("=====================")
    print("You have now successfully installed LineageOS on your device!")
    print("The device is now currently booting into the new operating system, so please wait!")
    print("\nThank you for installing LineageOS!")
    print("\nCreator: Gagan Malvi (XDA: malvigagan, Teracube Community: gagan)")

mainscr()