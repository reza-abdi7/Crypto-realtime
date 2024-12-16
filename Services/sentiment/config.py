from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file="settings.env")
    kafka_broker_address: str
    kafka_input_topic: str
    kafka_output_topic: str
    kafka_consumer_group: str

    model_provider: Literal["openai", "llamacpp"]


config = Config()
