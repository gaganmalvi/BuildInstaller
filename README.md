### LineageOS for the Teracube 2e

Simple plug-and-play installer for users who want to LineageOS from stock firmware, or from another custom ROM.

##### Dependencies: 
- [Google Platform Tools](https://developer.android.com/studio/releases/platform-tools) installed to PATH
- Python 3.9.x

Note: You can also copy the platform tools to the cloned repository directory for ADB and Fastboot.

##### Usage:
- First, install Platform Tools to PATH, or copy the platform tools to the cloned repository directory for it to 
work.

- Second, install Python 3.9.x, and check the Include in PATH option, or install Python 3.9.x from the Windows 
Store.

- Now, clone the repository:
```
git clone https://github.com/gaganmalvi/BuildInstaller build
```

- Run the Python file.
```
cd build
python3 main.py
```

- Follow the on-screen instructions to install LineageOS on your Teracube 2e.

- For Linux, you can install adb and fastboot via your package manager, and run the python file as shown above.

