from kubernetes import client, config

def load_kube_config():
    # Loading in-cluster kube-config
    try:
        config.load_incluster_config()
        # config.load_kube_config()
    except Exception as e:
        print("Error: Failed loading the in-cluster config: " + str(e))


def list_namespace():
    v1 = client.CoreV1Api()
    namespaces = v1.list_namespace()
    ns_names = [item.metadata.name for item in namespaces.items]
    
    return ns_names


def list_secret(ns_name):
    v1 = client.CoreV1Api()
    secrets = v1.list_namespaced_secret(ns_name)

    return [item.metadata.name for item in secrets.items]


def get_secret(ns_name, secret_name):
    import base64

    v1 = client.CoreV1Api()
    secret = v1.read_namespaced_secret(secret_name, ns_name)

    return {k:base64.b64decode(v) for k, v in secret.data.items()}
