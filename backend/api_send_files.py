from flask import Flask, Response
from werkzeug.utils import secure_filename
import pandas as pd
import io

app = Flask(__name__)

# Returns a modified excel file
@app.route('/receive-file',  methods=['GET'])
def download_file():
    # Read in file
    buffer = io.BytesIO()
    df = pd.read_excel('Sample TX Data.xlsx', header=0)

    # Modify file
    df["Fname"] = df["Fname"].astype(str).str.replace("A", "B")

    # Return the modified file
    try:
        df.to_excel(buffer)
        headers = {
            'Content-Disposition': 'attachment; filename=output.xlsx',
            'Content-type': 'application/vnd.ms-excel'
        }
        return Response(io.BytesIO(buffer.getvalue()), mimetype='application/vnd.ms-excel', headers=headers)
    finally:
        buffer.close()
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 8000, threaded = True, debug = True)