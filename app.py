from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():
    return jsonify({
        'name': 'Caio Reis dos Santos de Cresci',
        'email': 'caiodtn@gmail.com',
        'linkedin': 'https://www.linkedin.com/in/caio-reis-04224a20a/'
    })

if __name__ == '__main__':
    app.run()