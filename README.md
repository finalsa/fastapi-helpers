# Fastapi Helpers

This pip packages will help you to make your life easier when working with fastapi and ormar.

For installing this package:

```bash
pip install fastapi-helpers
```

If you need a default settings for your app, it includes an implemntation BaseSettings of pydantic.

```python
from fastapi_helpers import DefaultSettings
from utils import env_path
from typing import Optional

class Settings(DefaultSettings):
    app_name = "your-app-name"
    redis_url: Optional[str] = 'redis://localhost:6379'
    version: Optional[str] = '1.0.0.0'
    port: Optional[str] = "8000"
    env: Optional[str] = "dev" #dev, test, prod


settings = Settings(env_path)
```

If you need a logger, it includes an implemntation a colored console, and in prod envs it will log to aws with the help of watchtower.

```python
from fastapi_helpers import DefaultLogger
from .config import settings

logger = DefaultLogger("your-app-name", settings)
```

If you need to connect to a db super fast, the only thing you need to do is to:

```python
from fastapi_helpers import DbConfig
from core.config import settings
from core.logger import logger

db_config = DbConfig(settings, logger)
```

The are other tools for making the usage of ormar and fastapi even easier.


I would realy like to make this tools bigger, but I´m looking for help for documenting this package.


Happy codding!