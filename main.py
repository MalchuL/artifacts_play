from pprint import pprint

from dynaconf import Validator, settings

settings.validators.register(
    # Ensure some parameters exists (are required)
    Validator("API_TOKEN", must_exist=True),
    Validator("CHARACTERS", len_min=1, must_exist=True, cast=list),
)
pprint(settings.items())
print(settings.CHARACTERS)
