from setuptools import setup

APP = ['cv-mac.py']  # Замените 'main.py' на имя вашего скрипта
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['cv2', 'requests'],
    'plist': {
        'CFBundleName': 'YourAppName',
        'CFBundleDisplayName': 'YourAppName',
        'CFBundleIdentifier': 'com.yourname.yourappname',
        'CFBundleVersion': '0.1.0',
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)