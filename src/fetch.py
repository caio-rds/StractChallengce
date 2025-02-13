import requests

token = 'ProcessoSeletivoStract2025'
base_url = 'https://sidebar.stract.to/api'

session = requests.Session()
session.headers.update({
    'Authorization': f'Bearer {token}'
})

data = {}

def fetch_data(platform_index: str) -> dict | str:

    all_accounts, all_fields, insights_data = [], [], []
    page = 1

    while True:
        response = session.get(f'{base_url}/accounts', params={'platform': platform_index, 'page': page})
        resp_data = response.json()
        all_accounts.extend(resp_data.get('accounts', []))
        pagination = resp_data.get('pagination', {})
        if not pagination or pagination.get('current') >= pagination.get('total'):
            break
        page += 1

    page = 1
    while True:
        resp = session.get(f'{base_url}/fields', params={'platform': platform_index, 'page': page})
        resp_data = resp.json()
        all_fields.extend(resp_data.get('fields', []))
        pagination = resp_data.get('pagination', {})
        if not pagination or pagination.get('current') >= pagination.get('total'):
            break
        page += 1

    for account in all_accounts:
        account_id, account_token, account_name = account.get('id'), account.get('token'), account.get('name')
        page = 1
        while True:
            resp = session.get(f'{base_url}/insights', params={
                'platform': platform_index,
                'account': account_id,
                'token': account_token,
                'fields': ','.join([field['value'] for field in all_fields]),
                'page': page
            })
            resp_data = resp.json()
            for insight in resp_data.get('insights', []):
                insight.update({'account': account_id, 'account_name': account_name})
            insights_data.extend(resp_data.get('insights', []))
            pagination = resp_data.get('pagination', {})
            if not pagination or pagination.get('current') >= pagination.get('total'):
                break
            page += 1

    all_fields.extend([{'value': 'account_name', 'text': 'Account Name'}, {'value': 'account', 'text': 'Account'}])
    return {'accounts': all_accounts, 'fields': all_fields, 'insights': insights_data}


def fetch_platforms() -> list:
    response = session.get(f'{base_url}/platforms')
    return response.json().get('platforms', [])

for platform in fetch_platforms():
    req = fetch_data(platform['value'])
    data[platform['value']] = req
    data[platform['value']].update({'name': platform.get('text', '')})
    print(data)

def get_data(platform_index: str | None = False) -> dict | None:
    if platform_index == 'all':
        return data
    if data[platform_index]:
        return data[platform_index]
    return None