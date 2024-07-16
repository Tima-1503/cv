import ftplib

# FTP настройки (замените на ваши)
FTP_SERVER = 'ftp.qanat.kz'
FTP_USER = 'vkim'
FTP_PASSWORD = 'akco72TGH$'

def create_ftp_directory(directory):
    try:
        # Устанавливаем соединение с FTP-сервером
        ftps = ftplib.FTP_TLS()
        ftps.connect(FTP_SERVER, 21)
        ftps.auth()
        ftps.login(FTP_USER, FTP_PASSWORD)
        ftps.prot_p()

        # Создаем папку
        if directory not in ftps.nlst():
            ftps.mkd(directory)
            print(f"Directory '{directory}' created successfully.")
        else:
            print(f"Directory '{directory}' already exists.")

        # Закрываем соединение
        ftps.quit()
    except ftplib.all_errors as e:
        print(f"Error creating directory on FTP: {e}")

if __name__ == "__main__":
    create_ftp_directory('/monitoring/tmp2')
