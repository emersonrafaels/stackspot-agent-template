from pathlib import Path
from dynaconf import Dynaconf

# Get current directory
CONFIG_PATH = Path(__file__).parent.resolve()

settings = Dynaconf(
    settings_files=[
        Path(CONFIG_PATH, "settings.toml"),
        Path(CONFIG_PATH, ".secrets.toml"),
    ],
    environments=True,  # Enable multiple environments like development, production
    load_dotenv=True,  # Enable loading of .env files
)

"""
# Validate required settings
settings.validators.register(
    Validator("stackspot_client_secret", must_exist=True)
)
"""
