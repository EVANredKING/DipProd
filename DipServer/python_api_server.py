import http.server
import json
import sqlite3
import socketserver
from urllib.parse import urlparse, parse_qs

PORT = 8081

class APIHandler(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        # Добавляем заголовки CORS для всех ответов
        self.send_cors_headers()
        
        if parsed_path.path == "/api/nomenclatures":
            self.handle_get_nomenclatures()
        elif parsed_path.path.startswith("/api/nomenclatures/"):
            nomenclature_id = parsed_path.path.split("/")[-1]
            self.handle_get_nomenclature(nomenclature_id)
        elif parsed_path.path == "/api/lsi":
            self.handle_get_lsi()
        elif parsed_path.path.startswith("/api/lsi/"):
            lsi_id = parsed_path.path.split("/")[-1]
            self.handle_get_lsi_item(lsi_id)
        elif parsed_path.path == "/api/users":
            self.handle_get_users()
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode())
    
    def do_POST(self):
        parsed_path = urlparse(self.path)
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("utf-8")
        
        # Добавляем заголовки CORS для всех ответов
        self.send_cors_headers()
        
        try:
            data = json.loads(post_data)
            
            if parsed_path.path == "/api/nomenclatures":
                self.handle_create_nomenclature(data)
            elif parsed_path.path == "/api/lsi":
                self.handle_create_lsi(data)
            elif parsed_path.path == "/api/users":
                self.handle_post_user(data)
            else:
                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode())
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid JSON format"}).encode())
    
    def do_PUT(self):
        parsed_path = urlparse(self.path)
        content_length = int(self.headers["Content-Length"])
        put_data = self.rfile.read(content_length).decode("utf-8")
        
        # Добавляем заголовки CORS для всех ответов
        self.send_cors_headers()
        
        try:
            data = json.loads(put_data)
            
            if parsed_path.path.startswith("/api/nomenclatures/"):
                nomenclature_id = parsed_path.path.split("/")[-1]
                self.handle_update_nomenclature(nomenclature_id, data)
            elif parsed_path.path.startswith("/api/lsi/"):
                lsi_id = parsed_path.path.split("/")[-1]
                self.handle_update_lsi(lsi_id, data)
            elif parsed_path.path.startswith("/api/users/"):
                user_id = parsed_path.path.split("/")[-1]
                self.handle_update_user(user_id, data)
            else:
                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode())
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid JSON format"}).encode())
    
    def do_DELETE(self):
        parsed_path = urlparse(self.path)
        
        # Добавляем заголовки CORS для всех ответов
        self.send_cors_headers()
        
        if parsed_path.path.startswith("/api/nomenclatures/"):
            nomenclature_id = parsed_path.path.split("/")[-1]
            self.handle_delete_nomenclature(nomenclature_id)
        elif parsed_path.path.startswith("/api/lsi/"):
            lsi_id = parsed_path.path.split("/")[-1]
            self.handle_delete_lsi(lsi_id)
        elif parsed_path.path.startswith("/api/users/"):
            user_id = parsed_path.path.split("/")[-1]
            self.handle_delete_user(user_id)
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode())
    
    def do_OPTIONS(self):
        self.send_cors_headers()
        self.end_headers()
    
    def send_cors_headers(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
    
    def init_database(self):
        """
        Инициализация БД при запуске сервера, создание необходимых таблиц
        """
        conn = sqlite3.connect("/app/database.db")
        cursor = conn.cursor()
        
        # Создаем таблицу пользователей, если она не существует
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            email TEXT,
            password TEXT
        )
        ''')
        
        # Создаем таблицу номенклатуры, если она не существует
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS nomenclatures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            code TEXT
        )
        ''')
        
        # Создаем таблицу ЛСИ, если она не существует
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS lsi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            level INTEGER,
            code TEXT,
            parent_id INTEGER
        )
        ''')
        
        conn.commit()
        conn.close()
    
    # Обработчики для номенклатуры
    def handle_get_nomenclatures(self):
        conn = sqlite3.connect("/app/database.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM nomenclatures")
        nomenclatures = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        # Расширяем данные номенклатуры для совместимости с Django ORM
        for item in nomenclatures:
            item['pk'] = item['id']
            # Добавляем все необходимые поля из модели Django
            if 'abbreviation' not in item:
                item['abbreviation'] = item.get('name', '').split(' ')[0] if item.get('name') else ''
            if 'short_name' not in item:
                item['short_name'] = item.get('name', '')
            if 'full_name' not in item:
                item['full_name'] = item.get('description', '')
            if 'internal_code' not in item:
                item['internal_code'] = item.get('code', '')
            if 'cipher' not in item:
                item['cipher'] = ''
            if 'ekps_code' not in item:
                item['ekps_code'] = ''
            if 'kvt_code' not in item:
                item['kvt_code'] = ''
            if 'drawing_number' not in item:
                item['drawing_number'] = ''
            if 'type_of_nomenclature' not in item:
                item['type_of_nomenclature'] = ''
        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"nomenclatures": nomenclatures}).encode())
    
    def handle_get_nomenclature(self, nomenclature_id):
        conn = sqlite3.connect("/app/database.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM nomenclatures WHERE id = ?", (nomenclature_id,))
        nomenclature = cursor.fetchone()
        conn.close()
        
        if nomenclature:
            nomenclature_dict = dict(nomenclature)
            # Добавляем pk и все необходимые поля для совместимости с Django ORM
            nomenclature_dict['pk'] = nomenclature_dict['id']
            if 'abbreviation' not in nomenclature_dict:
                nomenclature_dict['abbreviation'] = nomenclature_dict.get('name', '').split(' ')[0] if nomenclature_dict.get('name') else ''
            if 'short_name' not in nomenclature_dict:
                nomenclature_dict['short_name'] = nomenclature_dict.get('name', '')
            if 'full_name' not in nomenclature_dict:
                nomenclature_dict['full_name'] = nomenclature_dict.get('description', '')
            if 'internal_code' not in nomenclature_dict:
                nomenclature_dict['internal_code'] = nomenclature_dict.get('code', '')
            if 'cipher' not in nomenclature_dict:
                nomenclature_dict['cipher'] = ''
            if 'ekps_code' not in nomenclature_dict:
                nomenclature_dict['ekps_code'] = ''
            if 'kvt_code' not in nomenclature_dict:
                nomenclature_dict['kvt_code'] = ''
            if 'drawing_number' not in nomenclature_dict:
                nomenclature_dict['drawing_number'] = ''
            if 'type_of_nomenclature' not in nomenclature_dict:
                nomenclature_dict['type_of_nomenclature'] = ''
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(nomenclature_dict).encode())
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Nomenclature not found"}).encode())
    
    def handle_create_nomenclature(self, data):
        conn = sqlite3.connect("/app/database.db")
        cursor = conn.cursor()
        
        name = data.get("name", "")
        description = data.get("description", "")
        code = data.get("code", "")
        
        cursor.execute(
            "INSERT INTO nomenclatures (name, description, code) VALUES (?, ?, ?)",
            (name, description, code)
        )
        nomenclature_id = cursor.lastrowid
        conn.commit()
        
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM nomenclatures WHERE id = ?", (nomenclature_id,))
        new_nomenclature = dict(cursor.fetchone())
        conn.close()
        
        self.send_response(201)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(new_nomenclature).encode())
    
    def handle_update_nomenclature(self, nomenclature_id, data):
        conn = sqlite3.connect("/app/database.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM nomenclatures WHERE id = ?", (nomenclature_id,))
        nomenclature = cursor.fetchone()
        
        if nomenclature:
            name = data.get("name", "")
            description = data.get("description", "")
            code = data.get("code", "")
            
            cursor.execute(
                "UPDATE nomenclatures SET name = ?, description = ?, code = ? WHERE id = ?",
                (name, description, code, nomenclature_id)
            )
            conn.commit()
            
            cursor.execute("SELECT * FROM nomenclatures WHERE id = ?", (nomenclature_id,))
            updated_nomenclature = dict(cursor.fetchone())
            conn.close()
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(updated_nomenclature).encode())
        else:
            conn.close()
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Nomenclature not found"}).encode())
    
    def handle_delete_nomenclature(self, nomenclature_id):
        conn = sqlite3.connect("/app/database.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM nomenclatures WHERE id = ?", (nomenclature_id,))
        nomenclature = cursor.fetchone()
        
        if nomenclature:
            cursor.execute("DELETE FROM nomenclatures WHERE id = ?", (nomenclature_id,))
            conn.commit()
            conn.close()
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode())
        else:
            conn.close()
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Nomenclature not found"}).encode())
    
    # Обработчики для ЛСИ
    def handle_get_lsi(self):
        conn = sqlite3.connect("/app/database.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM lsi")
        lsi_items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"lsi_items": lsi_items}).encode())
    
    def handle_get_lsi_item(self, lsi_id):
        conn = sqlite3.connect("/app/database.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM lsi WHERE id = ?", (lsi_id,))
        lsi = cursor.fetchone()
        conn.close()
        
        if lsi:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(dict(lsi)).encode())
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "LSI not found"}).encode())
    
    def handle_create_lsi(self, data):
        conn = sqlite3.connect("/app/database.db")
        cursor = conn.cursor()
        
        name = data.get("name", "")
        level = data.get("level", 0)
        code = data.get("code", "")
        parent_id = data.get("parentId")
        
        cursor.execute(
            "INSERT INTO lsi (name, level, code, parent_id) VALUES (?, ?, ?, ?)",
            (name, level, code, parent_id)
        )
        lsi_id = cursor.lastrowid
        conn.commit()
        
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM lsi WHERE id = ?", (lsi_id,))
        new_lsi = dict(cursor.fetchone())
        conn.close()
        
        self.send_response(201)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(new_lsi).encode())
    
    def handle_update_lsi(self, lsi_id, data):
        conn = sqlite3.connect("/app/database.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM lsi WHERE id = ?", (lsi_id,))
        lsi = cursor.fetchone()
        
        if lsi:
            name = data.get("name", "")
            level = data.get("level", 0)
            code = data.get("code", "")
            parent_id = data.get("parentId")
            
            cursor.execute(
                "UPDATE lsi SET name = ?, level = ?, code = ?, parent_id = ? WHERE id = ?",
                (name, level, code, parent_id, lsi_id)
            )
            conn.commit()
            
            cursor.execute("SELECT * FROM lsi WHERE id = ?", (lsi_id,))
            updated_lsi = dict(cursor.fetchone())
            conn.close()
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(updated_lsi).encode())
        else:
            conn.close()
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "LSI not found"}).encode())
    
    def handle_delete_lsi(self, lsi_id):
        conn = sqlite3.connect("/app/database.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM lsi WHERE id = ?", (lsi_id,))
        lsi = cursor.fetchone()
        
        if lsi:
            cursor.execute("DELETE FROM lsi WHERE id = ?", (lsi_id,))
            conn.commit()
            conn.close()
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode())
        else:
            conn.close()
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "LSI not found"}).encode())
    
    # Обработчики для пользователей
    def handle_get_users(self):
        conn = sqlite3.connect("/app/database.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"users": users}).encode())
        
    def handle_post_user(self, data):
        conn = sqlite3.connect("/app/database.db")
        cursor = conn.cursor()
        
        username = data.get("username", "")
        email = data.get("email", "")
        password = data.get("password", "password123")
        
        if not username or not email:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Username and email are required"}).encode())
            conn.close()
            return
        
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, password)
        )
        user_id = cursor.lastrowid
        conn.commit()
        
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        new_user = dict(cursor.fetchone())
        conn.close()
        
        self.send_response(201)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(new_user).encode())
        
    def handle_update_user(self, user_id, data):
        conn = sqlite3.connect("/app/database.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "User not found"}).encode())
            conn.close()
            return
        
        username = data.get("username", user["username"])
        email = data.get("email", user["email"])
        
        # Обновляем пароль только если он был предоставлен
        if "password" in data and data["password"]:
            password = data["password"]
            cursor.execute(
                "UPDATE users SET username = ?, email = ?, password = ? WHERE id = ?",
                (username, email, password, user_id)
            )
        else:
            cursor.execute(
                "UPDATE users SET username = ?, email = ? WHERE id = ?",
                (username, email, user_id)
            )
            
        conn.commit()
        
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        updated_user = dict(cursor.fetchone())
        conn.close()
        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(updated_user).encode())
        
    def handle_delete_user(self, user_id):
        conn = sqlite3.connect("/app/database.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "User not found"}).encode())
            conn.close()
            return
        
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"success": True}).encode())

if __name__ == "__main__":
    # Инициализируем базу данных перед запуском сервера
    # Создаем соединение с базой данных и инициализируем таблицы
    conn = sqlite3.connect("/app/database.db")
    cursor = conn.cursor()
    
    # Создаем таблицу пользователей, если она не существует
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        email TEXT,
        password TEXT
    )
    ''')
    
    # Создаем таблицу номенклатуры, если она не существует
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS nomenclatures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        code TEXT
    )
    ''')
    
    # Создаем таблицу ЛСИ, если она не существует
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS lsi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        level INTEGER,
        code TEXT,
        parent_id INTEGER
    )
    ''')
    
    conn.commit()
    conn.close()
    
    print(f"Инициализация базы данных завершена")
    
    # Запускаем сервер
    with socketserver.TCPServer(("", PORT), APIHandler) as httpd:
        print(f"Server started at http://localhost:{PORT}")
        httpd.serve_forever() 