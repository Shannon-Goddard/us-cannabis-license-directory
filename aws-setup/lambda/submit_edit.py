import json
import boto3
import urllib.request
import uuid
from datetime import datetime, timezone

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('cannabis-directory-ledger')

def lambda_handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization',
        'Access-Control-Allow-Methods': 'POST,OPTIONS'
    }

    if event.get('requestContext', {}).get('http', {}).get('method') == 'OPTIONS':
        return {'statusCode': 200, 'headers': headers, 'body': ''}

    try:
        body = json.loads(event.get('body', '{}'))
        token = body.get('github_token', '')

        # Validate GitHub token
        req = urllib.request.Request('https://api.github.com/user',
            headers={'Authorization': f'token {token}', 'User-Agent': 'cannabis-directory'})
        resp = urllib.request.urlopen(req)
        user = json.loads(resp.read())
        username = user['login']

        now = datetime.now(timezone.utc).isoformat()

        table.put_item(Item={
            'edit_id': str(uuid.uuid4()),
            'timestamp': now,
            'github_user': username,
            'row_index': str(body.get('row_index', '')),
            'column': body.get('column', ''),
            'old_value': body.get('old_value', ''),
            'new_value': body.get('new_value', ''),
            'business_name': body.get('business_name', ''),
            'status': 'pending'
        })

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'Edit submitted', 'user': username, 'timestamp': now})
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }
