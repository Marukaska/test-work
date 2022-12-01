from flask import Flask, jsonify, request, render_template
import json
import os
import tempfile


app = Flask(__name__)

storage_data = os.path.join(tempfile.gettempdir(), 'storage.data')


def read_data():
    if not os.path.exists(storage_data):
        return {}
    with open(storage_data, 'r', encoding='utf-8') as file:
       data = json.load(file)
    return data


def write_data(dict_data):
    with open(storage_data, 'w', encoding='utf-8') as file:
        json.dump(dict_data, file, ensure_ascii=False)


@app.route('/', methods=['GET'])
def api_source():
    return render_template('api.html')


@app.route('/api/v1/storage/json/all', methods=['GET'])
def get_all():
    with open(storage_data, 'r', encoding='utf-8') as file:
        return json.load(file)


@app.route('/api/v1/storage/json/read', methods=['GET'])
def read_key():
    data_temp = read_data()
    key = request.args.get('key')

    if key in data_temp:
        return {'results': list(data_temp[key])}
    else:
        return jsonify({"message": 'None'})


@app.route('/api/v1/storage/json/write', methods=['POST'])
def post():
    if not request.json:
        return jsonify({"message": 'Error data in CURL'})
    post_data = request.json

    data_temp = read_data()

    for key in post_data:
        data_temp = read_data()

        if key in data_temp:
            data_temp[key].append(post_data[key])
        else:
            data_temp[key] = [post_data[key]]

    write_data(data_temp)

    return f'Success add data {post_data}'


if __name__ == '__main__':
    app.run(debug=True)