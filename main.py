import sys
sys.path.append('C:\FACULTATE\AN 3\Practica in Python\Tema1Cloud\venv\Lib\site-packages\requests')
import requests
import json
import sqlite3
import config


the_input = sys.argv[1]
# the_input = 'Luke'
id_global = 10900

conn = sqlite3.connect('.\logs.db')


def connect_to_database():
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS call_api_logs
                 (id integer PRIMARY KEY, request string, response text,running bool, response_time text)''')
    conn.commit()
    return conn


def close_database_connection():
    conn.close()


def get_unique_id():
    global id_global
    local_id = id_global
    id_global += 1
    return local_id


def log_api_call_running(id, endpoint):
    c = conn.cursor()
    id = get_last_id()
    c.execute(f"INSERT INTO call_api_logs (id, request) VALUES (?,?)", (id, endpoint))

    # Save (commit) the changes
    conn.commit()


def log_api_call_finished(id, response, results):
    c = conn.cursor()
    # print(type(results))
    # print(str(results))
    c.execute(f"UPDATE call_api_logs SET response = ?, response_time = ? WHERE id = ?", (str(results), str(response.elapsed), id))


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    # print(text)
    return text


def call_to_star_wars_api_people():
    request = "https://swapi.co/api/people"
    id = get_unique_id()
    log_api_call_running(id, request)
    response = requests.get(request)
    results_call = response.json()['results']
    log_api_call_finished(id, response, response.json())
    return results_call


def call_to_star_wars_api_film(endpoint):
    id = get_unique_id()
    log_api_call_running(id, endpoint)
    response = requests.get(endpoint)
    print(response)
    results_call = response.json()['director']
    log_api_call_finished(id, response, response.json())
    return results_call


def call_to_api_with_key(director):
    # STORE IT in a CONFIG file!!!!!!
    key = config.google_api_key
    endpoint = f'https://www.googleapis.com/customsearch/v1?key={key}&q=' + director
    id = get_unique_id()
    log_api_call_running(id, endpoint)
    response = requests.get(endpoint)
    results_call = ''
    try:
        results_call = response.json()['queries']
    except:
        results_call = response.json()['error']
    log_api_call_finished(id, response, response.json())
    print('<h4>The custom search on google, Queries: </h4>')
    print('<br>')
    print(results_call)
    print('<br><br>')


def search_the_name(persons):
    for res in persons: # search in results

        found = the_input in res['name']
        if found == True:
            print(f"<h2>His full name is: {res['name']}</h2>")
            print("<h2>The directories in the movies he played are: </h2>")
            for film in res['films']:
                print('<br>')
                print('<br>')
                print(film)
                director = call_to_star_wars_api_film(film)
                print(director)
                call_to_api_with_key(director)


def get_last_id():
    c = conn.cursor()
    c.execute('SELECT * FROM call_api_logs')
    all = c.fetchall()
    id = id_global
    if not all:
        id = id_global
    else:
        id = max(all, key=lambda x: x[0])[0]
    return id+1


c = conn.cursor()
# c.execute('DELETE FROM call_api_logs')
# c.execute('DROP TABLE call_api_logs')
id_global = get_last_id()
connect_to_database()
results = call_to_star_wars_api_people()
search_the_name(results)
c = conn.cursor()
c.execute('SELECT * FROM call_api_logs')
# print(c.fetchall())
close_database_connection()





