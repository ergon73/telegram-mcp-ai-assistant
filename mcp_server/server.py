"""
FastAPI сервер для MCP (Model Context Protocol).
Предоставляет HTTP API для работы с инструментами каталога игр.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
import tools
import db
from simpleeval import simple_eval


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Управление жизненным циклом приложения.
    Инициализирует БД при запуске сервера.
    """
    # Startup: инициализация БД
    db.init_db()
    yield
    # Shutdown: можно добавить закрытие соединений, если нужно


app = FastAPI(
    title="MCP Game Store Server",
    version="1.0.0",
    lifespan=lifespan
)

# CORS для возможности обращения с любого домена
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CallToolRequest(BaseModel):
    """Модель запроса для вызова инструмента."""
    tool: str
    arguments: Dict[str, Any] = {}


class CallToolResponse(BaseModel):
    """Модель ответа от вызова инструмента."""
    ok: bool
    result: Optional[Any] = None
    error: Optional[str] = None


@app.get("/")
async def root():
    """Корневой эндпоинт."""
    return {"message": "MCP Game Store Server", "version": "1.0.0"}


@app.get("/tools")
async def get_tools() -> List[Dict[str, Any]]:
    """
    Возвращает список всех доступных MCP-инструментов.
    
    Returns:
        List[Dict]: Список описаний инструментов с их схемами
    """
    return tools.MCP_TOOLS


@app.post("/call_tool", response_model=CallToolResponse)
async def call_tool(request: CallToolRequest) -> CallToolResponse:
    """
    Вызывает указанный MCP-инструмент с переданными аргументами.
    
    Args:
        request: Запрос с именем инструмента и аргументами
        
    Returns:
        CallToolResponse: Результат выполнения инструмента или ошибка
    """
    tool_name = request.tool
    arguments = request.arguments
    
    try:
        # Специальная обработка для калькулятора
        if tool_name == "calculate":
            expression = arguments.get("expression", "")
            if not expression:
                return CallToolResponse(
                    ok=False,
                    error="Не указано выражение для вычисления"
                )
            try:
                result = simple_eval(expression)
                return CallToolResponse(ok=True, result=result)
            except Exception as e:
                return CallToolResponse(
                    ok=False,
                    error=f"Ошибка вычисления: {str(e)}"
                )
        
        # Обработка остальных инструментов
        if tool_name not in tools.TOOL_FUNCTIONS:
            return CallToolResponse(
                ok=False,
                error=f"Инструмент '{tool_name}' не найден"
            )
        
        tool_function = tools.TOOL_FUNCTIONS[tool_name]
        
        # Вызов функции с распаковкой аргументов
        if isinstance(arguments, dict):
            result = tool_function(**arguments)
        else:
            result = tool_function(arguments)
        
        return CallToolResponse(ok=True, result=result)
        
    except TypeError as e:
        return CallToolResponse(
            ok=False,
            error=f"Неверные аргументы для инструмента '{tool_name}': {str(e)}"
        )
    except ValueError as e:
        return CallToolResponse(
            ok=False,
            error=str(e)
        )
    except Exception as e:
        return CallToolResponse(
            ok=False,
            error=f"Ошибка при выполнении инструмента: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

