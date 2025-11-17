"""
Модуль конфигурации для Telegram-бота.
Читает переменные окружения из .env файла.
"""
import os
from dotenv import load_dotenv


load_dotenv()

# OpenAI API настройки
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY не найден в .env файле")

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не найден в .env файле")

# MCP Server URL
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000")

# OpenAI Model
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

