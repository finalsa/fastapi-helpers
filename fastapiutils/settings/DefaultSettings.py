from pydantic import BaseSettings
from typing import Optional


class DefaultSettings(BaseSettings):

    app_name: Optional[str] = "ap-buro-credito"
    db_url: Optional[str] = ""
    host: Optional[str] = ""
    env: Optional[str] = "dev"
    port: Optional[str] = "80"
    version: Optional[str] = '1.0.0.0'

    def is_development(self,):
        return (self.env.lower() == 'dev')

    def is_production(self,):
        return (self.env.lower() != 'dev')

    def get_open_api_path(self) -> str:
        if(self.is_development()):
            return "/openapi.json"
        return ""
