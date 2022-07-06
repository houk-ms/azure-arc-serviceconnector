# The script formats the parameter json file as Arc extension parameters
# It generally does the following things:
#   1. generate an correlationid
#   2. encode the resources propertry as base64 string
#   3. format the parameters as key-value pairs as CLI arguments

import sys


def format_parameter(file_path):
    import json
    import uuid
    import base64

    file_in = open(file_path, 'r', encoding='utf-8')
    data = json.load(file_in)

    data['correlationid'] = str(uuid.uuid4())
    serialized_resources = json.dumps(data['resources']).encode('utf-8')
    data['resources'] = base64.b64encode(serialized_resources).decode("utf-8")

    arguments = ''
    for name, value in data.items():
        arguments += '{}={} '.format(name, value)
    return arguments


if len(sys.argv) == 2:
    print(format_parameter(sys.argv[1]))
else:
    raise Exception("Invalid argument.")
