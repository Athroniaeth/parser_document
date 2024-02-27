from typing import Callable, Dict

import numpy

from src.data.config.nodes.preprocess import ConfigPreprocess
from src.nodes.preprocess import binarization, grayscale, noise_reduction, skew_correction


def pipeline_preprocess(
        image: numpy.ndarray,
        config: ConfigPreprocess
) -> numpy.ndarray:
    """
    Preprocess the image to make it more understandable for the OCR

    Args:
        image: Image of the document

    Returns:
        Image: Image preprocessed
    """

    mapping = {
        config.active_grayscale: grayscale,
        config.active_binarization: binarization,
        config.active_skew_correction: skew_correction,
        config.active_noise_reduction: noise_reduction
    }

    # for activate, function in mapping.items():
    #     if activate:
    #         image = function(config, image)

    return grayscale(config, image)
