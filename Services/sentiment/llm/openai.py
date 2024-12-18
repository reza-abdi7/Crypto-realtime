from typing import Optional, Literal
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
            You are an expert crypto financial analyst with deep knowledge of market dynamics and sentiment analysis.
            Analyze the following news story and determine its potential impact on crypto asset prices.
            Focus ONLY on coins that are directly mentioned or significantly impacted by the news.
            DO NOT include coins that are not relevant to the news content.

            Do not output data for a given coin if the news is not relevant to it.

            ## Example input
            "Goldman Sachs wants to invest in Bitcoin and Ethereum, but not in XRP"

            ## Example output
            [
                {"coin": "BTC", "signal": 1},
                {"coin": "ETH", "signal": 1},
                {"coin": "XRP", "signal": -1},
            ]

            ## Example input
            "Bitcoin ETF ads spotted on China's Alipay payment app"

            ## Example output
            [
                    {"coin": "BTC", "sentiment": 1}
            ]
           

            News story to analyze:
            {news_story}

            ## Output (only valid JSON):
            """
        )

        self.model_name = model_name

    def get_sentiment(
        self,
        text: str,
        output_format: Literal["dict", "NewsSentiment"] = "NewsSentiment",
    ) -> NewsSentiment | dict:
        response: NewsSentiment = self.llm.structured_predict(
            NewsSentiment,
            prompt=self.prompt_template,
            news_story=text,
        )
        # keep only news sentiments with non-zero sentiment
        response.news_sentiments = [
            news_sentiment
            for news_sentiment in response.news_sentiments
            if news_sentiment.sentiment != 0
        ]

        if output_format == "dict":
            return response.to_dict()
        else:
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
        print(response)
