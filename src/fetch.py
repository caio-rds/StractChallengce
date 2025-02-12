import requests

token = 'ProcessoSeletivoStract2025'
base_url = 'https://sidebar.stract.to/api'

session = requests.Session()
session.headers.update({
    'Authorization': f'Bearer {token}'
})

def exists_platform(platform: str) -> dict:
    response = session.get(f'{base_url}/platforms')
    data = response.json()
    platforms = data.get('platforms', [])
    for plat in platforms:
        if plat.get('value', '') == platform:
            return {'value': plat.get('value', ''), 'text': plat.get('text', '')}

def fetch_platforms() -> list:
    response = session.get(f'{base_url}/platforms')
    data = response.json()
    return data.get('platforms', [])

def fetch_data(platform: str) -> dict:
    # Fetch accounts
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
        if not pagination or pagination.get('current') >= pagination.get('total'):
            break
        page += 1

    # Fetch fields
    all_fields = []
    page = 1
    while True:
        response = session.get(f'{base_url}/fields', params={
            'platform': platform,
            'page': page
        })
        data = response.json()
        all_fields.extend(data.get('fields', []))
        pagination = data.get('pagination', {})
        if not pagination or pagination.get('current') >= pagination.get('total'):
            break
        page += 1

    # Fetch insights for each account
    insights_data = []
    for account in all_accounts:
        account_id = account.get('id')
        account_token = account.get('token')
        account_name = account.get('name')
        page = 1
        while True:
            response = session.get(f'{base_url}/insights', params={
                'platform': platform,
                'account': account_id,
                'token': account_token,
                'fields': ','.join([field['value'] for field in all_fields]),
                'page': page
            })
            data = response.json()
            for insight in data.get('insights', []):
                insight['account'] = account_id
                insight['account_name'] = account_name

            insights_data.extend(data.get('insights', []))
            pagination = data.get('pagination', {})
            if not pagination or pagination.get('current') >= pagination.get('total'):
                break
            page += 1
    all_fields.extend([{'value': 'account_name', 'text': 'Account Name'}, {'value': 'account', 'text': 'Account'}])
    return {
        'accounts': all_accounts,
        'fields': all_fields,
        'insights': insights_data
    }