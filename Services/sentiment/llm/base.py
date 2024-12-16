from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from typing import Literal


class NewsSentiment(BaseModel):
    btc_sentiment: Literal[-1, 0, 1] = Field(
        description="""
        the impace of the news on the price of BTC
        -1: if the price is expected to fall
        0: if the price is expected to remain stable
        1: if the price is expected to rise

        If the news is not related to BTC, the sentiment is 0
        """
    )

    eth_sentiment: Literal[-1, 0, 1] = Field(
        description="""
        the impace of the news on the price of ETH
        -1: if the price is expected to fall
        0: if the price is expected to remain stable
        1: if the price is expected to rise

        If the news is not related to ETH, the sentiment is 0
        """
    )

    reasoning: str = Field(
        description="The reasoning behind the sentiment analysis from news article."
    )

    def to_dict(self) -> dict:
        """
        Return a dictionary representation of the NewsSentiment object
        """
        return {
            "btc_sentiment": self.btc_sentiment,
            "eth_sentiment": self.eth_sentiment,
            "reasoning": self.reasoning,
        }


class BaseSentimentExtractor(ABC):
    @abstractmethod
    def extract_sentiment(
        self, text: str, output_format: Literal["dict", "NewsSentiment"] = "dict"
    ) -> dict | NewsSentiment:
        pass
