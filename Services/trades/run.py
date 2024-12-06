import loguru as logger

def main():
    """
    reads trades from the kraken API and push them to kafka topics.
    
    it does 2 things:
    1. reads trades from the kraken API
    2. push the trades to kafka topic.
    
    Args:
        None

    Returns:
        None
    """
    logger.info("Starting trades service")
    


if __name__ == "__main__":
    main()
