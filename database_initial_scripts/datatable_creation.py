import psycopg2
import configparser


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    db_config = config['PostgreSQL']

    create_user_datatable_query = """
        CREATE TABLE users
        (
            id bigint PRIMARY KEY,
            first_name varchar(100) NOT NULL,
            username varchar(100) default NULL
        );
        """

    create_characters_datatable_query = """
        CREATE TABLE characters
        (
            id serial PRIMARY KEY,
            name varchar(150) NOT NULL,
            height integer NOT NULL,
            short_description varchar(250) NOT NULL
        );
        """

    create_polls_datatable_query = """
        CREATE TABLE polls
        (
            id serial PRIMARY KEY,
            user_id bigint REFERENCES users(id) ON DELETE CASCADE,
            date_completed timestamp default NULL,
            used_in_analysis boolean default FALSE
        );
        """

    create_answers_datatable_query = """
        CREATE TABLE answers
        (
            id serial PRIMARY KEY,
            poll_id integer REFERENCES polls(id) ON DELETE CASCADE,
            character_a_id integer REFERENCES characters(id) ON DELETE CASCADE,
            character_b_id integer REFERENCES characters(id) ON DELETE CASCADE,
            ratio_a_to_b real NOT NULL,
            UNIQUE (poll_id, character_a_id, character_b_id)
        );
        """

    try:
        connection = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password'],
        )
        print('Successful connection')
        with connection.cursor() as cursor:
            cursor.execute(create_user_datatable_query)
            cursor.execute(create_characters_datatable_query)
            cursor.execute(create_polls_datatable_query)
            cursor.execute(create_answers_datatable_query)
            connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection:
            connection.close()
            print('Close connection')


if __name__ == '__main__':
    main()
