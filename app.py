from flask import Flask, jsonify
from utils import db_connect

app = Flask(__name__)


@app.route('/')
def index_page():
    return """
        <h2>Hello, this is the main page</h2>
    """


@app.route('/movie/<title>')
def search_by_title(title):
    query = f"""
        SELECT title, country, release_year, listed_in AS genre, description
        FROM netflix
        WHERE title='{title}'
        ORDER BY release_year DESC 
        LIMIT 1
    """
    result = db_connect(query)[0]
    response_json = {
        'title': result[0],
        'country': result[1],
        'release_year': result[2],
        'genre': result[3],
        'description': result[4],
    }
    return jsonify(response_json)


@app.route('/movie/<int:year1>/to/<int:year2>/')
def search_by_release_year(year1, year2):
    query = f"""
        SELECT title, release_year
        FROM netflix
        WHERE release_year BETWEEN {year1} AND {year2}
        ORDER BY release_year
        LIMIT 100
    """
    result = db_connect(query)
    response_json = []
    for file in result:
        response_json.append({
            'title': file[0],
            'release_year': file[1],
        })
    return jsonify(response_json)


@app.route('/rating/<group>')
def search_by_group(group):
    levels = {
        'children': ['G'],
        'family': ['G', 'PG', 'PG-13'],
        'adult': ['R', 'NC-17'],
    }

    if group in levels:
        level = '\", \"'.join(levels[group])
        level = f'\"{level}\"'
    else:
        return jsonify([])

    query = f"""
        SELECT title, rating, description
        FROM netflix
        WHERE rating IN ({level})
        
    """

    result = db_connect(query)
    response_json = []
    for file in result:
        response_json.append({
            'title': file[0],
            'rating': file[1],
            'description': file[2],
        })
    return jsonify(response_json)


@app.route('/genre/<genre>')
def search_by_genre(genre):
    query = f"""
        SELECT title,  
        description       
        FROM netflix
        WHERE listed_in LIKE '%{genre}%'
        ORDER BY release_year DESC
        LIMIT 10
    """

    result = db_connect(query)
    response_json = []
    for file in result:
        response_json.append({
            'title': file[0],
            'description': file[1]
        })
    return jsonify(response_json)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
