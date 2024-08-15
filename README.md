dynaconf validate

for openapi you should generate schema file

# Generate pydantic classes

You can find openapi specifications here https://api.artifactsmmo.com/docs/#/
`datamodel-codegen --input openapi_schema.json --input-file-type openapi --output model.py`
Generated file should be pasted into `src/playground/remote/model.py`

# Generate ready requests as python code from OpenAPI3

You can find openapi specifications here https://api.artifactsmmo.com/docs/#/ in my example it's https://api.artifactsmmo.com/openapi.json 

```bash
pip install openapi-python-client==0.21.2`
openapi-python-client generate --url https://api.artifactsmmo.com/openapi.json --output-path=src/playground/remote/openapi_client --overwrite
# (Optional) To make files more readable 
find src/playground/remote/openapi_client -name "*" | xargs pre-commit run --files  
```


Similar projects:
https://spacetraders.io/