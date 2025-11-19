"""
Описание MCP-инструментов для работы с каталогом игр.
Содержит структуру инструментов и маппинг на функции из db.py.
"""
from typing import Dict, Callable, Any
import db


# Описание всех MCP-инструментов
MCP_TOOLS = [
    {
        "name": "list_products",
        "description": "Возвращает список всех игр в каталоге",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "find_product",
        "description": "Ищет игры по частичному совпадению названия",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Название игры для поиска (частичное совпадение)"
                }
            },
            "required": ["name"]
        }
    },
    {
        "name": "find_products_by_category",
        "description": "Находит игры определённого жанра (Action, RPG, Strategy, Indie, Adventure, Shooter, Simulation)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "Жанр игры (Action, RPG, Strategy, Indie, Adventure, Shooter, Simulation)"
                }
            },
            "required": ["category"]
        }
    },
    {
        "name": "find_products_by_platform",
        "description": "Находит игры для конкретной платформы (PC, PlayStation, Xbox, Switch, Mobile)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "platform": {
                    "type": "string",
                    "description": "Платформа (PC, PlayStation, Xbox, Switch, Mobile)"
                }
            },
            "required": ["platform"]
        }
    },
    {
        "name": "find_products_by_price_range",
        "description": "Находит игры в заданном ценовом диапазоне",
        "inputSchema": {
            "type": "object",
            "properties": {
                "min_price": {
                    "type": "number",
                    "description": "Минимальная цена"
                },
                "max_price": {
                    "type": "number",
                    "description": "Максимальная цена"
                }
            },
            "required": ["min_price", "max_price"]
        }
    },
    {
        "name": "add_product",
        "description": "Добавляет новую игру в каталог",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Название игры"
                },
                "category": {
                    "type": "string",
                    "description": "Жанр игры (Action, RPG, Strategy, Indie, Adventure, Shooter, Simulation)"
                },
                "price": {
                    "type": "number",
                    "description": "Цена игры"
                },
                "platform": {
                    "type": "string",
                    "description": "Платформа (PC, PlayStation, Xbox, Switch, Mobile)"
                },
                "is_featured": {
                    "type": "integer",
                    "description": "Рекомендованная игра (1) или нет (0), по умолчанию 0",
                    "default": 0
                }
            },
            "required": ["name", "category", "price", "platform"]
        }
    },
    {
        "name": "list_featured_products",
        "description": "Возвращает список рекомендованных игр (избранное)",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "find_similar_products",
        "description": "Находит похожие игры на основе жанра и платформы указанной игры",
        "inputSchema": {
            "type": "object",
            "properties": {
                "base_name": {
                    "type": "string",
                    "description": "Название игры, похожие на которую нужно найти"
                }
            },
            "required": ["base_name"]
        }
    },
    {
        "name": "calculate",
        "description": "Безопасно вычисляет математическое выражение",
        "inputSchema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Математическое выражение для вычисления (например: '123 * 456', '10 + 20 - 5')"
                }
            },
            "required": ["expression"]
        }
    }
]


# Маппинг инструментов на функции из db.py
TOOL_FUNCTIONS: Dict[str, Callable] = {
    "list_products": db.get_all_products,
    "find_product": db.find_products_by_name,
    "find_products_by_category": db.find_products_by_category,
    "find_products_by_platform": db.find_products_by_platform,
    "find_products_by_price_range": db.find_products_by_price_range,
    "add_product": db.add_product,
    "list_featured_products": db.get_featured_products,
    "find_similar_products": db.find_similar_products,
}

