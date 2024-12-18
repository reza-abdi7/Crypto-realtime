from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from typing import Literal


class SentimentOneCoin(BaseModel):
    coin: Literal[
        "BTC",
        "ETH",
        "SOL",
        "XRP",
        "DOGE",
        "ADA",
        "XLM",
        "LTC",
        "BCH",
        "DOT",
        "XMR",
        "EOS",
        "XEM",
        "ZEC",
        "ETC",
        "LINK",
        "AAVE",
    ] = Field(description="The coin that the news is about")

    sentiment: Literal[-1, 0, 1] = Field(
        description="""
    The signal of the news on the coin price.
    1 if the price is expected to go up
    -1 if it is expected to go down.
    0 if the news is not related to the coin.

    IMPORTANT: Only include coins that are directly mentioned or impacted by the news.
    Do not include coins that are not relevant to the news content.
    """
    )


class NewsSentiment(BaseModel):
    news_sentiments: list[SentimentOneCoin]
    # reasoning: str = Field(description="Explanation of the sentiment analysis and reasoning behind the signals")

    def to_dict(self) -> dict:
        """
        Return a dictionary representation of the newsSentiment.
        """
        # return {
        #     'new_sentiment': [
        #         sentiment.model_dump() for sentiment in self.new_sentiment
        #     ],
        #     'reasoning': self.reasoning
        # }
        # raise NotImplementedError()


class BaseSentimentExtractor(ABC):
    @abstractmethod
    def get_sentiment(
        self, text: str, output_format: Literal["dict", "NewsSentiment"] = "dict"
    ) -> dict | NewsSentiment:
        pass
