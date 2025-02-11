from flask import Flask, jsonify, render_template

from src.fetch import accounts

app = Flask(__name__)

@app.get('/')
def hello_world():
    return render_template('index.html', name='Caio Reis dos Santos de Cresci', email='caiodtn@gmail.com', linkedin='https://www.linkedin.com/in/caio-reis-04224a20a/')

@app.get('/<platform>')
def hello_platform(platform):
    req = accounts(platform)
    return jsonify(req)

    # ads = [
    #     {'platform': platform, 'ad_name': 'Some Ad', 'clicks': 10},
    #     {'platform': platform, 'ad_name': 'Other Ad', 'clicks': 20}
    # ]
    # return render_template('platform.html', platform=platform, ads=ads)

@app.get('/geral')
def geral():
    ads = [
        {'platform': 'Facebook', 'ad_name': 'Some Ad', 'clicks': 10},
        {'platform': 'YouTube', 'ad_name': 'One More Ad', 'clicks': 5}
    ]
    return render_template('platform.html', platform='Geral', ads=ads)

@app.get('/geral/resumo')
def geral_resume():
    ads = [
        {'platform': 'Facebook', 'ad_name': '', 'clicks': 30},
        {'platform': 'YouTube', 'ad_name': '', 'clicks': 5}
    ]
    return render_template('platform.html', platform='Geral Resumo', ads=ads)

@app.route('/<platform>/resumo', methods=['GET'])
def hello_platform_resume(platform):
    ads = [
        {'platform': platform, 'ad_name': '', 'clicks': 30}
    ]
    return render_template('platform.html', platform=f'{platform} Resumo', ads=ads)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run()