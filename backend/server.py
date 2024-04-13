from threading import Thread
from scraper import Scraper
from query import Query, PrisonMatch
import os
import traceback

from flask import Flask, Response, request
from flask_cors import CORS
import json

scraper = Scraper()

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

def parse_query(dict):
    return Query.create(dict['Fname'], dict['Lname'], dict['InmateID'], dict['PrisonName'], dict['ADD1'], dict['CITY'], dict['STATE'], dict['ZIP'])

@app.route('/input',  methods=['post'])
def handle_input():
    input_str = request.form.get('data')
    parsed = json.loads(input_str)

    print("new input of len: ", len(parsed))
    print('Scraper', scraper)

    queries = [None] * len(parsed)
    threads = []

    def process_query(i, query):
        try:
            iters = 0
            while queries[i] is None:
                try:
                    queries[i] = scraper.query(query)
                    break
                except:
                    iters += 1
                if iters > 10:
                    break
        except:
            if i == 0:
                traceback.print_exc()
        
    for i in range(len(parsed)):
        thread = Thread(target=process_query, args=(i, parse_query(parsed[i])))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
    print('Queries', queries)
    for i in range(len(parsed)):
        if len(queries[i])==0:
            parsed[i].update(PrisonMatch.serialize(PrisonMatch.blank()))
        else:
            parsed[i].update(PrisonMatch.serialize(queries[i][0]))


    out = json.dumps(parsed)
    response = Response(out, mimetype='application/json')
    print('Response', response)
    return response



if __name__ == '__main__':
    app.run(port=os.getenv("PORT", default=5000), threaded = True, debug = True, use_reloader=False)

