import boto3
domainName = 'tnh15'
endpoint_url = 'https://profile.us-east-1.amazonaws.com'
client = boto3.client('customer-profiles', region_name='us-east-1')