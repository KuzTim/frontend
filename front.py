import requests
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        # Send the text to the backend
        response = requests.post('http://localhost:5001/receive', data={'text': text})
        return 'Text sent to backend!'
    return '''
        <form action="" method="post">
            <input type="text" name="text" placeholder="Enter some text">
            <input type="submit" value="Отправить">
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True, port=5000)