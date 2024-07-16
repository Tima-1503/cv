from setuptools import setup

APP = ['cv-mac.py']  # Замените 'your_script.py' на имя вашего основного скрипта

OPTIONS = {
    'argv_emulation': True,
    'packages': ['cv2', 'dlib', 'requests', 'ftplib', 'os', 'socket', 'time'],
    'plist': {
        'CFBundleName': 'YourAppName',
        'CFBundleDisplayName': 'Your App Name',
        'CFBundleGetInfoString': "Your App Description",
        'CFBundleIdentifier': "com.yourcompany.yourapp",
        'CFBundleVersion': "0.1.0",
        'CFBundleShortVersionString': "0.1.0",
        'CFBundleExecutable': "YourAppName",
        'LSUIElement': True,  # Если ваше приложение не показывает окно
    },

}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
