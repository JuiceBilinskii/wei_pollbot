import psycopg2
import configparser


def main():
    config = configparser.ConfigParser()
    config.read('../config.ini')
    db_config = config['PostgreSQL']

    sql_query = """
    CREATE TABLE users
    (
        id bigint PRIMARY KEY,
        first_name varchar(100) NOT NULL,
        username varchar(100) default NULL
    );
    
    CREATE TABLE characters
    (
        id serial PRIMARY KEY,
        name varchar(150) NOT NULL,
        height integer NOT NULL,
        short_description varchar(1000) NOT NULL,
        url varchar(100) NOT NULL
    );
    
    CREATE TABLE polls
    (
        id serial PRIMARY KEY,
        user_id bigint NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        date_completed timestamp NOT NULL,
        analysis_usage boolean NOT NULL default FALSE,
        concordance_factor real NOT NULL
    );
    
    CREATE TABLE answers
    (
        id serial PRIMARY KEY,
        poll_id integer NOT NULL REFERENCES polls(id) ON DELETE CASCADE,
        character_a_id integer NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
        character_b_id integer NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
        ratio_a_to_b real NOT NULL,
        UNIQUE (poll_id, character_a_id, character_b_id)
    )
    """

    # create_user_datatable_query = """
    #     CREATE TABLE users
    #     (
    #         id bigint PRIMARY KEY,
    #         first_name varchar(100) NOT NULL,
    #         username varchar(100) default NULL
    #     );
    #     """
    #
    # create_characters_datatable_query = """
    #     CREATE TABLE characters
    #     (
    #         id serial PRIMARY KEY,
    #         name varchar(150) NOT NULL,
    #         height integer NOT NULL,
    #         short_description varchar(1000) NOT NULL
    #     );
    #     """
    #
    # create_polls_datatable_query = """
    #     CREATE TABLE polls
    #     (
    #         id serial PRIMARY KEY,
    #         user_id bigint NOT NULL,
    #         date_completed timestamp NOT NULL,
    #         used_in_analysis boolean NOT NULL default FALSE,
    #         CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    #     );
    #     """
    #
    # create_answers_datatable_query = """
    #     CREATE TABLE answers
    #     (
    #         id serial PRIMARY KEY,
    #         poll_id integer,
    #         character_a_id integer,
    #         character_b_id integer,
    #         ratio_a_to_b real NOT NULL,
    #         UNIQUE (poll_id, character_a_id, character_b_id),
    #         CONSTRAINT fk_poll FOREIGN KEY(poll_id) REFERENCES polls(id) ON DELETE CASCADE,
    #         CONSTRAINT fk_character_a FOREIGN KEY(character_a_id) REFERENCES characters(id) ON DELETE CASCADE,
    #         CONSTRAINT fk_character_b FOREIGN KEY(character_b_id) REFERENCES characters(id) ON DELETE CASCADE
    #     );
    #     """

    try:
        connection = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password'],
        )
        print('Successful connection')
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection:
            connection.close()
            print('Close connection')


if __name__ == '__main__':
    main()
