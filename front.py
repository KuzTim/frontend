from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return '''
        <html>
            <head>
                <title>Frontend 2.0</title>
            </head>
            <body>
                <h1>Frontend 2.0</h1>
                <form action="/api/data" method="post">
                    <input type="text" name="userInput" placeholder="Enter some text">
                    <input type="submit" value="Send to Backend">
                </form>
                <div id="result-field">{{ result }}</div>
            </body>
        </html>
    '''

@app.route('/api/data', methods=['POST'])
def send_to_backend():
    user_input = request.form['userInput']
    response = requests.post('http://backend:5000/api/data', json={'userInput': user_input})
    return render_template_string('''
        <html>
            <body>
                <div id="result-field">{{ response.text }}</div>
            </body>
        </html>
    ''', response=response)

if __name__ == '__main__':
    app.run(debug=True)
