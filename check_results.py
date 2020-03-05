import requests
import sqlite3
conn = sqlite3.connect('.\logs.db')
c = conn.cursor()

c.execute('SELECT * FROM call_api_logs')
queries = c.fetchall()
for i in queries:
    print(i)

print()
print()
print()
for l in list(map(lambda x: (x[1], x[4]), queries)):
    print(l)

#CONCLUZII: un request la swapi dureaza de 2, 3 ori mai mult timp decat unul la google aprox 0.6
# #Google: 0:00:00.165752
# #Swapi -people 0:00:00.659200
# #Swapi - films/7 0:00:00.563665
# Din pacate cand am rulat scriptul cu 500 de requesturi.. a picat api de la swapi
# Iar la google custom search esti limitat de 100 de requesturi pe zi
# Finalized all 481 requests.
# Took 61.21520686149597 seconds to pull 481 websites.
