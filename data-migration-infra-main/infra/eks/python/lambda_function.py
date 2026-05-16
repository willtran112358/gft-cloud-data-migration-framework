import boto3
import json
import os

def lambda_handler(event, context):
    cluster_name = os.getenv('CLUSTER_NAME')
    region = os.getenv('REGION')
    namespace = os.getenv('NAMESPACE')

    eks = boto3.client('eks', region_name=region)
    response = eks.describe_cluster(name=cluster_name)
    endpoint = response['cluster']['endpoint']
    cert_authority = response['cluster']['certificateAuthority']['data']
    
    kubeconfig = f"""
    apiVersion: v1
    kind: Config
    clusters:
    - cluster:
        server: {endpoint}
        certificate-authority-data: {cert_authority}
      name: {cluster_name}
    contexts:
    - context:
        cluster: {cluster_name}
        user: {cluster_name}
      name: {cluster_name}
    current-context: {cluster_name}
    users:
    - name: {cluster_name}
      user:
        exec:
          apiVersion: client.authentication.k8s.io/v1beta1
          command: aws
          args:
          - eks
          - get-token
          - --cluster-name
          - {cluster_name}
    """

    with open('/tmp/kubeconfig', 'w') as file:
        file.write(kubeconfig)

    os.environ['KUBECONFIG'] = '/tmp/kubeconfig'

    import subprocess
    subprocess.run(["kubectl", "create", "namespace", namespace], check=True)

    return {
        'statusCode': 200,
        'body': json.dumps(f'Namespace {namespace} created successfully!')
    }
