import sqlite3

"""Создание класса БД"""
class DataBase():
    def __init__(self, db_name): # Конструктор класса БД
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()
        
    def create_table(self): # создание таблицы БД если ее нет
        try:
            query = ("CREATE TABLE IF NOT EXISTS users("
                     "id INTEGER PRIMARY KEY,"
                     "tg_user_id TEXT UNIQUE,"
                     "city TEXT);")
            self.cursor.execute(query)
            self.conn.commit()
        except sqlite3.Error as Error:
            print(f"Ошибка при создании таблицы БД {Error}")
        
    def check_user(self, user_id): # Проверка наличия пользователя в БД
        result = self.cursor.execute("SELECT id FROM users WHERE tg_user_id = ?", (user_id,))
        user = result.fetchone()
        if user:
            return user[0]  
        else:
            return None  

    def add_user(self, user_id): # Добавление пользователя в БД
        self.cursor.execute("INSERT INTO users (tg_user_id) VALUES (?)", (user_id,))
        self.conn.commit()
        
    def check_city(self, user_id): # Проверка наличия города (у пользователя) в БД
        result = self.cursor.execute("SELECT city FROM users WHERE tg_user_id = ?", (user_id,))
        user = result.fetchone()
        if user:
            return user[0]  
        else:
            return None  
    
    def add_city(self, city, user_id): # Добавление города (пользователю) в БД
        self.cursor.execute("UPDATE users SET city = ? WHERE tg_user_id = ?", (city, user_id,))
        self.conn.commit()
        
    def delete_city(self, city, user_id): # Удаление города (у пользователя) из БД
        self.cursor.execute("UPDATE users SET city = NULL WHERE city = ? AND tg_user_id = ?", (city, user_id,))
        self.conn.commit()
            
    def __del__(self): # Деконструктор
        if self.conn:
            self.cursor.close()
            self.conn.close()