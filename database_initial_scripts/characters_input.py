import psycopg2
import configparser
import json


def main():
    with open('../characters.json', 'r', encoding='utf8') as file:
        characters = json.load(file)
    
    # for character in characters['characters']:
    #     print(character)
    
    config = configparser.ConfigParser()
    config.read('../config.ini')
    db_config = config['PostgreSQL']

    insert_character_query = """
    INSERT INTO characters (name, height, short_description) VALUES (%s, %s, %s);
    """

    try:
        connection = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password'],
        )
        print('Successfull connection')
        with connection.cursor() as cursor:
            for character in characters['characters']:
                cursor.execute(insert_character_query, (character['name'], character['height'], character['short_description']))
            connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection:
            connection.close()
            print('Close connection')


if __name__ == '__main__':
    main()
