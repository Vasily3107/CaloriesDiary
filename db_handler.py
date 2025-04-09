from pyodbc import connect as connect_to_db
server   = 'localhost\SQLEXPRESS'
database = 'test_db'
dsn      =f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

class DBHandler:
    '''
    SQL database utility class
    '''
    @staticmethod
    def __find_user(email:str):
        conn = connect_to_db(dsn)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()
        return bool(row)

    @staticmethod
    def log_in(email:str, password:str) -> bool:
        '''
        True  : success
        False : failure (user does not exist)
        '''
        conn = connect_to_db(dsn)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE email = ? AND [password] = ?', (email, password))
        row = cursor.fetchone()

        cursor.close()
        conn.close()
        return bool(row)

    @staticmethod
    def update_user_info(email:str, sex:str, age:int, weight:int, height:int, goal:str) -> None:
        conn = connect_to_db(dsn)
        cursor = conn.cursor()

        cursor.execute('UPDATE users SET sex = ?, age = ?, weight = ?, height = ?, goal = ? WHERE email = ?',
                       (sex, age, weight, height, goal, email))
        conn.commit()

        cursor.close()
        conn.close()

    @staticmethod
    def sign_up(email:str, password:str, sex:str, age:int, weight:int, height:int, goal:str) -> bool:
        '''
        True  : success
        False : failure (user already exist)
        '''
        conn = connect_to_db(dsn)
        cursor = conn.cursor()

        if DBHandler.__find_user(email):
            return False

        cursor.execute('INSERT INTO users VALUES (?, ?, DEFAULT, DEFAULT, ?, ?, ?, ?, ?)',
                       (email, password, sex, age, weight, height, goal))
        conn.commit()

        cursor.close()
        conn.close()
        return True

    @staticmethod
    def get_user_info(email:str) -> tuple:
        '''
        returns tuple(calories_score, goals_achieved, sex, age, weight, height, goal)
        '''
        conn = connect_to_db(dsn)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        info = tuple(cursor.fetchone())[2:]

        cursor.close()
        conn.close()
        return info

    @staticmethod
    def add_meal(email:str, name:str, calories:int) -> None:
        conn = connect_to_db(dsn)
        cursor = conn.cursor()

        cursor.execute('INSERT INTO meals VALUES (?, ?, ?, DEFAULT)', (email, name, calories))
        conn.commit()

        cursor.close()
        conn.close()

    @staticmethod
    def meal_iter(email:str):
        '''
        yields tuple(name, calories, time)
        '''
        conn = connect_to_db(dsn)
        cursor = conn.cursor()

        cursor.execute('SELECT [name], calories, [when] FROM meals WHERE email = ?', (email,))
        try:
            for row in cursor: yield tuple(row)

        except StopIteration:
            cursor.close()
            conn.close()

    @staticmethod
    def add_activity(email:str, name:str, calories:int) -> None:
        conn = connect_to_db(dsn)
        cursor = conn.cursor()

        cursor.execute('INSERT INTO activities VALUES (?, ?, ?, DEFAULT)', (email, name, calories))
        conn.commit()

        cursor.close()
        conn.close()

    @staticmethod
    def activity_iter(email:str):
        '''
        yields tuple(name, calories, time)
        '''
        conn = connect_to_db(dsn)
        cursor = conn.cursor()

        cursor.execute('SELECT [name], calories, [when] FROM activities WHERE email = ?', (email,))
        try:
            for row in cursor: yield tuple(row)

        except StopIteration:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_user_data(email:str):
        conn = connect_to_db(dsn)
        cursor = conn.cursor()

        cursor.execute('UPDATE users SET calories_score = 0, goals_achieved = 0 WHERE email = ?', (email,))
        cursor.execute('DELETE FROM meals WHERE email = ?', (email,))
        cursor.execute('DELETE FROM activities WHERE email = ?', (email,))
        conn.commit()

        cursor.close()
        conn.close()

    @staticmethod
    def update_user_scores(calories_score:int, email:str) -> None:
        conn = connect_to_db(dsn)
        cursor = conn.cursor()

        cursor.execute('UPDATE users SET calories_score = ?, goals_achieved += 1 WHERE email = ?', (calories_score, email))
        conn.commit()

        cursor.close()
        conn.close()
