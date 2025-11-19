"""
FastAPI сервер для MCP (Model Context Protocol).
Предоставляет HTTP API для работы с инструментами каталога игр.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional
import re
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


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Обработчик ошибок ValueError (включая проблемы с сериализацией больших чисел)."""
    error_msg = str(exc)
    if "int_max_str_digits" in error_msg or "Exceeds the limit" in error_msg:
        return JSONResponse(
            status_code=200,
            content={
                "ok": False,
                "error": "Результат вычисления слишком большой для отображения"
            }
        )
    # Для других ValueError возвращаем стандартную ошибку
    return JSONResponse(
        status_code=500,
        content={"ok": False, "error": f"Ошибка: {error_msg}"}
    )


class CallToolRequest(BaseModel):
    """Модель запроса для вызова инструмента."""
    tool: str
    arguments: Dict[str, Any] = Field(default_factory=dict)


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
        return await _call_tool_internal(tool_name, arguments)
    except ValueError as e:
        # Перехватываем ошибки сериализации JSON (слишком большие числа)
        error_msg = str(e)
        if "int_max_str_digits" in error_msg or "Exceeds the limit" in error_msg:
            return CallToolResponse(
                ok=False,
                error="Результат вычисления слишком большой для отображения"
            )
        raise
    except Exception as e:
        # Перехватываем любые другие неожиданные ошибки
        return CallToolResponse(
            ok=False,
            error=f"Внутренняя ошибка сервера: {str(e)}"
        )


async def _call_tool_internal(tool_name: str, arguments: Dict[str, Any]) -> CallToolResponse:
    """Внутренняя функция для вызова инструмента."""
    try:
        # Специальная обработка для калькулятора
        if tool_name == "calculate":
            expression = (arguments.get("expression") or "").strip()
            if not expression:
                return CallToolResponse(
                    ok=False,
                    error="Не указано выражение для вычисления"
                )
            
            # Защита от DoS: ограничение длины и whitelist символов
            if len(expression) > 100:
                return CallToolResponse(
                    ok=False,
                    error="Выражение слишком длинное (максимум 100 символов)"
                )
            
            # Запрещаем оператор степени (**) для защиты от DoS
            if "**" in expression:
                return CallToolResponse(
                    ok=False,
                    error="Оператор степени (**) не разрешён из соображений безопасности"
                )
            
            # Разрешаем только безопасные математические символы
            if not re.fullmatch(r"[0-9()+\-*/. \t\n]+", expression):
                return CallToolResponse(
                    ok=False,
                    error="Допустимы только числа и операторы +-*/()."
                )
            
            # Проверка на очень большие числа в выражении (защита от DoS)
            # Ищем числа длиннее 10 цифр
            large_number_pattern = r'\d{11,}'
            if re.search(large_number_pattern, expression):
                return CallToolResponse(
                    ok=False,
                    error="Числа в выражении слишком большие (максимум 10 цифр)"
                )
            
            try:
                # Используем simple_eval с ограничениями для безопасности
                result = simple_eval(expression, names={}, functions={})
                
                # Проверяем результат на разумность (защита от переполнения и проблем с JSON)
                if isinstance(result, (int, float)):
                    # Проверка на очень большие числа (больше 10^15)
                    if abs(result) > 1e15:
                        return CallToolResponse(
                            ok=False,
                            error="Результат вычисления слишком большой"
                        )
                    
                    # Проверка на числа, которые могут вызвать проблемы при сериализации JSON
                    # Python 3.13+ имеет ограничение на количество цифр в строковом представлении (4300 по умолчанию)
                    if isinstance(result, int):
                        # Используем математический подход для оценки количества цифр
                        # log10(n) + 1 даёт количество цифр, но для очень больших чисел это тоже может быть проблемой
                        # Поэтому просто проверяем абсолютное значение
                        if abs(result) > 10**100:  # Безопасный лимит (100 цифр)
                            return CallToolResponse(
                                ok=False,
                                error="Результат вычисления слишком большой для отображения"
                            )
                
                return CallToolResponse(ok=True, result=result)
            except (OverflowError, MemoryError) as e:
                return CallToolResponse(
                    ok=False,
                    error="Результат вычисления слишком большой или вызывает переполнение"
                )
            except ValueError as e:
                # Обработка ошибок сериализации JSON (например, слишком большие числа)
                error_msg = str(e)
                if "int_max_str_digits" in error_msg or "Exceeds the limit" in error_msg:
                    return CallToolResponse(
                        ok=False,
                        error="Результат вычисления слишком большой для отображения"
                    )
                return CallToolResponse(
                    ok=False,
                    error=f"Ошибка вычисления: {error_msg}"
                )
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

