import psycopg2


class Database:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

        self.connection = None
    
    def open_connection(self):
        self.connection = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password,
        )
        print('Database connection opened.')
        return True
    
    def close_connection(self):
        if self.connection:
            self.connection.close()
            print('Database connection closed.')
        return True


class DatabaseQueries:
    GET_CHARACTERS = """SELECT * FROM characters"""
    INSERT_USER_WITH_USERNAME = (
        "INSERT INTO users (id, first_name, username) "
        "VALUES (%s, %s, %s) "
        "ON CONFLICT (id) DO UPDATE "
        "SET first_name = excluded.first_name, username = excluded.username"
    )
    INSERT_USER = (
        "INSERT INTO users (id, first_name) "
        "VALUES (%s, %s) "
        "ON CONFLICT (id) DO UPDATE "
        "SET first_name = excluded.first_name"
    )
    INSERT_POLL = (
        "INSERT INTO polls (user_id, date_completed, used_in_analysis) "
        "VALUES (%s, %s, %s) RETURNING id;"
    )
    INSERT_ANSWERS = "INSERT INTO answers (poll_id, character_a_id, character_b_id, ratio_a_to_b) VALUES "

    def __init__(self, host, database, user, password):
        self.database = Database(host, database, user, password)

    def select_characters(self):
        if self.database.open_connection():
            with self.database.connection.cursor() as cursor:
                cursor.execute(self.GET_CHARACTERS)
                result = cursor.fetchall()
        self.database.close_connection()
        return result
    
    def insert_user(self, _id, first_name, username=None):
        if self.database.open_connection():
            with self.database.connection.cursor() as cursor:
                cursor.execute(self.INSERT_USER_WITH_USERNAME, (_id, first_name, username))
                self.database.connection.commit()
        self.database.close_connection()
        return True
    
    def insert_poll_and_answers(self, poll_information, answers_list):
        if self.database.open_connection():
            with self.database.connection.cursor() as cursor:
                cursor.execute(self.INSERT_POLL, poll_information)
                poll_id = cursor.fetchone()[0]

                args = (cursor.mogrify("(%s, %s, %s, %s)", (poll_id, *x)).decode('utf-8') for x in answers_list)
                args_str = ','.join(args)

                cursor.execute(self.INSERT_ANSWERS + args_str)
                self.database.connection.commit()
        self.database.close_connection()
        return True
