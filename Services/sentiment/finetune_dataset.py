import json
import random
import os
import requests
import rarfile
from typing import Literal
from pathlib import Path

import pandas as pd

instruction = """
You are an expert crypto financial analyst with deep knowledge of market dynamics and sentiment analysis.
Analyze the following news story and determine its potential impact on crypto asset prices.
Focus on both direct mentions and indirect implications for each asset.

Do not output data for a given coin if the news is not relevant to it.

## Example input news story
"Goldman Sachs wants to invest in Bitcoin and Ethereum, but not in XRP"

## Example output
[
    {"coin": "BTC", "signal": 1},
    {"coin": "ETH", "signal": 1},
    {"coin": "XRP", "signal": -1},
]
"""


def download_dataset(url: str, save_path: str) -> str:
    """
    Download the dataset from the given URL and save it to the specified path.

    Args:
        url: URL to download the dataset from
        save_path: Path to save the downloaded file

    Returns:
        Path to the downloaded file
    """
    print(f"Downloading dataset from {url}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    return save_path


def extract_dataset(rar_path: str, extract_path: str) -> str:
    """
    Extract the RAR dataset to the specified path.

    Args:
        rar_path: Path to the RAR file
        extract_path: Path to extract the contents to

    Returns:
        Path to the extracted CSV file
    """
    print(f"Extracting dataset from {rar_path}...")
    os.makedirs(extract_path, exist_ok=True)

    with rarfile.RarFile(rar_path) as rf:
        rf.extractall(extract_path)

    # Find the CSV file in the extracted contents
    csv_files = list(Path(extract_path).rglob("*.csv"))
    if not csv_files:
        raise FileNotFoundError("No CSV file found in the extracted contents")

    return str(csv_files[0])


def prepare_dataset(
    url: str = "https://github.com/soheilrahsaz/cryptoNewsDataset/raw/refs/heads/main/CryptoNewsDataset_csvOutput.rar",
) -> str:
    """
    Download and prepare the dataset for fine-tuning.

    Args:
        url: URL to download the dataset from

    Returns:
        Path to the prepared CSV file
    """
    data_dir = "data"
    rar_path = os.path.join(data_dir, "dataset.rar")
    extract_path = os.path.join(data_dir, "extracted")

    # Download if not exists
    if not os.path.exists(rar_path):
        download_dataset(url, rar_path)

    # Extract if not already extracted
    csv_files = list(Path(extract_path).rglob("*.csv"))
    if not csv_files:
        return extract_dataset(rar_path, extract_path)
    return str(csv_files[0])


def generate_dataset(
    model_provider: Literal["claude", "ollama"],
    n: int,
    input_file: str = None,
    output_file: str = "finetune_dataset.jsonl",
):
    """
    Generate a dataset of (instruction, input, output) tuples to do
    Supervised Fine Tuning.

    Args:
        model_provider: The model provider to use.
        n: The number of news stories to generate.
        input_file: The file to read the news stories from. If None, downloads and uses the default dataset.
        output_file: The file to write the dataset to.

    Returns:
        None
    """
    # If no input file specified, download and prepare the dataset
    if input_file is None:
        input_file = prepare_dataset()

    # load dataset
    df = pd.read_csv(input_file)
    news = df["title"].tolist()

    # random sample of n news
    news = random.sample(news, min(n, len(news)))

    # llm
    from llms.factory import get_llm

    llm = get_llm(model_provider=model_provider)

    from tqdm import tqdm

    # Create output directory if it doesn't exist
    os.makedirs(
        os.path.dirname(output_file) if os.path.dirname(output_file) else ".",
        exist_ok=True,
    )

    with open(output_file, "w", encoding="utf-8") as f:
        for news_item in tqdm(news):
            try:
                signals = llm.get_signal(news_item)
                output = {
                    "instruction": instruction,
                    "input": news_item,
                    "output": signals.model_dump_json(),
                    "teacher_model_name": llm.model_name,
                }
                f.write(json.dumps(output) + "\n")
            except Exception as e:
                print(f"Error processing news item: {e}")
                continue


if __name__ == "__main__":
    from fire import Fire

    Fire(generate_dataset)
