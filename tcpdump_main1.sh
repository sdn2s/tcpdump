#!/bin/bash

# Интерфейс для захвата
INTERFACE="p00"

# Путь для сохранения файлов
OUTPUT_DIR="/path/to/save"

# Время захвата дампа в секундах
DURATION=15

# Максимальное количество файлов
MAX_FILES=15

# Проверяем, существует ли каталог
if [ ! -d "$OUTPUT_DIR" ]; then
    mkdir -p "$OUTPUT_DIR"
fi

echo "Запуск сбора tcpdump на интерфейсе $INTERFACE с ротацией каждые $DURATION секунд, максимум $MAX_FILES файлов"

# Бесконечный цикл для непрерывной работы
while true; do 
    # Создание нового дампа с уникальным именем
    TIMESTAMP=$(date +"%Y%m%d%H%M%S")
    FILENAME="$OUTPUT_DIR/capture-$TIMESTAMP.pcap"
    
    # Запуск tcpdump на 15 секунд
    sudo tcpdump -i "$INTERFACE" -w "$FILENAME" &
    PID=$!
    sleep $DURATION
    sudo kill $PID

    echo "Дамп сохранен в файле $FILENAME"

    # Подсчет текущего количества файлов
    NUM_FILES=$(ls -1q $OUTPUT_DIR/capture-*.pcap | wc -l)

    # Если файлов больше, чем нужно
    if [ $NUM_FILES -gt $MAX_FILES ]; then
        # Удаление старых файлов, чтобы осталось $MAX_FILES
        ls -1tr $OUTPUT_DIR/capture-*.pcap | head -n -$MAX_FILES | xargs rm -f
    fi

    echo "Текущее количество файлов: $NUM_FILES"
done