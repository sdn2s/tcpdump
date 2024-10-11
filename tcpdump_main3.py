import os
import subprocess
import time
from datetime import datetime
import glob

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

# Функция для подсчета количества файлов
def count_pcap_files():
    return len(glob.glob(os.path.join(OUTPUT_DIR, "capture-*.pcap")))

# Функция для удаления старых файлов
def remove_old_files():
    pcap_files = sorted(glob.glob(os.path.join(OUTPUT_DIR, "capture-*.pcap")), key=os.path.getmtime)
    if len(pcap_files) > MAX_FILES:
        files_to_remove = pcap_files[:len(pcap_files) - MAX_FILES]
        for file in files_to_remove:
            os.remove(file)
            print(f"Удалён файл: {file}")

# Бесконечный цикл для непрерывной работы
while True:
    # Создание нового дампа с уникальным именем
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = os.path.join(OUTPUT_DIR, f"capture-{timestamp}.pcap")
    
    # Запуск tcpdump на заданное время
    process = subprocess.Popen(["sudo", "tcpdump", "-i", INTERFACE, "-w", filename])
    time.sleep(DURATION)
    process.terminate()  # Завершаем процесс tcpdump
    
    print(f"Дамп сохранен в файле {filename}")
    
    # Подсчет текущего количества файлов
    num_files = count_pcap_files()
    
    # Если файлов больше, чем нужно
    if num_files > MAX_FILES:
        remove_old_files()
    
    print(f"Текущее количество файлов: {num_files}")
