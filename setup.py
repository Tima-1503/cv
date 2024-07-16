from setuptools import setup

APP = ['your_script.py']  # Замените 'your_script.py' на имя вашего основного скрипта

OPTIONS = {
    'argv_emulation': True,
    'packages': ['cv2', 'dlib', 'requests', 'ftplib', 'platform', 'os', 'socket', 'time'],
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
    'iconfile': 'icon.icns',  # Укажите путь к вашему файлу иконки, если требуется
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
