from threading import Thread
from scraper import Scraper
from query import Query, PrisonMatch

from flask import Flask, Response, request
import json

scraper = Scraper()

app = Flask(__name__)

def parse_query(dict):
    return Query.create(dict['Fname'], dict['Lname'], dict['InmateID'], dict['PrisonName'], dict['ADD1'], dict['CITY'], dict['STATE'], dict['ZIP'])

@app.route('/input',  methods=['post'])
def handle_input():
    input_str = request.form.get('data')
    parsed = json.loads(input_str)

    print("new input of len: ", len(parsed))

    queries = [None] * len(parsed)
    threads = []

    def process_query(i, query):
        queries[i] = scraper.query(query)
    for i in range(len(parsed)):
        thread = Thread(target=process_query, args=(i, parse_query(parsed[i])))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
    
    for i in range(len(parsed)):
        if len(queries[i])==0:
            parsed[i].update(PrisonMatch.serialize(PrisonMatch.blank()))
        else:
            parsed[i].update(PrisonMatch.serialize(queries[i][0]))


    out = json.dumps(parsed)
    response = Response(out, mimetype='application/json')
    return response



if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 8000, threaded = True, debug = True, use_reloader=False)

