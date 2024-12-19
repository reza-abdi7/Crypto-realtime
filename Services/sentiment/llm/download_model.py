import huggingface_hub
from pathlib import Path
import fire


def download_model(
    model_id: str = "TheBloke/Llama-2-7B-Chat-GGUF",
    filename: str = "llama-2-7b-chat.Q4_K_M.gguf",
    models_dir: str = "models",
) -> str:
    """
    Download a model from Hugging Face Hub.

    Args:
        model_id: The Hugging Face model ID (e.g., 'TheBloke/Llama-2-7B-Chat-GGUF')
        filename: The specific model file to download (e.g., 'llama-2-7b-chat.Q4_K_M.gguf')
        models_dir: Directory to store models

    Returns:
        str: Path to the downloaded model file
    """
    # Create models directory if it doesn't exist
    models_path = Path(models_dir)
    models_path.mkdir(exist_ok=True)

    print(f"Downloading {filename} from {model_id}...")

    # Download the model
    model_path = huggingface_hub.hf_hub_download(
        repo_id=model_id,
        filename=filename,
        local_dir=models_path,
        local_dir_use_symlinks=False,
    )

    print(f"Model downloaded successfully to: {model_path}")
    return model_path


if __name__ == "__main__":
    fire.Fire(download_model)
