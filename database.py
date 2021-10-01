import psycopg2


class DatabaseConnection:
    def __init__(self, **kwargs):
        self.connection = psycopg2.connect(
            host=kwargs['host'],
            database=kwargs['database'],
            user=kwargs['user'],
            password=kwargs['password'],
        )

    def __enter__(self):
        return self.connection

    def __exit__(self, type, value, traceback):
        self.connection.close()
        return True


class DatabaseQueries:
    SELECT_CHARACTERS = """SELECT * FROM characters ORDER BY id ASC"""

    INSERT_USER_WITH_USERNAME = (
        "INSERT INTO users (id, first_name, username) "
        "VALUES (%s, %s, %s) "
        "ON CONFLICT (id) DO UPDATE "
        "SET first_name = excluded.first_name, username = excluded.username"
    )

    INSERT_POLL = (
        "INSERT INTO polls (user_id, date_completed, analysis_usage, concordance_factor) "
        "VALUES (%s, %s, %s, %s) RETURNING id;"
    )

    INSERT_ANSWERS = "INSERT INTO answers (poll_id, character_a_id, character_b_id, ratio_a_to_b) VALUES "

    INSERT_AVERAGE_CHARACTERS_RATING = "INSERT INTO average_characters_rating (poll_id, character_id, rating) VALUES "

    SELECT_POLLS_FROM_USER_WITH_ANALYSIS_USAGE = "SELECT * FROM polls WHERE user_id = %s AND analysis_usage = TRUE"

    def __init__(self, host, database, user, password):
        self.connect_information = {
            'host': host,
            'database': database,
            'user': user,
            'password': password,
        }

    def select_characters(self):
        with DatabaseConnection(**self.connect_information) as connection:
            with connection.cursor() as cursor:
                cursor.execute(self.SELECT_CHARACTERS)
                result = cursor.fetchall()
                return result
    
    def insert_user(self, _id, first_name, username=None):
        with DatabaseConnection(**self.connect_information) as connection:
            with connection.cursor() as cursor:
                cursor.execute(self.INSERT_USER_WITH_USERNAME, (_id, first_name, username))
                connection.commit()
    
    def insert_poll_answers_and_rating(self, poll_information, answers_list, characters_rating):
        with DatabaseConnection(**self.connect_information) as connection:
            with connection.cursor() as cursor:
                cursor.execute(self.INSERT_POLL, poll_information)
                poll_id = cursor.fetchone()[0]

                args = (cursor.mogrify("(%s, %s, %s, %s)", (poll_id, *x)).decode('utf-8') for x in answers_list)
                args_str = ','.join(args)
                cursor.execute(self.INSERT_ANSWERS + args_str)

                args = (cursor.mogrify("(%s, %s, %s)", (poll_id, character_id, rating)).decode('utf-8') for character_id, rating in characters_rating.items())
                args_str = ','.join(args)
                cursor.execute(self.INSERT_AVERAGE_CHARACTERS_RATING + args_str)

                connection.commit()

    def get_user_analysis_usage(self, user_id):
        with DatabaseConnection(**self.connect_information) as connection:
            with connection.cursor() as cursor:
                cursor.execute(self.SELECT_POLLS_FROM_USER_WITH_ANALYSIS_USAGE, (user_id, ))
                result = cursor.fetchone()

                return True if result is not None else False
