import platform
import cv2
import time
import requests
import ftplib
from datetime import datetime
import os
import socket
import dlib

# Настройка видеопотока
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Инициализация детектора лиц из dlib
detector = dlib.get_frontal_face_detector()

# Функция оценки расстояния до лица
def estimate_distance(face_width_px):
    KNOWN_WIDTH = 14.0  # средняя ширина лица в см
    FOCAL_LENGTH = 615  # фокусное расстояние камеры в пикселях
    distance = (KNOWN_WIDTH * FOCAL_LENGTH) / face_width_px
    return distance

# Адрес сервера
SERVER_URL = 'https://request.qanat.kz'

# Токен для авторизации (замените на ваш токен)
TOKEN = 'rAO0woSmvvze8g3XKIQVmPvaGammf5MhbHMCwGagTKHgu0ZuDuyqTiRH2zV8VUfA'

# Информация о клиенте
computer_name = platform.node()  # Имя компьютера
username = os.getlogin()  # Имя пользователя

# Переменные для отслеживания состояния
presence_detected = False
last_status_change_time = datetime.now()
waiting_for_recovery = False
recovery_start_time = None

# FTP настройки (замените на ваши)
FTP_SERVER = '109.248.156.34'
FTP_USER = 'admin'
FTP_PASSWORD = 'TVx7*15%5VyM*k~B'

# Функция для проверки доступности интернет-соединения
def is_internet_available():
    try:
        # Попытка подключения к серверу Google DNS по порту 80
        socket.create_connection(("ya.ru", 80), timeout=1)
        return True
    except OSError:
        pass
    return False

def send_status_to_server(status):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    headers = {
        'Authorization': f'Bearer {TOKEN}'
    }
    payload = {
        'status': status,
        'computer_name': computer_name,
        'username': username,
        'current_date': current_time
    }
    try:
        response = requests.post(SERVER_URL, json=payload, headers=headers)
        response.raise_for_status()
        print(f"Data sent to server: {payload}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data to server: {e}")

def main():
    global presence_detected, last_status_change_time, waiting_for_recovery, recovery_start_time

    while True:
        # Проверяем доступность интернета перед началом работы
        if not is_internet_available():
            time.sleep(5)  # Ждем 5 секунд перед повторной проверкой
            continue

        ret, frame = cap.read()
        if not ret:
            print("Error reading frame")
            continue

        # Используем детектор лиц dlib
        faces = detector(frame)

        face_detected = False
        for face in faces:
            (x, y, w, h) = (face.left(), face.top(), face.width(), face.height())
            distance = estimate_distance(w)
            if 5 <= distance <= 85:  # Проверка расстояния до лица
                face_detected = True
                break

        if face_detected and not presence_detected:
            presence_detected = True
            last_status_change_time = datetime.now()
            send_status_to_server(True)
        elif not face_detected and presence_detected:
            if not waiting_for_recovery:
                waiting_for_recovery = True
                recovery_start_time = datetime.now()
            else:
                time_since_recovery_start = datetime.now() - recovery_start_time
                if time_since_recovery_start.total_seconds() >= 10:
                    presence_detected = False
                    waiting_for_recovery = False
                    send_status_to_server(False)
                    last_status_change_time = datetime.now()
        elif face_detected and waiting_for_recovery:
            waiting_for_recovery = False  # Отменяем отправку статуса "отсутствия"

        # Ограничение частоты обновления кадров
        time.sleep(0.2)  # 5 кадров в секунду (0.2 секунды между кадрами)

if __name__ == "__main__":
    try:
        main()
    finally:
        cap.release()
        cv2.destroyAllWindows()
        # При завершении работы отправляем последний статус на сервер
        if presence_detected:
            send_status_to_server(False)  # Закрываем открытый период присутствия
