# Frontend

## 📦 Технологии

- **React 19** + **TypeScript 5**
- **Vite 7** — сборка и dev-сервер
- **Redux Toolkit** + RTK Query — управление состоянием и API-клиент
- **React Router 7** — маршрутизация
- **MUI v7** + Emotion — UI-компоненты и стили
- **@rtk-query/codegen-openapi** — автогенерация типизированного API-клиента из OpenAPI спецификации

## 🚀 Установка и запуск

```bash
# установка зависимостей
npm install

# запуск dev-сервера
npm run dev

# сборка для продакшена
npm run build

# предпросмотр билда
npm run preview
```

## 🧹Линтинг и форматирование

В проекте настроены следующие инструменты для поддержания качества кода и удобства разработки:

- **ESLint** — проверка TypeScript/React-кода.
- **Prettier** — автоформатирование кода.
- **EditorConfig** — стандартизация настроек редактора.
- **Stylelint** — проверка CSS/SCSS.
- **Husky** — хуки Git для автоматического запуска проверок перед коммитом.
- **MSW (Mock Service Worker)** — моки API для локальной разработки.

```bash
# ESLint
npm run lint
npm run lint:fix

# Stylelint (scss/css)
npm run lint:style

# Prettier
npm run format
```

### 🔌 Рекомендации для разработчиков

Если у вас ещё не установлены расширения VSCode, рекомендуем добавить:

- **Prettier**
- **Stylelint**
- **EditorConfig**

### 🐶 Husky

Husky запускает перед коммитом только в директорию frontend:

1. Prettier
2. Stylelint
3. ESLint

## 🔗 API

Генерация API-клиента из OpenAPI-спецификации:

Проект использует RTK Query для работы с API.
API-клиент генерируется из OpenAPI спецификации:

### Генерация API

При обновлении API на бэкенде:

- Обновите файл `frontend/openapi.yaml` (новая спецификация API).
- Выполните скрипт генерации: `npm run generate:api`
- Вы великолепны!
- После генерации создаются типизированные endpoint’ы в `frontend/src/api.ts`, которые можно использовать напрямую в компонентах React через hooks (useGetSomethingQuery, usePostSomethingMutation и т.д.)

### Разработка с локальным бэкендом

В Vite dev-сервере настроено проксирование `/api` на локальный бэкенд.
Quick старт бэкенда:

- перейти в директорию `backend`
- скопировать `.env-example` в `.env`
- задать `BOT_TOKEN` в `.env` (токен можно получить у бэкендеров или самому зарегистрировать бот в телеграм)
- запустить `docker compose up --build`
