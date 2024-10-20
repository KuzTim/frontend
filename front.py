from flask import Flask, request, render_template_string, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return '''
        <html>
            <head>
                <title>Frontend 2.0</title>
                <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        margin: 0;
                        padding: 20px;
                    }
                    h1 {
                        color: #333;
                    }
                    form {
                        background: #fff;
                        padding: 20px;
                        border-radius: 5px;
                        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                    }
                    input[type="text"] {
                        width: calc(100% - 22px);
                        padding: 10px;
                        margin: 10px 0;
                        border: 1px solid #ccc;
                        border-radius: 4px;
                    }
                    input[type="button"] {
                        padding: 10px 15px;
                        background-color: #28a745;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        cursor: pointer;
                    }
                    input[type="button"]:hover {
                        background-color: #218838;
                    }
                    #result-field {
                        margin-top: 20px;
                        padding: 10px;
                        background-color: #e2e3e5;
                        border-radius: 4px;
                    }
                </style>
            </head>
            <body>
                <h1>Frontend 2.0</h1>
                <form>
                    <input type="text" id="userInput" placeholder="Введите текст">
                    <input type="button" value="Отправить на Backend" onclick="sendToBackend()">
                    <br>
                    <input type="button" value="Получить последнюю строку из Backend" onclick="getLastLineFromBackend()">
                </form>
                <div id="result-field" placeholder="Результат"></div>
                <script>
                    function sendToBackend() {
                        var userInput = $('#userInput').val();
                        $.ajax({
                            type: 'POST',
                            url: '/api/data',
                            data: JSON.stringify({userInput: userInput}),
                            contentType: 'application/json',
                            success: function(data) {
                                // Успешно отправлено, ничего не нужно делать
                            },
                            error: function(xhr, status, error) {
                                $('#result-field').text('Ошибка: ' + error);
                            }
                        });
                    }

                    function getLastLineFromBackend() {
                        $.ajax({
                            type: 'GET',
                            url: '/api/data',
                            success: function(data) {
                                var lastLine = data.data;
                                $('#result-field').text(lastLine);
                            },
                            error: function(xhr, status, error) {
                                $('#result-field').text('Ошибка: ' + error);
                            }
                        });
                    }
                </script>
            </body>
        </html>
    '''

@app.route('/api/data', methods=['POST', 'GET'])
def send_to_backend():
    if request.method == 'POST':
        try:
            user_input = request.json['userInput']
            try:
                response = requests.post('http://127.0.0.1:5001/api/data', json={'userInput': user_input})
                response.raise_for_status()
                return jsonify({'data': response.json()['data']})
            except requests.exceptions.RequestException as e:
                return jsonify({'error': str(e)}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    elif request.method == 'GET':
        try:
            response = requests.get('http://127.0.0.1:5001/api/data')
            response.raise_for_status()
            return jsonify({'data': response.json()['data']})
        except requests.exceptions.RequestException as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5002)