"""Matching functions for the pipeline."""
import itertools
import logging
import re
from typing import List, Optional, Callable, Tuple

import rapidfuzz
import typer
from rapidfuzz import fuzz, process

from src.data.bbox import Bbox




def get_list_bbox_next_bbox(
        bbox: Bbox,
        list_bbox: List[Bbox],
        matrix: Tuple[float, float, float, float] = (0, 0, 0, 0),
) -> List[Bbox]:
    """
    Get the list of bbox that are next to the bbox

    Args:
        bbox: Bbox to compare
        list_bbox: list of Bbox
        matrix: matrice de recherche (gauche, haut, droite, bas) la valeur 1 signifie qu'on cherche une bbox dans cette direction

    Returns:
        List[Bbox]: list of Bbox that are next to the bbox

    Examples:
        >>> matrix = (1, 1, 1, 1)  # gauche, haut, droite, bas
        >>> matrix = (1, 1, 1, 1)  # Cherche d'une bbox à gauche, à droite, en haut et en bas
        >>> matrix = (2, 0, 0, 0)  # Cherche d'une bbox à gauche
        ['bbox_2', 'bbox_3']
    """
    list_bbox_candidate = []

    for bbox_candidate in list_bbox:
        # Interval on x and y in common of the two bbox with multiply (percent of width or height) tolerance
        condition = (
            bbox.x - bbox.width * matrix[0] <= bbox_candidate.x <= bbox.x + bbox.width * matrix[2],
            bbox.y - bbox.height * matrix[1] <= bbox_candidate.y <= bbox.y + bbox.height * matrix[3],
        )

        if all(condition):
            list_bbox_candidate.append(bbox_candidate)

    return list_bbox_candidate

def match_list_box_regex(
        list_bbox: List[Bbox],
        regex: str,
        tolerance=0,
) -> List[Bbox]:
    """
    Matching list bbox for found text

    Args:
        list_bbox (List[Bbox]): list of Bbox objects
        regex (str): regex to match
        tolerance (int): tolerance for the length of the word

    Returns:
        Bbox: Bbox with the highest confidence with match_word

    Examples:
        >>> bbox_1 = Bbox(x=204, y=6, width=171, height=29, confidence=0.3, text="6463")
        >>> bbox_2 = Bbox(x=104, y=6, width=171, height=29, confidence=0.5, text="6463n")
        >>> bbox_3 = Bbox(x=104, y=6, width=171, height=29, confidence=0.5, text="xxxx")
        >>> list_bbox = [bbox_1, bbox_2, bbox_3]
        >>> regex = r"[0-9]{4}"

        >>> match_list_box_regex(list_bbox, regex)
        [Bbox(x=204, y=6, width=171, height=29, text='6463', confidence=0.3), Bbox(x=104, y=6, width=171, height=29, text='6463n', confidence=0.5)]

        >>> [bbox.text for bbox in match_list_box_regex(list_bbox, regex, 1)]
        ['6463', '6463n']

    """

    # For bbox with text '646n' and regex (number, length 4) and tolerance 1
    return [bbox for bbox in list_bbox if re.match(regex, bbox.text)]


def match_list_bbox(
        list_bbox: List[Bbox],
        match_word: List[str] or str,
        threshold: float = 70,

        list_black_word: Optional[List[str]] = None,
        threshold_black: float = 70,

        fuzz_function: Callable = fuzz.ratio,
        processor: rapidfuzz.utils = rapidfuzz.utils.default_process,
) -> Optional[Bbox]:
    """
    Matching list bbox for found text

    Args:
        list_bbox (List[Bbox]): list of Bbox objects
        match_word (str): word to match
        list_black_word (List[str]): list of black word
        threshold_black (float): threshold for black word
        fuzz_function (Callable): function to calculate the score
        processor (rapidfuzz.utils): function to process the string before comparing

    Returns:
        Bbox: Bbox with the highest confidence with match_word

    Examples:
        >>> bbox1 = Bbox(x=204, y=6, width=171, height=29, confidence=0.3, text="Bordeayx")
        >>> bbox2 = Bbox(x=104, y=6, width=171, height=29, confidence=0.5, text="Feuille")
        >>> list_bbox = [bbox2, bbox1]
        >>> match_word = "Bordeaux"

        >>> list_black_word = ["Feuille", "Echelle"]

        >>> match_list_bbox(list_bbox=list_bbox, match_word=match_word, list_black_word=list_black_word)
        Bbox(x=204, y=6, width=171, height=29, text='Bordeayx', confidence=0.3)
    """
    if isinstance(match_word, str):
        match_word = [match_word]

    list_word = [bbox.text for bbox in list_bbox]

    if list_black_word is not None:
        # Make score for each word
        scores_black = process.cdist(
            list_word,
            list_black_word,
            processor=processor,
            scorer=fuzz_function
        )

        # If the score is more than 80% we consider the word as a black word
        list_acceptable_word = scores_black.max(axis=1) < threshold_black  # List[True, False]

        # Reload the list of bbox and word
        list_bbox = [bbox for bbox, acceptable in zip(list_bbox, list_acceptable_word) if acceptable]
        list_word = [bbox.text for bbox in list_bbox]

    if len(list_word) == 0:
        logging.info(f"No bbox found for '{match_word}'")
        return None

    # Return the bbox with the highest confidence with match_word (one word)
    scores = process.cdist(
        list_word,
        match_word,
        processor=processor,
        scorer=fuzz_function
    )

    if len(scores) == 0:
        logging.info(f"No bbox found for '{match_word}'")
        return None

    index_bbox_match = scores.max(axis=1).argmax()
    index_text_match = scores.max(axis=0).argmax()
    score = scores.max(axis=1)[index_bbox_match]

    ###typer.echo(f"Found for matching with : '{list_word[index_bbox_match]}' (match with '{match_word[index_text_match]}') "
          ###f"with score '{score}' and threshold '{threshold}'")

    score = scores.max(axis=1)[index_bbox_match]
    if score < threshold:
        logging.info(f"No bbox found for '{match_word}' (score: {score}, threshold: {threshold})")
        return None

    return list_bbox[index_bbox_match]
