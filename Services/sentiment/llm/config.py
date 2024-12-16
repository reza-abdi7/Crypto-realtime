from pydantic_settings import BaseSettings, SettingsConfigDict


class OpenAIConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file="credentials.env")
    openai_api_key: str
    openai_model_name: str
