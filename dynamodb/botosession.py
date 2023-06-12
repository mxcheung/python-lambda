import boto3

# Set the AWS profile
session = boto3.Session(profile_name='your_profile_name')

# Use the session to create AWS service clients
s3_client = session.client('s3')
ec2_client = session.client('ec2')

# Now you can use the AWS service clients to interact with AWS
# For example:
response = s3_client.list_buckets()
instances = ec2_client.describe_instances()

# Rest of your code...
