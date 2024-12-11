from config import config
from loguru import logger
from quixstreams import State

MAX_CANDLES_IN_STATE = config.max_candles_in_state


def update_candle(candle: dict, state: State) -> dict:
    """
    update the list of candles we have in our state using the latest candle

    if the latest candle corresponds to a new window and total number of candles
    is less than num_candles_in_state we just append it to the list
    if it corresponds to the same window, we replace the last candle in the list

    Args:
        candle (dict): latest candle
        state (State): state of the candles
        num_candles_in_state (int): number of candles to keep in state

    Returns:
        candles
    """
    candles = state.get('candles', default=[])
    if not candles:
        candles.append(candle)
    elif same_window(candle, candles[-1]):
        candles[-1] = candle
    else:
        candles.append(candle)

    if len(candles) > MAX_CANDLES_IN_STATE:
        candles.pop(0)

    # TODO: we should check the candles have no missing windows
    # This can happen for low volume pairs. In this case, we could interpoalte the missing windows

    logger.debug(f'Number of candles in state for {candle["pair"]}: {len(candles)}')

    # Update the state with the new list of candles
    state.set('candles', candles)

    return candle


def same_window(candle_1: dict, candle_2: dict) -> bool:
    """
    Checks if the candle is the same window as the last candle

    Args:
        candle_1 (dict): candle to check
        candle_2 (dict): last candle

    Returns:
        bool: True if the candle is the same window as the last candle
    """
    return (
        candle_1['window_start_ms'] == candle_2['window_start_ms']
        and candle_1['window_end_ms'] == candle_2['window_end_ms']
        and candle_1['pair'] == candle_2['pair']
    )
