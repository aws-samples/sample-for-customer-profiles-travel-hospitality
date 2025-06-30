import boto3
domainName = 'amazon-connect-cp-hotels'
endpoint_url = 'https://profile.us-east-1.amazonaws.com'
client = boto3.client('customer-profiles')