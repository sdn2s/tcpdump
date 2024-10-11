import os
import subprocess

# Ввод данных от пользователя
INTERFACE = input("Введите имя сетевого интерфейса (например, eth0): ")
DURATION = int(input("Введите время захвата в секундах: "))

# Путь для сохранения файлов
OUTPUT_DIR = "/path/to/save"

# Максимальное количество файлов
MAX_FILES = 15

# Проверяем, существует ли каталог
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print(f"Запуск сбора tcpdump на интерфейсе {INTERFACE} с ротацией каждые {DURATION} секунд, максимум {MAX_FILES} файлов")

try:
    # Формируем команду tcpdump с ротацией файлов
    filename_template = os.path.join(OUTPUT_DIR, "capture-%Y%m%d%H%M%S.pcap")
    command = [
        "sudo", "tcpdump", "-i", INTERFACE, "-G", str(DURATION), "-W", str(MAX_FILES), "-w", filename_template
    ]

    # Запуск процесса
    subprocess.run(command)
except Exception as e:
    print(f"Ошибка при запуске tcpdump: {e}")
