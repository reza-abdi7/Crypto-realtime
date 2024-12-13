from typing import List, Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='settings.env', env_file_encoding='utf-8'
    )
    kafka_broker_address: str
    kafka_input_topic: str
    kafka_consumer_group: str
    feature_group_name: str
    feature_group_version: int
    feature_group_primary_key: List[str]
    feature_group_event_time: str
    feature_group_materialization_interval_minutes: int
    data_source: Literal['live', 'historical']


class HopsworksCredentials(BaseSettings):
    model_config = SettingsConfigDict(env_file='credentials.env')
    hopsworks_api_key: str
    hopsworks_project_name: str


config = Settings()
hopsworks_credentials = HopsworksCredentials()
