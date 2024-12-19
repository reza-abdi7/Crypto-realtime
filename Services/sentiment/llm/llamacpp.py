from typing import Literal
from llama_cpp import Llama, LlamaGrammar
from llama_index.core.prompts import PromptTemplate
from base import BaseSentimentExtractor, NewsSentiment, SentimentOneCoin

# Get coin literals from SentimentOneCoin
COINS = SentimentOneCoin.model_fields["coin"].annotation.__args__

# Define the grammar for JSON output
grammar_string = f"""
root ::= "{{" ws news_field ws "," ws sentiment_field ws "}}"
news_field ::= "\\"news\\"" ws ":" ws "\\"" [^"]+ "\\""
sentiment_field ::= "\\"sentiment\\"" ws ":" ws "[" array_items? "]"
array_items ::= coin_object (ws "," ws coin_object)*
coin_object ::= "{{" ws "\\"coin\\"" ws ":" ws "\\"" coin "\\"" ws "," ws signal_type ws ":" ws signal_value ws "}}"
coin ::= {" | ".join(f'"{coin}"' for coin in COINS)}
signal_type ::= "\\"sentiment\\""
signal_value ::= "1" | "-1" | "0"
ws ::= " "*
"""


class LlamaCppSentimentExtractor(BaseSentimentExtractor):
    def __init__(
        self,
        model_path: str,
        temperature: float = 0.0,
        max_tokens: int = 256,
        n_ctx: int = 2048,
        n_threads: int = 8,
        repeat_penalty: float = 1.0,
        verbose: bool = False,
        penalize_nl: bool = False,
        escape_newlines: bool = True,
    ):
        self.llm = Llama(
            model_path=model_path,
            n_ctx=n_ctx,
            n_threads=n_threads,
            repeat_penalty=repeat_penalty,
            penalize_nl=penalize_nl,
            verbose=verbose,
        )
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.escape_newlines = escape_newlines
        self.grammar = LlamaGrammar.from_string(grammar_string, verbose=False)

        self.prompt_template = PromptTemplate(
            template="""You are an expert crypto financial analyst with deep knowledge of market dynamics and sentiment analysis.
            Analyze the following news story and determine its potential impact on crypto asset prices.
            Focus ONLY on coins that are directly mentioned or significantly impacted by the news.
            DO NOT include coins that are not relevant to the news content.

            Do not output data for a given coin if the news is not relevant to it.
            Output ONLY valid JSON without any markdown formatting or code block markers.

            ## Example input
            "Goldman Sachs wants to invest in Bitcoin and Ethereum, but not in XRP"

            ## Example output
            {{
                "news": "Goldman Sachs wants to invest in Bitcoin and Ethereum, but not in XRP",
                "sentiment": [
                    {{"coin": "BTC", "signal": 1}},
                    {{"coin": "ETH", "signal": 1}},
                    {{"coin": "XRP", "signal": -1}}
                ]
            }}

            ## Example input
            "Bitcoin ETF ads spotted on China's Alipay payment app"

            ## Example output
            {{
                "news": "Bitcoin ETF ads spotted on China's Alipay payment app",
                "sentiment": [
                    {{"coin": "BTC", "sentiment": 1}}
                ]
            }}

            News story to analyze:
            {news_story}

            ## Output (ONLY JSON, no markdown):"""
        )

    def get_sentiment(
        self,
        news_story: str,
        output_format: Literal["dict", "NewsSentiment"] = "NewsSentiment",
    ) -> NewsSentiment | dict:
        prompt = self.prompt_template.format(news_story=news_story)

        response: NewsSentiment = self.llm.create_chat_completion(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            top_p=0.95,  # Default from docs
            top_k=40,  # Default from docs
            min_p=0.05,  # Default from docs
            typical_p=1.0,  # Default from docs
            presence_penalty=0.0,  # Default from docs
            frequency_penalty=0.0,  # Default from docs
            repeat_penalty=1.0,  # Disable repetition
            tfs_z=1.0,  # Default from docs
            mirostat_mode=0,  # Default from docs
            mirostat_tau=5.0,  # Default from docs
            mirostat_eta=0.1,  # Default from docs
            grammar=self.grammar,
        )

        return response["choices"][0]["message"]["content"]


if __name__ == "__main__":
    from config import LlamaCppConfig
    import os

    # Create config with env file path
    config = LlamaCppConfig(
        _env_file=os.path.join(os.path.dirname(__file__), "llamacpp.env")
    )

    extractor = LlamaCppSentimentExtractor(
        model_path=config.model_path,
        temperature=0.0,
        max_tokens=256,
        n_threads=8,
        repeat_penalty=1.0,
        verbose=False,
        penalize_nl=False,
        escape_newlines=True,
    )

    examples = [
        "U.S. Supreme Court Lets Nvidia's Crypto Lawsuit Move Forward",
        "Trump's World Liberty Acquires ETH, LINK, and AAVE in $12M Crypto Shopping Spree",
    ]

    for example in examples:
        print(f"Example: {example}")
        response = extractor.get_sentiment(example)
        print(response)
