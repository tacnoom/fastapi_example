from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='./app/.env', case_sensitive=False)

    database_hostname: str 
    database_port: str 
    database_name: str 
    database_username: str 
    database_password: str 
    secret_key: str 
    algorithm: str 
    access_token_expire_minutes: int


settings = Settings()
# print(settings.model_dump())

#doing a listdir helped
