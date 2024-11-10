dynaconf validate

for openapi you should generate schema file

# Generate pydantic classes

You can find openapi specifications here https://api.artifactsmmo.com/docs/#/
`datamodel-codegen --input .stuff/openapiv3.yaml --input-file-type openapi --output src/rest_api_client/model.py`
!! Replace all `regex` occurrences to `pattern` !!!

And if you are using PyCharm, install pydantic plugin https://plugins.jetbrains.com/plugin/12861-pydantic
Generated file should be pasted into `src/playground/remote/model.py`

# Generate ready requests as python code from OpenAPI3

You can find openapi specifications here https://api.artifactsmmo.com/docs/#/ in my example it's https://api.artifactsmmo.com/openapi.json 

```bash
python tools/generate_openapi_classes.py
```

Create file .secrets.toml
```toml
[default]
api_token="<API_TOKEN>"
```

Similar projects:
https://spacetraders.io/