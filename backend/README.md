# 🤖 Chatbot "I Hear You"    
(!!!ТРЕБУЕТСЯ РЕДАКЦИЯ ТЕКСТА!!!)

## 📋 О проекте

Telegram chatbot project repository for the non-profit organization "I Hear You"

### ✨ Основные возможности

- 💬 Консультации и поддержка пользователей
- 📚 Предоставление информационных материалов
- 📊 Сбор обратной связи

---

## 🚀 Быстрый старт

### 📦 Установка

#### 1. Клонирование репозитория

```bash
git clone https://github.com/your-org/chatbot_i_hear_you.git
cd chatbot_i_hear_you
```

#### 2. Переход в директорию бота

```bash
cd bot
```

#### 3. Создание виртуального окружения

```bash
# Linux/MacOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

#### 4. Установка зависимостей

```bash
pip install -r requirements.txt
```

---

## ⚙️ Настройка

### 1. Создание файла конфигурации

Скопируйте файл с примером переменных окружения:

```bash
cp .env.example .env
```

### 2. Настройка переменных окружения

Откройте файл `.env` и добавьте ваш токен бота:

```env
# Токен бота от @BotFather
BOT_TOKEN=your_bot_token_here

# Режим отладки
DEBUG=False
```

### 3. Получение токена бота

1. Найдите [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Скопируйте полученный токен в файл `.env`

---

## 🎯 Запуск

### Локальный запуск (разработка)

```bash
# Активируйте виртуальное окружение (если еще не активировано)
source venv/bin/activate  # Linux/MacOS
# или
source venv\Scripts\activate  # Windows

# Запустите бота
python3 src/main.py
```

## Разработка

1. Создать локальную копию файла `.env.example` и переименовать `.env`, в нем переменную `DEV` установить в `True`.

2. Собрать контейнеры. Если переменные среды будут изменены, этот шаг необходимо повторить.

```bash
docker-compose build
```

3. Запустить контейнеры в режиме прослушивания и дождаться их полного запуска:

```bash
docker compose up --watch
```

4. После запуска контейнеров будут отслеживаться и автоматически применяться изменения в следующих директориях:

- `/admin/src`
- `/bot/scr`

## Тесты

1. Создать локальную копию файла `.env.example` и переименовать `.env`, в нем переменную `DEV` установить в `True`.

2. Собрать контейнеры. Если переменные среды будут изменены, этот шаг необходимо повторить.

```bash
docker-compose -f docker-compose.yml -f docker-compose.tests.yml build
```

3. Запустить контейнеры в режиме прослушивания и дождаться их полного запуска:

```bash
docker-compose -f docker-compose.yml -f docker-compose.tests.yml up --watch admin-tests admin-postgres-db
```

4. После запуска контейнеров будут отслеживаться и автоматически применяться изменения в следующих директориях:

- `/admin/src`

### Собрать контейнеры

```bash
docker-compose up -d
docker-compose up -d --build # если контейнер нужно пересобрать
```

### Остановить контейнеры

```bash
docker-compose down
docker-compose down -v # если нужно удалить вольюмы
```
