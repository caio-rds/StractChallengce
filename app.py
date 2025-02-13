from flask import Flask, jsonify, render_template

from src.fetch import fetch_data, fetch_platforms, get_data

app = Flask(__name__)


@app.get('/')
def index():
    return render_template('index.html', name='Caio Reis dos Santos de Cresci', email='caiodtn@gmail.com',
                           linkedin='https://www.linkedin.com/in/caio-reis-04224a20a/')


@app.get('/<platform_p>')
def platform(platform_p):
    req = fetch_data(platform_p)
    if req:
        return render_template('platform.html',
                               platform=req.get('name', ''),
                               ads=req.get('insights', []),
                               fields=req.get('fields', []))
    return jsonify({'error': 'Platform not found'}), 404

@app.get('/geral')
def general():
    all_data = get_data('all')
    all_ads = []
    all_fields = set()

    for key, plat in all_data.items():
        ads = plat.get('insights', [])
        fields = plat.get('fields', [])
        all_ads.extend([{'platform': plat.get('name'), **ad} for ad in ads])
        all_fields.update(field['value'] for field in fields)

    all_fields = list(all_fields)
    all_fields.extend(['platform', 'account_name'])

    # Calculate Cost per Click
    for ad in all_ads:
        if 'spend' in ad and 'clicks' in ad and ad['clicks'] > 0:
            ad['cost_per_click'] = ad['spend'] / ad['clicks']
        else:
            ad['cost_per_click'] = None

    return render_template('platform.html', platform='Geral', ads=all_ads, fields=[{'value': field, 'text': field.replace('_', ' ').title()} for field in all_fields])

@app.get('/geral/resumo')
def general_resume():
    all_data = get_data('all')
    all_ads = []
    all_fields = set()

    for key, plat in all_data.items():
        ads = plat.get('insights', [])
        fields = plat.get('fields', [])
        all_ads.extend([{'platform': plat.get('name'), **ad} for ad in ads])
        all_fields.update(field['value'] for field in fields)

    all_fields = list(all_fields)
    all_fields.extend(['platform'])

    # Aggregate data by platform
    aggregated_data = {}
    for ad in all_ads:
        plat = ad['platform']
        if plat not in aggregated_data:
            aggregated_data[plat] = {key: 0 if isinstance(value, (int, float)) else '' for key, value in ad.items()}
            aggregated_data[plat]['platform'] = plat
        for key, value in ad.items():
            if isinstance(value, (int, float)):
                aggregated_data[plat][key] += value

    # Convert aggregated data to list
    aggregated_ads = list(aggregated_data.values())

    return render_template('platform.html', platform='Geral Resumo', ads=aggregated_ads, fields=[{'value': field, 'text': field.replace('_', ' ').title()} for field in all_fields])

@app.route('/<platform_p>/resumo', methods=['GET'])
def platform_resume(platform_p):
    req = fetch_data(platform_p)
    if not req:
        return jsonify({'error': 'Platform not found'}), 404
    ads = req.get('insights', [])

    # Aggregate data by account
    aggregated_data = {}
    for ad in ads:
        account = ad['account']
        if account not in aggregated_data:
            aggregated_data[account] = {key: 0 if isinstance(value, (int, float)) else '' for key, value in ad.items()}
            aggregated_data[account]['account'] = account
            aggregated_data[account]['account_name'] = ad['account_name']
        for key, value in ad.items():
            if isinstance(value, (int, float)):
                aggregated_data[account][key] += value

    # Convert aggregated data to list
    aggregated_ads = list(aggregated_data.values())
    return render_template('platform.html', platform=req.get('name', ''), ads=aggregated_ads, fields=req.get('fields', []))

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run()