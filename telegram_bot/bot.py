"""
Telegram-бот для каталога цифровых игр.
Использует OpenAI GPT-4 для обработки запросов пользователей
и MCP-сервер для работы с каталогом игр.
"""
import asyncio
import json
import re
from typing import Dict, List, Any, Optional
from collections import defaultdict

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from openai import AsyncOpenAI

import config
import mcp_client


# Инициализация бота и диспетчера
bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Клиент OpenAI
openai_client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)

# Хранение контекста диалога для каждого пользователя
user_contexts: Dict[int, List[Dict[str, str]]] = defaultdict(list)


# Системный промпт для GPT-4
SYSTEM_PROMPT = """
Ты — умный помощник по каталогу цифровых игр. 

Доступные инструменты:
1. list_products — показать все игры
2. find_product — найти игру по названию
3. find_products_by_category — найти игры жанра
4. find_products_by_platform — найти игры для платформы
5. find_products_by_price_range — найти игры в ценовом диапазоне
6. add_product — добавить новую игру
7. list_featured_products — показать рекомендованные игры
8. find_similar_products — найти похожие игры
9. calculate — выполнить математическое вычисление

Формат вызова инструмента (JSON):
{
  "tool": "название_инструмента",
  "arguments": {"параметр": "значение"}
}

Примеры запросов пользователя и ответов:

Запрос: "покажи все игры"
Ответ: {"tool": "list_products", "arguments": {}}

Запрос: "найди игру ведьмак"
Ответ: {"tool": "find_product", "arguments": {"name": "ведьмак"}}

Запрос: "покажи RPG игры"
Ответ: {"tool": "find_products_by_category", "arguments": {"category": "RPG"}}

Запрос: "игры на PC"
Ответ: {"tool": "find_products_by_platform", "arguments": {"platform": "PC"}}

Запрос: "игры дешевле 30"
Ответ: {"tool": "find_products_by_price_range", "arguments": {"min_price": 0, "max_price": 30}}

Запрос: "добавь игру Hades цена 25 жанр Action платформа PC"
Ответ: {"tool": "add_product", "arguments": {"name": "Hades", "category": "Action", "price": 25, "platform": "PC"}}

Запрос: "покажи похожие на Witcher 3"
Ответ: {"tool": "find_similar_products", "arguments": {"base_name": "Witcher 3"}}

Запрос: "сколько будет 123 * 456"
Ответ: {"tool": "calculate", "arguments": {"expression": "123 * 456"}}

Если инструмент не нужен, отвечай обычным текстом.
Отвечай дружелюбно, на русском языке.
Если запрос непонятен, задавай уточняющие вопросы.
"""


def get_context(user_id: int) -> List[Dict[str, str]]:
    """Получает контекст диалога для пользователя."""
    if user_id not in user_contexts:
        user_contexts[user_id] = []
    return user_contexts[user_id]


def add_to_context(user_id: int, role: str, content: str) -> None:
    """
    Добавляет сообщение в контекст диалога пользователя.
    Ограничивает историю последними 20 сообщениями.
    """
    context = get_context(user_id)
    context.append({"role": role, "content": content})
    # Ограничение: максимум 20 последних сообщений
    if len(context) > 20:
        context.pop(0)


def format_product_list(products: List[Dict[str, Any]]) -> str:
    """
    Форматирует список игр для отображения пользователю.
    
    Args:
        products: Список словарей с данными игр
        
    Returns:
        str: Отформатированная строка со списком игр
    """
    if not products:
        return "Игры не найдены."
    
    if len(products) > 20:
        products = products[:20]
        message = f"Найдено игр: {len(products)} (показаны первые 20)\n\n"
    else:
        message = f"Найдено игр: {len(products)}\n\n"
    
    for product in products:
        featured_mark = "⭐ " if product.get("is_featured") else "🎮 "
        message += f"{featured_mark}{product['name']}\n"
        message += f"   Платформа: {product['platform']}\n"
        message += f"   Жанр: {product['category']}\n"
        message += f"   Цена: {product['price']} ₽\n\n"
    
    return message.strip()


