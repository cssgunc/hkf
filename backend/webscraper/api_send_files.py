from flask import Flask, Response, request
import json
from webscraper import handle_queries, Query


app = Flask(__name__)

def parse_query(dict):
    return Query(dict['Fname'], dict['Lname'], dict['InmateID'], dict['PrisonName'], dict['ADD1'], dict['CITY'], dict['STATE'], dict['ZIP'])


# Returns a modified excel file
@app.route('/input',  methods=['post'])
def handle_input():
    input_str = request.form.get('data')
    parsed = json.loads(input_str)

    print("new input of len: ", len(parsed))

    queries = []
    for input in parsed:
        queries.append(parse_query(input))

    output = handle_queries(queries)

    response = Response(output, mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=data.csv'
    return response



if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 8000, threaded = True, debug = True)