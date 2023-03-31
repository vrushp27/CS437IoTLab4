import boto3

def create_thing(thing_name):
    iot_client = boto3.client('iot', region_name='us-east-2')
    response = iot_client.create_thing(
        thingName=thing_name
    )
    return response['thingArn']

    
def create_keys_and_certificate(thing_name):
    iot_client = boto3.client('iot', region_name='us-east-2')
    response = iot_client.create_keys_and_certificate(
        setAsActive=True
    )
    certificate_arn = response['certificateArn']
    certificate_id = response['certificateId']
    private_key = response['keyPair']['PrivateKey']
    public_key = response['keyPair']['PublicKey']
    iot_client.attach_thing_principal(
        thingName=thing_name,
        principal=certificate_arn
    )
    return (certificate_id, certificate_arn, private_key, public_key)

def attach_policy(certificate_arn, policy_name):
    iot_client = boto3.client('iot', region_name='us-east-2')
    response = iot_client.attach_policy(
        policyName=policy_name,
        target=certificate_arn
    )

def attach_thing_principal(thing_name, certificate_arn):
    iot_client = boto3.client('iot', region_name='us-east-2')
    response = iot_client.attach_thing_principal(
        thingName=thing_name,
        principal=certificate_arn
    )

def add_thing_to_thing_group(thing_name, thing_group_name):
    iot_client = boto3.client('iot', region_name='us-east-2')
    response = iot_client.add_thing_to_thing_group(
        thingGroupName=thing_group_name,
        thingName=thing_name
    )

# Example usage:
thing_name = 'Device4'
create_thing(thing_name)
certificate_id, certificate_arn, private_key, public_key = create_keys_and_certificate(thing_name)
attach_policy(certificate_arn, 'MyIotPolicy')
attach_thing_principal(thing_name, certificate_arn)
add_thing_to_thing_group(thing_name, 'MyStaticGroup')
