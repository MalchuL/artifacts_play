from dynaconf import settings, Validator


def test_config():
    settings.validators.register(
        # Ensure some parameters exists (are required)
        Validator('API_TOKEN', must_exist=True)
    )
    print(settings.TOKEN)