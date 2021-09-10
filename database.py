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


class DatabaseQuiries:
    # UPDATE_USER = (
    #     "INSERT INTO chat_selections (id, number_of_replies) "
    #     "VALUES (%s, %s) "
    #     "ON CONFLICT (id) DO UPDATE "
    #     "SET number_of_replies = excluded.number_of_replies"
    # )
    # GET_NUMBER_OF_REPLIES = "SELECT number_of_replies FROM chat_selections WHERE id=%s"

    GET_CHARACTERS = """SELECT * FROM characters"""

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