async def call_openai(user_message: str, user_id: int) -> str:
    """
    Вызывает OpenAI API для обработки запроса пользователя.
    
    Args:
        user_message: Сообщение от пользователя
        user_id: ID пользователя Telegram
        
    Returns:
        str: Ответ от GPT-4
    """
    context = get_context(user_id)
    
    # Формируем список сообщений для API
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(context)
    messages.append({"role": "user", "content": user_message})
    
    try:
        response = await openai_client.chat.completions.create(
            model=config.OPENAI_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Ошибка при вызове OpenAI API: {e}")
        return "Извините, произошла ошибка при обработке вашего запроса."


def parse_json_response(text: str) -> Optional[Dict[str, Any]]:
    """
    Парсит JSON из ответа GPT-4.
    Пытается найти JSON объект в тексте.
    
    Args:
        text: Текст ответа от GPT-4
        
    Returns:
        Optional[Dict]: Распарсенный JSON или None
    """
    # Пытаемся найти JSON объект в тексте
    json_match = re.search(r'\{[^{}]*\}', text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            pass
    
    # Если не нашли, пытаемся распарсить весь текст как JSON
    text = text.strip()
    if text.startswith("{") and text.endswith("}"):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
    
    return None


async def process_user_message(message: Message) -> None:
    """
    Обрабатывает сообщение от пользователя.
    
    Алгоритм:
    1. Добавляем сообщение в контекст
    2. Отправляем запрос к OpenAI
    3. Парсим ответ
    4. Если это JSON с инструментом — вызываем MCP-инструмент
    5. Форматируем и отправляем ответ пользователю
    """
    user_id = message.from_user.id
    user_text = message.text
    
    # Добавляем сообщение пользователя в контекст
    add_to_context(user_id, "user", user_text)
    
    # Получаем ответ от GPT-4
    gpt_response = await call_openai(user_text, user_id)
    
    # Парсим ответ
    tool_call = parse_json_response(gpt_response)
    
    if tool_call and "tool" in tool_call:
        # Это вызов инструмента
        tool_name = tool_call["tool"]
        arguments = tool_call.get("arguments", {})
        
        # Вызываем MCP-инструмент
        result = await mcp_client.call_tool(tool_name, arguments)
        
        if result.get("ok", False):
            tool_result = result.get("result")
            
            # Форматируем результат
            if isinstance(tool_result, list) and tool_result:
                # Это список игр
                if isinstance(tool_result[0], dict) and "name" in tool_result[0]:
                    formatted_result = format_product_list(tool_result)
                else:
                    formatted_result = str(tool_result)
            elif isinstance(tool_result, dict):
                # Это одна игра или объект
                if "name" in tool_result:
                    product = tool_result
                    featured_mark = "⭐ " if product.get("is_featured") else "🎮 "
                    formatted_result = (
                        f"{featured_mark}{product['name']}\n"
                        f"Платформа: {product['platform']}\n"
                        f"Жанр: {product['category']}\n"
                        f"Цена: {product['price']} ₽"
                    )
                else:
                    formatted_result = str(tool_result)
            else:
                # Это простое значение (например, результат вычисления)
                formatted_result = str(tool_result)
            
            # Добавляем результат в контекст
            add_to_context(user_id, "assistant", formatted_result)
            
            # Просим GPT-4 сформулировать финальный ответ
            final_prompt = f"Пользователь спросил: {user_text}\n\nРезультат выполнения инструмента:\n{formatted_result}\n\nСформулируй дружелюбный ответ пользователю на русском языке."
            final_response = await call_openai(final_prompt, user_id)
            
            # Добавляем финальный ответ в контекст
            add_to_context(user_id, "assistant", final_response)
            
            await message.answer(final_response)
        else:
            # Ошибка при вызове инструмента
            error_msg = result.get("error", "Неизвестная ошибка")
            response = f"Произошла ошибка: {error_msg}"
            add_to_context(user_id, "assistant", response)
            await message.answer(response)
    else:
        # Обычный текстовый ответ
        add_to_context(user_id, "assistant", gpt_response)
        await message.answer(gpt_response)


@dp.message(Command("start"))
async def cmd_start(message: Message) -> None:
    """Обработчик команды /start."""
    welcome_message = (
        "👋 Привет! Я бот-помощник по каталогу цифровых игр.\n\n"
        "Я могу помочь тебе:\n"
        "🎮 Найти игры по названию, жанру, платформе или цене\n"
        "➕ Добавить новую игру в каталог\n"
        "⭐ Показать рекомендованные игры\n"
        "🔍 Найти похожие игры\n"
        "🧮 Выполнить математические вычисления\n\n"
        "Просто напиши мне, что тебе нужно, например:\n"
        "• \"покажи все игры\"\n"
        "• \"найди игру witcher\"\n"
        "• \"покажи RPG игры\"\n"
        "• \"игры дешевле 30 долларов\"\n\n"
        "Я понимаю естественный язык, так что пиши как удобно! 😊"
    )
    await message.answer(welcome_message)


@dp.message()
async def handle_message(message: Message) -> None:
    """Обработчик всех текстовых сообщений."""
    await process_user_message(message)


async def main() -> None:
    """Главная функция для запуска бота."""
    print("Запуск Telegram-бота...")
    print(f"MCP Server URL: {config.MCP_SERVER_URL}")
    
    # Проверяем доступность MCP-сервера
    try:
        tools_list = await mcp_client.get_tools()
        print(f"MCP-сервер доступен. Доступно инструментов: {len(tools_list)}")
    except Exception as e:
        print(f"⚠️  Предупреждение: MCP-сервер недоступен: {e}")
        print("Бот запустится, но инструменты работать не будут.")
    
    # Запускаем бота
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

