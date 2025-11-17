"""
Модуль для работы с базой данных SQLite.
Содержит функции CRUD для работы с таблицей products.
"""
import sqlite3
from typing import List, Dict, Optional, Any


DB_PATH = "products.db"


def get_connection() -> sqlite3.Connection:
    """Создаёт и возвращает соединение с БД."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """
    Создаёт таблицу products и заполняет её тестовыми данными.
    Минимум 100 игр, все категории и платформы представлены.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        
        # Создание таблицы
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL,
                platform TEXT NOT NULL,
                is_featured INTEGER NOT NULL DEFAULT 0
            )
        """)
        
        # Проверка, есть ли уже данные
        cursor.execute("SELECT COUNT(*) FROM products")
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Заполнение тестовыми данными
            games = [
                # Featured games
                ("The Witcher 3: Wild Hunt", "RPG", 40.0, "PC", 1),
                ("Elden Ring", "RPG", 60.0, "PlayStation", 1),
                ("Hollow Knight", "Indie", 15.0, "PC", 1),
                ("Cyberpunk 2077", "Action", 60.0, "PC", 1),
                ("God of War", "Action", 50.0, "PlayStation", 1),
                ("Breath of the Wild", "Adventure", 60.0, "Switch", 1),
                ("Stardew Valley", "Simulation", 15.0, "Switch", 1),
                ("Dark Souls III", "RPG", 60.0, "PC", 1),
                ("Red Dead Redemption 2", "Adventure", 60.0, "PlayStation", 1),
                ("Portal 2", "Puzzle", 10.0, "PC", 1),
                ("Half-Life: Alyx", "Shooter", 60.0, "PC", 1),
                ("The Last of Us Part II", "Action", 60.0, "PlayStation", 1),
                ("Super Mario Odyssey", "Adventure", 60.0, "Switch", 1),
                ("Celeste", "Indie", 20.0, "PC", 1),
                ("Hades", "Action", 25.0, "PC", 1),
                
                # Action games
                ("Doom Eternal", "Action", 40.0, "PC", 0),
                ("Devil May Cry 5", "Action", 40.0, "PlayStation", 0),
                ("Assassin's Creed Valhalla", "Action", 60.0, "PC", 0),
                ("Monster Hunter: World", "Action", 40.0, "PlayStation", 0),
                ("Nier: Automata", "Action", 40.0, "PC", 0),
                ("Metal Gear Solid V", "Action", 30.0, "PC", 0),
                ("Bayonetta 2", "Action", 60.0, "Switch", 0),
                ("Spider-Man", "Action", 50.0, "PlayStation", 0),
                ("Tomb Raider", "Action", 20.0, "PC", 0),
                ("Uncharted 4", "Action", 40.0, "PlayStation", 0),
                ("Just Cause 4", "Action", 40.0, "PC", 0),
                ("Dead Cells", "Action", 25.0, "PC", 0),
                ("Sekiro: Shadows Die Twice", "Action", 60.0, "PC", 0),
                ("Batman: Arkham Knight", "Action", 20.0, "PC", 0),
                ("Horizon Zero Dawn", "Action", 40.0, "PlayStation", 0),
                ("Resident Evil 4", "Action", 40.0, "PC", 0),
                ("Shadow of the Tomb Raider", "Action", 30.0, "PC", 0),
                
                # RPG games
                ("Skyrim", "RPG", 20.0, "PC", 0),
                ("Final Fantasy VII Remake", "RPG", 60.0, "PlayStation", 0),
                ("Persona 5 Royal", "RPG", 60.0, "PlayStation", 0),
                ("Divinity: Original Sin 2", "RPG", 45.0, "PC", 0),
                ("Pillars of Eternity", "RPG", 30.0, "PC", 0),
                ("Baldur's Gate 3", "RPG", 60.0, "PC", 0),
                ("Dragon Age: Inquisition", "RPG", 30.0, "PC", 0),
                ("Mass Effect Legendary Edition", "RPG", 60.0, "PC", 0),
                ("The Outer Worlds", "RPG", 60.0, "PC", 0),
                ("Fire Emblem: Three Houses", "RPG", 60.0, "Switch", 0),
                ("Octopath Traveler", "RPG", 60.0, "Switch", 0),
                ("Xenoblade Chronicles 3", "RPG", 60.0, "Switch", 0),
                ("Path of Exile", "RPG", 0.0, "PC", 0),
                ("Diablo III", "RPG", 40.0, "PC", 0),
                ("Monster Hunter Rise", "RPG", 40.0, "Switch", 0),
                ("Genshin Impact", "RPG", 5.0, "Mobile", 0),
                ("Pokémon Scarlet", "RPG", 60.0, "Switch", 0),
                ("Persona 4 Golden", "RPG", 20.0, "PC", 0),
                
                # Strategy games
                ("Civilization VI", "Strategy", 60.0, "PC", 0),
                ("Total War: Warhammer III", "Strategy", 60.0, "PC", 0),
                ("Age of Empires IV", "Strategy", 60.0, "PC", 0),
                ("Crusader Kings III", "Strategy", 50.0, "PC", 0),
                ("XCOM 2", "Strategy", 50.0, "PC", 0),
                ("Stellaris", "Strategy", 40.0, "PC", 0),
                ("Company of Heroes 3", "Strategy", 60.0, "PC", 0),
                ("Fire Emblem: Engage", "Strategy", 60.0, "Switch", 0),
                ("Into the Breach", "Strategy", 15.0, "PC", 0),
                ("Advance Wars 1+2", "Strategy", 60.0, "Switch", 0),
                ("Anno 1800", "Strategy", 40.0, "PC", 0),
                ("Northgard", "Strategy", 25.0, "PC", 0),
                ("Frostpunk", "Strategy", 30.0, "PC", 0),
                ("They Are Billions", "Strategy", 25.0, "PC", 0),
                ("Desperados III", "Strategy", 40.0, "PC", 0),
                
                # Indie games
                ("Cuphead", "Indie", 20.0, "PC", 0),
                ("Ori and the Blind Forest", "Indie", 20.0, "PC", 0),
                ("Hades", "Indie", 25.0, "Switch", 0),
                ("Bastion", "Indie", 15.0, "PC", 0),
                ("Transistor", "Indie", 20.0, "PC", 0),
                ("Limbo", "Indie", 10.0, "PC", 0),
                ("Inside", "Indie", 20.0, "PC", 0),
                ("Undertale", "Indie", 10.0, "PC", 0),
                ("Among Us", "Indie", 5.0, "Mobile", 0),
                ("Fall Guys", "Indie", 20.0, "PC", 0),
                ("Valheim", "Indie", 20.0, "PC", 0),
                ("Terraria", "Indie", 10.0, "PC", 0),
                ("Minecraft", "Indie", 27.0, "PC", 0),
                ("Slay the Spire", "Indie", 25.0, "PC", 0),
                ("Dead Cells", "Indie", 25.0, "Switch", 0),
                ("Gris", "Indie", 17.0, "PC", 0),
                ("A Short Hike", "Indie", 8.0, "PC", 0),
                ("What Remains of Edith Finch", "Indie", 20.0, "PC", 0),
                
                # Adventure games
                ("Life is Strange", "Adventure", 20.0, "PC", 0),
                ("The Walking Dead", "Adventure", 25.0, "PC", 0),
                ("Gone Home", "Adventure", 15.0, "PC", 0),
                ("Firewatch", "Adventure", 20.0, "PC", 0),
                ("Outer Wilds", "Adventure", 25.0, "PC", 0),
                ("The Talos Principle", "Adventure", 40.0, "PC", 0),
                ("Oxenfree", "Adventure", 10.0, "PC", 0),
                ("Night in the Woods", "Adventure", 20.0, "PC", 0),
                ("Samorost 3", "Adventure", 15.0, "PC", 0),
                ("Gorogoa", "Adventure", 15.0, "PC", 0),
                ("Kentucky Route Zero", "Adventure", 25.0, "PC", 0),
                ("Tacoma", "Adventure", 20.0, "PC", 0),
                ("Detroit: Become Human", "Adventure", 40.0, "PlayStation", 0),
                ("Heavy Rain", "Adventure", 20.0, "PlayStation", 0),
                ("Until Dawn", "Adventure", 20.0, "PlayStation", 0),
                
                # Shooter games
                ("Call of Duty: Modern Warfare", "Shooter", 60.0, "PC", 0),
                ("Counter-Strike 2", "Shooter", 0.0, "PC", 0),
                ("Valorant", "Shooter", 0.0, "PC", 0),
                ("Overwatch 2", "Shooter", 0.0, "PC", 0),
                ("Apex Legends", "Shooter", 0.0, "PC", 0),
                ("PUBG", "Shooter", 30.0, "PC", 0),
                ("Destiny 2", "Shooter", 0.0, "PC", 0),
                ("Borderlands 3", "Shooter", 60.0, "PC", 0),
                ("Titanfall 2", "Shooter", 30.0, "PC", 0),
                ("BioShock Infinite", "Shooter", 30.0, "PC", 0),
                ("DOOM (2016)", "Shooter", 20.0, "PC", 0),
                ("Wolfenstein II", "Shooter", 40.0, "PC", 0),
                ("Metro Exodus", "Shooter", 40.0, "PC", 0),
                ("S.T.A.L.K.E.R.: Shadow of Chernobyl", "Shooter", 10.0, "PC", 0),
                ("Insurgency: Sandstorm", "Shooter", 30.0, "PC", 0),
                
                # Simulation games
                ("Cities: Skylines", "Simulation", 30.0, "PC", 0),
                ("The Sims 4", "Simulation", 40.0, "PC", 0),
                ("Euro Truck Simulator 2", "Simulation", 20.0, "PC", 0),
                ("Farming Simulator 22", "Simulation", 40.0, "PC", 0),
                ("Planet Zoo", "Simulation", 45.0, "PC", 0),
                ("Two Point Hospital", "Simulation", 35.0, "PC", 0),
                ("Prison Architect", "Simulation", 30.0, "PC", 0),
                ("Kerbal Space Program", "Simulation", 40.0, "PC", 0),
                ("Factorio", "Simulation", 30.0, "PC", 0),
                ("RimWorld", "Simulation", 35.0, "PC", 0),
                ("Dwarf Fortress", "Simulation", 30.0, "PC", 0),
                ("Elite Dangerous", "Simulation", 30.0, "PC", 0),
                ("Microsoft Flight Simulator", "Simulation", 70.0, "PC", 0),
                ("Animal Crossing: New Horizons", "Simulation", 60.0, "Switch", 0),
                ("Harvest Moon", "Simulation", 50.0, "Switch", 0),
            ]
            
            cursor.executemany("""
                INSERT INTO products (name, category, price, platform, is_featured)
                VALUES (?, ?, ?, ?, ?)
            """, games)
            
            conn.commit()
            print(f"База данных инициализирована. Добавлено {len(games)} игр.")
    except Exception as e:
        print(f"Ошибка при инициализации БД: {e}")
        conn.rollback()
    finally:
        conn.close()


def get_all_products() -> List[Dict[str, Any]]:
    """Возвращает все игры из каталога."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products ORDER BY name")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def find_products_by_name(name: str) -> List[Dict[str, Any]]:
    """Поиск игр по частичному совпадению имени (LIKE)."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM products WHERE name LIKE ? ORDER BY name",
            (f"%{name}%",)
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def find_products_by_category(category: str) -> List[Dict[str, Any]]:
    """Поиск игр по жанру."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM products WHERE category = ? ORDER BY name",
            (category,)
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def find_products_by_platform(platform: str) -> List[Dict[str, Any]]:
    """Поиск игр по платформе."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM products WHERE platform = ? ORDER BY name",
            (platform,)
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def find_products_by_price_range(min_price: float, max_price: float) -> List[Dict[str, Any]]:
    """Поиск игр в диапазоне цен."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM products WHERE price >= ? AND price <= ? ORDER BY price",
            (min_price, max_price)
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def add_product(name: str, category: str, price: float, 
                platform: str, is_featured: int = 0) -> Dict[str, Any]:
    """
    Добавляет новую игру в каталог.
    Возвращает созданный объект игры.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO products (name, category, price, platform, is_featured)
            VALUES (?, ?, ?, ?, ?)
        """, (name, category, price, platform, is_featured))
        conn.commit()
        
        product_id = cursor.lastrowid
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        row = cursor.fetchone()
        return dict(row)
    except Exception as e:
        conn.rollback()
        raise ValueError(f"Ошибка при добавлении игры: {e}")
    finally:
        conn.close()


def get_featured_products() -> List[Dict[str, Any]]:
    """Возвращает список рекомендованных игр (is_featured = 1)."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM products WHERE is_featured = 1 ORDER BY name"
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def find_similar_products(base_name: str) -> List[Dict[str, Any]]:
    """
    Находит похожие игры на основе жанра и платформы базовой игры.
    Если игра не найдена, возвращает пустой список.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        # Сначала находим базовую игру
        cursor.execute(
            "SELECT * FROM products WHERE name LIKE ? LIMIT 1",
            (f"%{base_name}%",)
        )
        base_game = cursor.fetchone()
        
        if not base_game:
            return []
        
        base_dict = dict(base_game)
        category = base_dict["category"]
        platform = base_dict["platform"]
        base_id = base_dict["id"]
        
        # Ищем игры того же жанра и платформы, исключая саму игру
        cursor.execute("""
            SELECT * FROM products 
            WHERE (category = ? OR platform = ?) 
            AND id != ?
            ORDER BY name
            LIMIT 10
        """, (category, platform, base_id))
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

