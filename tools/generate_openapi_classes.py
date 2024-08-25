import pprint

from openapi_parser import parse

content = parse('.stuff/openapiv2.yaml')

"""
Parses file and creates files for src/rest_api_client
"""

import_classes = []

for path in content.paths:
    for operation in path.operations:
        method_name = operation.method.name.lower()
        endpoint_pattern = path.url
        successful_response = [response for response in operation.responses if response.content][0]
        assert len(successful_response.content) == 1
        response_schema = successful_response.content[0].schema.title.replace('[', "").replace("]",
                                                                                               "")
        assert len([response for response in operation.responses if response.content]) == 1

        if operation.request_body is None:
            request_class_name = None
        else:
            request = operation.request_body.content
            assert len(request) == 1
            request_class_name = request[0].schema.title

        error_responses = {int(response.code): response.description for response in
                           operation.responses if response.code != 200}

        if request_class_name:
            import_classes.append(request_class_name)
        import_classes.append(response_schema)

        class_name = operation.summary.replace(" ", "")
        parent_class = "CharacterRequest" if "{name}" in endpoint_pattern else "SingleArtifactsRequest"
        print(f"class {class_name}({parent_class}):")

        print(f'    """')
        print(f"    {operation.summary}")
        print(f"    {operation.description}")
        print(f"    operationId: {operation.operation_id}")
        print(f'    """')

        print(f"    endpoint_pattern = '{endpoint_pattern}'")
        print(f"    method_name = '{method_name}'")
        print(f"    response_schema = {response_schema}")
        if len(error_responses) == 0:
            print(f"    error_responses = {{}}")
        for i, (err_code, err_desc) in enumerate(error_responses.items()):
            dict_item = f"{err_code}: '{err_desc}'"
            if i == 0:
                if len(error_responses) == 1:
                    print(f"    error_responses = {{{dict_item}}}")
                else:
                    print(f"    error_responses = {{{dict_item}, ")
            elif i == len(error_responses) - 1:
                print(f"                       {dict_item}}}")
            else:
                print(f"                       {dict_item},")
        print()
        if request_class_name is None:
            print(f"    def __call__(self) -> {response_schema}:")
            print("        return super().__call__(None)")
        else:
            print(f"    def __call__(self, data: {request_class_name}) -> {response_schema}:")
            print("        return super().__call__(data)")
        print()
        print()
    # print(path)
    # print({path.})

print(", ".join(set(import_classes)))