import json
import urllib.request
import urllib.parse
import os

def lambda_handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST,OPTIONS'
    }

    if event.get('requestContext', {}).get('http', {}).get('method') == 'OPTIONS':
        return {'statusCode': 200, 'headers': headers, 'body': ''}

    try:
        body = json.loads(event.get('body', '{}'))
        code = body.get('code', '')

        data = urllib.parse.urlencode({
            'client_id': os.environ['GITHUB_CLIENT_ID'],
            'client_secret': os.environ['GITHUB_CLIENT_SECRET'],
            'code': code
        }).encode()

        req = urllib.request.Request('https://github.com/login/oauth/access_token',
            data=data,
            headers={'Accept': 'application/json', 'User-Agent': 'cannabis-directory'})
        resp = urllib.request.urlopen(req)
        token_data = json.loads(resp.read())

        if 'access_token' not in token_data:
            return {'statusCode': 400, 'headers': headers,
                    'body': json.dumps({'error': 'GitHub auth failed', 'details': token_data})}

        # Get user info
        req2 = urllib.request.Request('https://api.github.com/user',
            headers={'Authorization': f'token {token_data["access_token"]}', 'User-Agent': 'cannabis-directory'})
        resp2 = urllib.request.urlopen(req2)
        user = json.loads(resp2.read())

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'access_token': token_data['access_token'],
                'username': user['login'],
                'avatar_url': user.get('avatar_url', '')
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }
