import sqlite3


def db_connect(query):
    """Функция возвращает результат запроса к базе данных"""
    with sqlite3.connect('netflix.db') as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def get_actors(name1, name2):
    """Функция по 5му шагу ДЗ"""
    query = f"""
        SELECT `cast`
        FROM netflix
        WHERE `cast` LIKE '%{name1}%' 
        AND `cast` LIKE '%{name2}%'
    """
    response = db_connect(query)
    actors = []
    for cast in response:
        actors.extend(cast[0].split(', '))

    result = []
    for actor in actors:
        if actor not in [name1, name2]:
            if actors.count(actor) > 2:
                result.append(actor)
    result = set(result)
    return result


def get_movies(type, year, genre):
    """Функция по 6му шагу ДЗ"""
    query = f"""
        SELECT title, description
        FROM netflix
        WHERE release_year={year} 
        AND type='{type}'
        AND listed_in LIKE '%{genre}%'
    """
    response = db_connect(query)
    result_json = []
    for row in response:
        result_json.append({
            'title': row[0],
            'description': row[1]
        })

    return result_json


print(get_movies('TV Show', 2010, 'Dramas'))
