import requests
import getpass
import platform
import datetime
import psutil  # Для получения времени включения ПК на Windows


def collect_pc_activity():
    # Собираем информацию о пользователе и ПК
    username = getpass.getuser()
    pc_name = platform.node()

    # Получаем время включения ПК
    try:
        if platform.system() == 'Windows':
            startup_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        else:
            # Здесь можно использовать другой метод для UNIX-подобных систем, если требуется
            startup_time = datetime.datetime.now()  # Ваша логика для UNIX-подобных систем
    except Exception as e:
        print(f'Ошибка при получении времени включения ПК: {str(e)}')
        return

    shutdown_time = datetime.datetime.now()  # Ваша логика получения времени выключения ПК

    # Преобразуем datetime в строки
    startup_time_str = startup_time.strftime('%Y-%m-%d %H:%M:%S')
    shutdown_time_str = shutdown_time.strftime('%Y-%m-%d %H:%M:%S')

    # Формируем данные для отправки на сервер
    data = {
        'username': username,
        'pc_name': pc_name,
        'startup_time': startup_time_str,
        'shutdown_time': shutdown_time_str
    }

    # Отправляем POST запрос на сервер Django
    url = 'http://django.qanat.kz//pcactivity/collect_pc_activity/'  # Замените на ваш URL обработчика в Django
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Проверяем успешность запроса
        print('Данные успешно отправлены на сервер Django.')
    except requests.exceptions.RequestException as e:
        print(f'Ошибка при отправке данных на сервер Django: {str(e)}')


if __name__ == '__main__':
    collect_pc_activity()
