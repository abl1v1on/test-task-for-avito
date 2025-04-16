from pydantic import BaseModel
from pydantic_settings import BaseSettings


class PageSettings(BaseModel):
    base_url: str = (
        'https://makarovartem.github.io/frontend-avito-tech-test-assignment/'
    )


class Settings(BaseSettings):
    page: PageSettings = PageSettings()


settings = Settings()
