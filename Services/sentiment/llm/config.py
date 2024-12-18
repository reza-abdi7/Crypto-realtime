from pydantic_settings import BaseSettings, SettingsConfigDict


class OpenAIConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file="credentials.env")
    openai_api_key: str
    openai_model_name: str


class OllamaConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file="ollama.env")
    model_name: str


class LlamacppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file="llamacpp.env")
    model_name: str
