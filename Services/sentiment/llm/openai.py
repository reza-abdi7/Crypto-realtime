from typing import Optional
from llama_index.core.prompts import PromptTemplate

from llama_index.llms.openai import OpenAI
from .base import NewsSentiment


class OpenaiSentimentExtractor:
    def __init__(
        self,
        model_name: str,
        api_key: str,
        temperature: Optional[float] = 0,
        max_tokens: int = 256,
    ):
        self.llm = OpenAI(
            model=model_name,
            api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        self.prompt_template = PromptTemplate(
            template="""
            You are an expert in sentiment analysis.
            You will be given news about Bitcoin and Ethereum and you will provide a sentiment analysis of the news.
            The sentiment analysis will be in the form of a JSON object with the following fields:
            - btc_sentiment: the impace of the news on the price of BTC
                -1: if the price is expected to fall
                0: if the price is expected to remain stable
                1: if the price is expected to rise

            - eth_sentiment: the impace of the news on the price of ETH
                -1: if the price is expected to fall
                0: if the price is expected to remain stable
                1: if the price is expected to rise

            If the news is not related to BTC or ETH, the sentiment is 0

            Here is the news article:
            {news_article}
            """
        )

    def get_sentiment(self, news: str) -> NewsSentiment:
        response: NewsSentiment = self.llm.structured_predict(
            NewsSentiment, prompt=self.prompt_template, news_article=news
        )

        return response


if __name__ == "__main__":
    from .config import OpenAIConfig

    config = OpenAIConfig()
    llm = OpenaiSentimentExtractor(
        model_name=config.openai_model_name,
        api_key=config.openai_api_key,
    )

    examples = [
        "Bitcoin ETF ads spotted on China’s Alipay payment app",
        "U.S. Supreme Court Lets Nvidia’s Crypto Lawsuit Move Forward",
        "Trump’s World Liberty Acquires ETH, LINK, and AAVE in $12M Crypto Shopping Spree",
    ]

    for example in examples:
        print(f"Example: {example}")
        response = llm.get_sentiment(example)
