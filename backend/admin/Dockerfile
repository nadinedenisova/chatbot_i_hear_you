FROM python:3.13-bookworm

# Устанавливаем рабочую директорию
WORKDIR /app/src

# Копируем зависимости
COPY requirements.txt /app

# Устанавливаем зависимости
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

# Копируем исходный код приложения
COPY . /app

RUN chmod +x /app/entrypoint.sh

# Команда для запуска приложения
ENTRYPOINT ["/app/entrypoint.sh"]
