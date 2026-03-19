import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

# Create LOGS directory if it doesn't exist
LOGS_DIR = 'LOGS'
os.makedirs(LOGS_DIR, exist_ok=True)

# Configure logging with rotating file handler
log_filename = os.path.join(LOGS_DIR, 'variance_calculator.log')
rotating_handler = RotatingFileHandler(
    log_filename,
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5  # Keep 5 backup files
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        rotating_handler,
        logging.StreamHandler()  # Also log to console
    ]
)
logger = logging.getLogger(__name__)

MAX_SCORE = 100
MAX_SCORE_COUNT = 3

def _find_variance(scores: list[int]) -> float:
    """
    Compute the population variance of a list of integer scores.

    Args:
        scores: A non-empty list of integers (bool values are not permitted).

    Returns:
        The population variance of the input scores as a float.

    Raises:
        ValueError: If the input list is empty.
        TypeError: If the input is not a list 
        TypeError: If the list elements are not ints
    """
    # Type check input to ensure it is a list
    if not isinstance(scores, list):
        raise TypeError(f"scores must be a list, got {type(scores).__name__}")
    # Check the input is not empty
    if not scores:
        raise ValueError("scores must not be empty")

    total = 0 
    for score in scores: 
        if type(score) is not int:
            raise TypeError("All scores must be integers (bool is not allowed)")
        total += score

    n = len(scores)
    mean = total / n
    variance = sum((score - mean) ** 2 for score in scores) / n
    
    return variance

def _get_scores_from_user() -> list[int]:
    """
        Get score input from the user and return as a list of ints

        Args:
            NONE

        Returns:
            Scores in the form of a list of ints

        Raises:
            ValueError: If any of the input is not an int or not between 0 and 100
            ValueError: Only 3 scores are allowed, if more than 3 scores are provided, raise a ValueError
    """
    logger.info("Starting user input collection process")

    while True:
        raw = input("Enter scores separated by commas (e.g. 90, 85, 88): ")
        logger.debug(f"Raw user input: '{raw}'")

        try:
            scores = [int(item.strip()) for item in raw.split(",")]
            logger.debug(f"Parsed scores: {scores}")
        except ValueError as e:
            logger.warning(f"Invalid input parsing: {e}")
            print("Invalid input — please enter integers only, separated by commas.")
            continue

        if len(scores) > MAX_SCORE_COUNT:
            logger.warning(f"Too many scores provided: {len(scores)} > {MAX_SCORE_COUNT}")
            print(f"Only {MAX_SCORE_COUNT} scores are allowed.")
            continue

        invalid_scores = [score for score in scores if not (0 <= score <= MAX_SCORE)]
        if invalid_scores:
            logger.warning(f"Out-of-range scores detected: {invalid_scores}")
            print("Scores must be between 0 and 100 inclusive.")
            continue

        logger.info(f"Valid scores collected: {scores}")
        return scores


def find_variance_from_user_input() -> float:
    """
        Prompt the user for scores and return the population variance.
    
        Repeatedly prompts via stdin until valid comma-separated integers are
        entered, then computes and returns the population variance of those scores.
    
        Args:
            None
    
        Returns:
            The population variance of the user-provided scores as a float.
    
        Raises:
            TypeError: If the parsed scores list is not a list of integers.
            ValueError: If the parsed scores list is empty.
    """
    
    user_input = _get_scores_from_user()
    variance = _find_variance(user_input)

    return variance

if __name__ == "__main__":
    result = find_variance_from_user_input()
    print(f"Score variance: {result:.4f}")