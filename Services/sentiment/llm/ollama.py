from typing import Optional, Literal
from .base import BaseSentimentExtractor, NewsSentiment
from llama_index.core.prompts import PromptTemplate
from llama_index.llms.ollama import Ollama


class OllamaSentimentExtractor(BaseSentimentExtractor):
    def __init__(
        self,
        model_name: str,
        temperature: Optional[float] = 0,
    ):
        self.llm = Ollama(
            model=model_name,
            temperature=temperature,
        )

        self.prompt_template = PromptTemplate(
            template="""
            You are an expert crypto financial analyst with deep knowledge of market dynamics and sentiment analysis.
            Analyze the following news story and determine its potential impact on crypto asset prices.
            Focus ONLY on coins that are directly mentioned or significantly impacted by the news.
            DO NOT include coins that are not relevant to the news content.

            ## Example input
            "Goldman Sachs wants to invest in Bitcoin and Ethereum, but not in XRP"

            ## Example output
            {
                "new_sentiment": [
                    {"coin": "BTC", "sentiment": 1},
                    {"coin": "ETH", "sentiment": 1},
                    {"coin": "XRP", "sentiment": -1}
                ],
                "reasoning": "Goldman Sachs' interest in Bitcoin and Ethereum indicates strong institutional adoption potential for these assets, suggesting positive price impact. Their explicit disinterest in XRP could negatively impact its market sentiment."
            }

            ## Example input
            "Bitcoin ETF ads spotted on China's Alipay payment app"

            ## Example output
            {
                "new_sentiment": [
                    {"coin": "BTC", "sentiment": 1}
                ],
                "reasoning": "The presence of Bitcoin ETF ads on Alipay indicates growing institutional interest in Bitcoin specifically. This news only affects Bitcoin and has no direct impact on other cryptocurrencies."
            }

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
    ) -> dict | NewsSentiment:
        """
        get sentiment from given text

        Args:
            text (str): text to get sentiment from
            output_format (Literal["dict", "NewsSentiment"], optional): output format. Defaults to "NewsSentiment".

        Returns:
            dict | NewsSentiment: the news sentiment
        """
        response: NewsSentiment = self.llm.structured_predict(
            NewsSentiment,
            prompt=self.prompt_template,
            news_story=text,
        )

        if output_format == "dict":
            return response.to_dict()
        else:
            return response


if __name__ == "__main__":
    from .config import OllamaConfig

    config = OllamaConfig()
    llm = OllamaSentimentExtractor(
        model_name=config.model_name,
    )

    examples = [
        "Bitcoin ETF ads spotted on China’s Alipay payment app",
        "Goldman Sachs wants to invest in Bitcoin and Ethereum, but not in XRP",
        "U.S. Supreme Court Lets Nvidia’s Crypto Lawsuit Move Forward",
        "Trump’s World Liberty Acquires ETH, LINK, and AAVE in $12M Crypto Shopping Spree",
    ]

    for example in examples:
        print(f"Example: {example}")
        response = llm.get_sentiment(example)
        # breakpoint()
        print(response)
