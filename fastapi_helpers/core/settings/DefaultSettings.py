from typing import Optional
from pydantic import BaseSettings


class DefaultSettings(BaseSettings):
    app_name: Optional[str] = "fastapi"
    db_url: Optional[str] = ""
    host: Optional[str] = ""
    env: Optional[str] = "dev"
    port: Optional[str] = "80"
    version: Optional[str] = '1.0.0.0'

    def is_development(self, ) -> bool:
        return self.env.lower() == 'dev'

    def is_production(self, ) -> bool:
        return self.env.lower() == 'prod'

    def is_stage(self) -> bool:
        return self.env.lower() == 'stage'

    def is_qa(self) -> bool:
        return self.env.lower() == 'qa'

    def is_test(self, ) -> bool:
        return self.env.lower() == 'test'

    def get_db_url(self) -> str:
        if self.is_test():
            return "sqlite:///:memory:"
        return self.db_url

    def get_open_api_path(self) -> str:
        if self.is_development() or self.is_qa():
            return "/openapi.json"
        return ""
