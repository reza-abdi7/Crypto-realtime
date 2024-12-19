from pydantic_settings import BaseSettings, SettingsConfigDict


class OpenAIConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file="credentials.env")
    openai_api_key: str
    openai_model_name: str


class OllamaConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file="ollama.env")
    model_name: str


class LlamaCppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file="llamacpp.env")
    model_path: str
    n_ctx: int
    n_threads: int
    temperature: float
    max_tokens: int
    repeat_penalty: float
    verbose: bool
    penalize_nl: bool
    escape_newlines: bool
