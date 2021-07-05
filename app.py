from flask import Flask, json, jsonify, request 
from pdfExtract import create_json
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'PDF Extaction APP<br>http://192.168.0.43:8089/pdf/1<br>http://192.168.0.43:8089/getFile'

@app.route('/pdf/<int:n>')
def pdf(n):
    json1 = create_json()
    result = {
        "Number": n,
        "Table": json1
    }
    return jsonify(result)

@app.route('/getFile', methods=['POST'])
def predict():
    # Catch the image file from a POST request
    if 'file' not in request.files:
        return "Please try again. The Image doesn't exist"
    
    file = request.files.get('file')
    print(file)
    if not file:
        return  "no"

    json1 = create_json(file)

    # Read the image
    # img_bytes = file.read()

    # # Prepare the image
    # img = prepare_image(img_bytes)

    result = {
        "Number":11,
        "Table": json1
    }
    return jsonify(result)


if __name__=="__main__":
    app.run(host = '0.0.0.0', port="8089", debug=True)