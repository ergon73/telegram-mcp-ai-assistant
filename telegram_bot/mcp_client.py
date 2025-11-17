"""
HTTP-клиент для работы с MCP-сервером.
Предоставляет функции для получения списка инструментов и их вызова.
"""
from typing import List, Dict, Any, Optional
import httpx
import config


async def get_tools() -> List[Dict[str, Any]]:
    """
    Получает список всех доступных MCP-инструментов с сервера.
    
    Returns:
        List[Dict]: Список описаний инструментов
        
    Raises:
        Exception: Если сервер недоступен или произошла ошибка
    """
    url = f"{config.MCP_SERVER_URL}/tools"
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
    except httpx.TimeoutException:
        raise Exception("MCP сервер недоступен: timeout")
    except httpx.HTTPError as e:
        raise Exception(f"MCP сервер недоступен: {str(e)}")


async def call_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Вызывает указанный MCP-инструмент с переданными аргументами.
    
    Args:
        tool_name: Имя инструмента для вызова
        arguments: Словарь с аргументами инструмента
        
    Returns:
        Dict: Результат выполнения инструмента
        Формат: {"ok": bool, "result": any, "error": str}
        
    Raises:
        Exception: Если сервер недоступен
    """
    url = f"{config.MCP_SERVER_URL}/call_tool"
    
    payload = {
        "tool": tool_name,
        "arguments": arguments
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            result = response.json()
            
            if not result.get("ok", False):
                error_msg = result.get("error", "Неизвестная ошибка")
                print(f"Ошибка при вызове инструмента {tool_name}: {error_msg}")
            
            return result
    except httpx.TimeoutException:
        error_msg = "MCP сервер недоступен: timeout"
        print(f"Ошибка при вызове инструмента {tool_name}: {error_msg}")
        return {"ok": False, "error": error_msg}
    except httpx.HTTPError as e:
        error_msg = f"MCP сервер недоступен: {str(e)}"
        print(f"Ошибка при вызове инструмента {tool_name}: {error_msg}")
        return {"ok": False, "error": error_msg}

