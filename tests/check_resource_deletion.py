import sys
from utils import (
    load_kube_config,
    list_namespace,
    list_secret
)

def check_resource_deletion(parameter_file):
    import json

    load_kube_config()
    file_in = open(parameter_file, 'r', encoding='utf-8')
    data = json.load(file_in)

    ns_name = data.get('resources').get('namespace').get('name')
    secret_name = data.get('resources').get('secret', dict()).get('name')
    if not secret_name:
        secret_name = data.get('resources').get('secretProviderClass').get('k8sSecretName')

    # check namespace
    ns_names = list_namespace()
    if ns_name not in ns_names:
        print("Error: Namespace {} does not exist.".format(ns_name))
        return
    
    # check secret
    secrets = list_secret(ns_name)
    if secret_name not in secrets:
        print("Error: Secret {} should not be deleted.".format(secret_name))
        return

    print("Success: Resource deletion checking passed.")


if len(sys.argv) == 2:
    check_resource_deletion(sys.argv[1])
else:
    raise Exception("Invalid argument.")
