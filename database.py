import psycopg2


class Database:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
    
    def open_connection(self):
        try:
            conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
            )
            print('Database connection opened.')
            return conn
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False
    
    def close_connection(self, conn):
        if conn:
            conn.close()
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

    def get_characters_query(self):
        connection = self.database.open_connection()
        if connection:
            with connection.cursor() as cursor:
                cursor.execute(self.GET_CHARACTERS)
                result = cursor.fetchall()
        self.database.close_connection(connection)
        return result
    
    def insert_user_query(self, id, first_name, username=None):
        connection = self.database.open_connection()
        if connection:
            with connection.cursor() as cursor:
                cursor.execute(self.INSERT_USER_WITH_USERNAME, (id, first_name, username))
                connection.commit()
        self.database.close_connection(connection)
        return True
    
    def insert_poll_query(self, user_id, date_completed, used_in_analysis):
        connection = self.database.open_connection()
        if connection:
            with connection.cursor() as cursor:
                cursor.execute(self.INSERT_POLL, (user_id, date_completed, used_in_analysis))
                poll_id = cursor.fetchone()[0]
                connection.commit()
        self.database.close_connection(connection)
        return poll_id
    
    def inserts_answers_query(self, poll_id, answers_list):
        connection = self.database.open_connection()
        if connection:
            with connection.cursor() as cursor:
                args_str = ','.join((cursor.mogrify("(%s, %s, %s, %s)", (poll_id, *x))).decode('utf-8') for x in answers_list)
                cursor.execute(self.INSERT_ANSWERS + args_str)
                connection.commit()
        self.database.close_connection(connection)
        return True
