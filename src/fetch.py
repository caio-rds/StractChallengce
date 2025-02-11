import requests

token = 'ProcessoSeletivoStract2025'
base_url = 'https://sidebar.stract.to/api'

session = requests.Session()
session.headers.update({
    'Authorization': f'Bearer {token}'
})

def accounts(platform: str) -> list:
    all_accounts = []
    page = 1
    while True:
        response = session.get(f'{base_url}/accounts', params={
            'platform': platform,
            'page': page
        })
        data = response.json()
        all_accounts.extend(data.get('accounts', []))
        pagination = data.get('pagination', {})
        if pagination.get('current') >= pagination.get('total'):
            break
        page += 1
    return all_accounts

def fields(platform: str) -> dict:
    response = session.get(f'{base_url}/fields', params={
        'platform': platform
    })
    return response.json().get('fields')

def insights(platform: str, account_id: str, account_token: str, fields: str) -> dict:
    response = session.get(f'{base_url}/insights', params={
        'platform': platform,
        'account': account_id,
        'token': account_token,
        'fields': fields
    })
    return response.json()