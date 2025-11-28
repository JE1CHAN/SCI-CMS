import sqlite3

class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()
        self.check_and_migrate()

    def create_table(self):
        """Creates the database table if it doesn't exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS concerns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT,
                student_name TEXT,
                category TEXT,
                concern_details TEXT,
                date_filed TEXT,
                status TEXT,
                is_anonymous INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    def check_and_migrate(self):
        """Checks if the is_anonymous column exists, adds it if not (Migration)."""
        try:
            self.cursor.execute("SELECT is_anonymous FROM concerns LIMIT 1")
        except sqlite3.OperationalError:
            # Column doesn't exist, so we add it
            self.cursor.execute("ALTER TABLE concerns ADD COLUMN is_anonymous INTEGER DEFAULT 0")
            self.conn.commit()

    def insert(self, student_id, student_name, category, concern_details, date_filed, status, is_anonymous):
        """Inserts a new record into the database."""
        self.cursor.execute("INSERT INTO concerns (student_id, student_name, category, concern_details, date_filed, status, is_anonymous) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (student_id, student_name, category, concern_details, date_filed, status, is_anonymous))
        self.conn.commit()

    def fetch_all(self):
        """Fetches all records for the list view."""
        self.cursor.execute("SELECT id, student_id, student_name, category, date_filed, status, is_anonymous FROM concerns")
        return self.cursor.fetchall()

    def search(self, term):
        """Searches for records by name or student ID."""
        query = "SELECT id, student_id, student_name, category, date_filed, status, is_anonymous FROM concerns WHERE student_name LIKE ? OR student_id LIKE ?"
        self.cursor.execute(query, ('%' + term + '%', '%' + term + '%'))
        return self.cursor.fetchall()

    def fetch_details(self, record_id):
        """Fetches the full details (including the text block) for a specific ID."""
        self.cursor.execute("SELECT concern_details, is_anonymous FROM concerns WHERE id=?", (record_id,))
        return self.cursor.fetchone()

    def update(self, record_id, student_id, student_name, category, concern_details, status, is_anonymous):
        """Updates an existing record."""
        self.cursor.execute("""
            UPDATE concerns 
            SET student_id=?, student_name=?, category=?, concern_details=?, status=?, is_anonymous=?
            WHERE id=?
        """, (student_id, student_name, category, concern_details, status, is_anonymous, record_id))
        self.conn.commit()

    def delete(self, record_id):
        """Deletes a record by ID."""
        self.cursor.execute("DELETE FROM concerns WHERE id=?", (record_id,))
        self.conn.commit()

    def __del__(self):
        """Closes the connection when the object is destroyed."""
        self.conn.close()