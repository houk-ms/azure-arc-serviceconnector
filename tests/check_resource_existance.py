import sys
from utils import (
    load_kube_config,
    list_namespace,
    list_secret,
    get_secret
)

def check_resource_existance(parameter_file):
    import json

    load_kube_config()
    file_in = open(parameter_file, 'r', encoding='utf-8')
    data = json.load(file_in)

    ns_name = data.get('resources').get('namespace').get('name')

    secret_name = data.get('resources').get('secret', dict()).get('name')
    secret_keys = list(data.get('resources').get('secret', dict()).get('data', []))
    if not secret_name:
        secret_name = data.get('resources').get('secretProviderClass').get('k8sSecretName')
        secret_keys = list(data.get('resources').get('secretProviderClass').get('keyvaultSecrets'))

    # check namespace
    ns_names = list_namespace()
    if ns_name not in ns_names:
        print("Error: Namespace {} does not exist.".format(ns_name))
        return

    # check secret
    secrets = list_secret(ns_name)
    if secret_name not in secrets:
        print("Error: Secret {} does not exist.".format(secret_name))
        return

    # check secret key
    secret_keyvals = get_secret(ns_name, secret_name)
    for key in secret_keys:
        if key not in secret_keyvals:
            print("Error: Key {} not found in secret {}.".format(key, secret_name))
            return

    print("Success: Resource existance checking passed.")


if len(sys.argv) == 2:
    check_resource_existance(sys.argv[1])
else:
    raise Exception("Invalid argument.")
