dynaconf validate

for openapi you should generate schema file

# Generate pydantic classes

You can find openapi specifications here https://api.artifactsmmo.com/docs/#/
`datamodel-codegen  --input openapi_schema.json --input-file-type openapi --output model.py`

# Generate ready requests as python code from OpenAPI3

You can find openapi specifications here https://api.artifactsmmo.com/docs/#/

```bash
pip install openapi-python-client==0.21.2`
openapi-python-client generate --url https://api.artifactsmmo.com/openapi.json --output-path=artifacts_openapi_client
```
