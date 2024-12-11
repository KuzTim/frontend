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
            </head>
            <body>
                <h1>Frontend 2.0</h1>
                <form>
                    <input type="text" id="userInput" placeholder="Enter some text">
                    <input type="button" value="Send to Backend" onclick="sendToBackend()">
                    <br><br>
                    <input type="button" value="Get Last Line from Backend" onclick="getLastLineFromBackend()">
                    <br><br>
                    <input type="text" id="result-field" placeholder="Result">
                </form>
                <div id="result-field"></div>
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
                                $('#result-field').val('Error123: ' + error);
                            }
                        });
                    }

                    function getLastLineFromBackend() {
                        $.ajax({
                            type: 'GET',
                            url: '/api/data',
                            success: function(data) {
                                var lastLine = data.data;
                                $('#result-field').val(lastLine);
                            },
                            error: function(xhr, status, error) {
                                $('#result-field').val('Error123: ' + error);
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
