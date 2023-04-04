import os
from flask import Flask, request, Response,send_file, jsonify, render_template

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download_excel():
    # Get the path of the Excel file
    file_path = os.path.join(os.getcwd(), "test.xlsx")
    # Set the output file's content type to Excel
    response = Response()
    response.headers['Content-Type'] = 'application/vnd.ms-excel'
    # Set the file name and attachment disposition
    response.headers['Content-Disposition'] = 'attachment; filename="test.xlsx"'
    # Open the file and read its contents
    with open(file_path, 'rb') as f:
        file_contents = f.read()
        response.set_data(file_contents)
    return response

if __name__ == '__main__':
    app.run()
