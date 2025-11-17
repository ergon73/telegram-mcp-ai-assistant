# 🎮 MCP Game Store Telegram Bot

> Telegram-бот для каталога цифровых игр с использованием Model Context Protocol (MCP) и GPT-4

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![aiogram](https://img.shields.io/badge/aiogram-3.0+-blue.svg)](https://docs.aiogram.dev/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange.svg)](https://openai.com/)

---

## 📖 Описание

Учебный проект по курсу **вайб-кодинга**, демонстрирующий интеграцию:
- **MCP (Model Context Protocol)** — универсальный протокол для работы AI-агентов с инструментами
- **FastAPI** — современный веб-фреймворк для создания MCP-сервера
- **SQLite** — локальная база данных каталога игр
- **Telegram Bot** — интерфейс для пользователей
- **OpenAI GPT-4** — мозг системы, принимающий решения о вызове инструментов

### Архитектура

```
┌─────────────┐
│   Telegram  │
│    User     │
└──────┬──────┘
       │
       ▼
┌─────────────┐      ┌──────────────┐
│  Telegram   │─────▶│   OpenAI     │
│     Bot     │◀─────│    GPT-4     │
└──────┬──────┘      └──────────────┘
       │
       │ HTTP
       ▼
┌─────────────┐
│    MCP      │
│   Server    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   SQLite    │
│  Database   │
└─────────────┘
```

---

## ✨ Возможности

### Основной функционал

- 🎮 **Каталог игр** — более 100 цифровых игр в базе данных
- 🔍 **Умный поиск** — по названию, жанру, платформе, цене
- ➕ **Добавление игр** — пополнение каталога через диалог с ботом
- 🎯 **Рекомендации** — похожие игры на основе жанра и платформы
- ⭐ **Избранное** — специальная подборка рекомендованных игр
- 🧮 **Калькулятор** — безопасные математические вычисления

### MCP-инструменты

Реализовано 9 MCP-инструментов:

1. `list_products` — список всех игр
2. `find_product` — поиск по названию
3. `find_products_by_category` — поиск по жанру
4. `find_products_by_platform` — поиск по платформе
5. `find_products_by_price_range` — поиск в ценовом диапазоне
6. `add_product` — добавление новой игры
7. `list_featured_products` — рекомендованные игры
8. `find_similar_products` — поиск похожих игр
9. `calculate` — безопасный калькулятор

---

## 🚀 Быстрый старт

### Требования

- Python 3.11 или выше
- Токен Telegram-бота (получить у [@BotFather](https://t.me/BotFather))
- API ключ OpenAI (получить на [platform.openai.com](https://platform.openai.com/))

### Установка

1. **Клонировать репозиторий:**

```bash
git clone https://github.com/yourusername/mcp-game-store-bot.git
cd mcp-game-store-bot
```

2. **Создать виртуальное окружение:**

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# или
.venv\Scripts\activate     # Windows
```

3. **Установить зависимости:**

```bash
pip install -r mcp_server/requirements.txt
pip install -r telegram_bot/requirements.txt
```

4. **Настроить переменные окружения:**

Создать файл `.env` в корне проекта:

```env
OPENAI_API_KEY=sk-proj-your-key-here
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
MCP_SERVER_URL=http://localhost:8000
```

### Запуск

**Терминал 1 — MCP-сервер:**

```bash
cd mcp_server
python server.py
```

**Терминал 2 — Telegram-бот:**

```bash
cd telegram_bot
python bot.py
```

Готово! Теперь можно писать боту в Telegram.

---

## 💬 Примеры использования

### Основные команды

```
/start — приветствие и описание возможностей
```

### Примеры запросов

**Поиск игр:**
```
👤 покажи все игры
🤖 [список игр из каталога]

👤 найди игру witcher
🤖 🎮 The Witcher 3: Wild Hunt
   Платформа: PC
   Жанр: RPG
   Цена: 40 ₽
```

**Поиск по параметрам:**
```
👤 покажи RPG игры на PlayStation дешевле 50 долларов
🤖 [список подходящих игр]
```

**Добавление игры:**
```
👤 добавь игру Hollow Knight цена 15 жанр Indie платформа PC
🤖 ✅ Игра успешно добавлена в каталог!
   🎮 Hollow Knight
   Платформа: PC
   Жанр: Indie
   Цена: 15 ₽
```

**Рекомендации:**
```
👤 найди похожие игры на The Witcher 3
🤖 [список игр жанра RPG для той же платформы]

👤 что порекомендуешь?
🤖 [список рекомендованных игр]
```

**Вычисления:**
```
👤 сколько будет 199 * 3
🤖 199 * 3 = 597
```

---

## 📁 Структура проекта

```
product-mcp/
├── README.md                 # Основное описание проекта
├── human-readme.md           # Руководство для разработчика
├── genai-readme.md           # Техническое задание для AI-агента
├── .cursorrules              # Правила для Cursor IDE
├── .env.example              # Шаблон переменных окружения
├── .gitignore
│
├── mcp_server/               # MCP-сервер (FastAPI)
│   ├── server.py             # HTTP API эндпоинты
│   ├── db.py                 # Работа с SQLite БД
│   ├── tools.py              # Описание MCP-инструментов
│   ├── products.db           # База данных (создаётся автоматически)
│   └── requirements.txt
│
└── telegram_bot/             # Telegram-бот (MCP-клиент)
    ├── bot.py                # Логика бота и обработчики
    ├── config.py             # Конфигурация (.env)
    ├── mcp_client.py         # HTTP-клиент для MCP-сервера
    └── requirements.txt
```

---

## 🛠️ Технологии

### Backend (MCP-сервер)

- **FastAPI** — современный веб-фреймворк
- **Uvicorn** — ASGI сервер
- **SQLite3** — встроенная база данных
- **Pydantic** — валидация данных

### Frontend (Telegram-бот)

- **aiogram 3.x** — асинхронный фреймворк для Telegram ботов
- **OpenAI Python SDK** — интеграция с GPT-4
- **httpx** — асинхронный HTTP-клиент

### Инструменты разработки

- **python-dotenv** — управление переменными окружения
- **simpleeval** — безопасное вычисление математических выражений

---

## 📚 Документация

- [human-readme.md](human-readme.md) — пошаговое руководство по созданию проекта
- [genai-readme.md](genai-readme.md) — техническое задание для AI-агента
- [.cursorrules](.cursorrules) — правила работы в Cursor IDE

---

## 🧪 Тестирование

### Базовые сценарии

Перед деплоем протестировать следующие сценарии:

1. ✅ Запуск MCP-сервера без ошибок
2. ✅ Запуск Telegram-бота без ошибок
3. ✅ Команда `/start`
4. ✅ Список всех игр
5. ✅ Поиск по названию
6. ✅ Поиск по жанру
7. ✅ Поиск по платформе
8. ✅ Поиск по цене
9. ✅ Добавление новой игры
10. ✅ Поиск похожих игр
11. ✅ Рекомендованные игры
12. ✅ Калькулятор
13. ✅ Сохранение контекста диалога

---

## 🤝 Вклад в проект

Проект создан в образовательных целях в рамках курса **вайб-кодинга**.

Если хотите улучшить проект:

1. Fork репозитория
2. Создайте ветку для фичи (`git checkout -b feature/AmazingFeature`)
3. Commit изменений (`git commit -m 'Add some AmazingFeature'`)
4. Push в ветку (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

---

## 📝 Лицензия

Этот проект создан в образовательных целях и распространяется под лицензией MIT.

---

## 👨‍💻 Автор

**Georgy**

- 📧 Email: [your-email@example.com]
- 💼 LinkedIn: [your-linkedin]
- 🐙 GitHub: [@yourusername](https://github.com/yourusername)

---

## 🙏 Благодарности

- Курс **вайб-кодинг** за отличные материалы и практику
- **Anthropic** за Model Context Protocol
- **OpenAI** за мощное API
- Сообщество разработчиков за поддержку и вдохновение

---

## 📊 Статус проекта

🟢 **Активная разработка** — проект создан как учебная работа и может быть расширен дополнительными функциями.

### Возможные улучшения

- [ ] Добавление рейтингов и отзывов
- [ ] Интеграция с внешними API (RAWG, Steam)
- [ ] Система скидок и акций
- [ ] Мультиязычность (EN/RU)
- [ ] Веб-интерфейс для администрирования
- [ ] Деплой на облачный сервер
- [ ] Мониторинг и логирование
- [ ] Unit и интеграционные тесты

---

<p align="center">
  Сделано с ❤️ и помощью AI
</p>
