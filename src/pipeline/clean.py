from pathlib import Path

import numpy


def pipeline_clean(image: numpy.ndarray) -> numpy.ndarray:
    """
    Clean the image to make it more understandable for the OCR

    Args:
        image: Image of the document

    Returns:
        Image: Image cleaned
    """
    return image
