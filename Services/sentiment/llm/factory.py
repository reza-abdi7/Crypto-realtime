from typing import Literal
from .base import BaseSentimentExtractor
from .openai import OpenaiSentimentExtractor
# from .llamacpp import LlamacppSentimentExtractor


def get_llm(model_provider: Literal["openai", "llamacpp"]) -> BaseSentimentExtractor:
    """
    Returns the llm for sentiment analysis
    """

    if model_provider == "openai":
        from .config import OpenAIConfig

        config = OpenAIConfig()

        return OpenaiSentimentExtractor(
            model_name=config.openai_model_name, api_key=config.openai_api_key
        )

    # elif model_provider == "llamacpp":
    #     return LlamacppSentimentExtractor()
    else:
        raise ValueError(f"Unknown model provider: {model_provider}")
