from dataclasses import dataclass

from src.data.config.node import NodeConfig



class ConfigPreprocess(NodeConfig):
    """
    Configuration de la pipeline de l'image

    Args:
        active_upscale (bool): Upscale the image
        active_grayscale (bool): Convert the image to grayscale
        active_noise_reduction (bool): Reduce the noise of the image
        active_binarization (bool): Binarize the image
        active_skew_correction (bool): Correct the skew of the image
        active_normalization (bool): Normalize the image
        active_thinning (bool): Thinning the image
    """
    folder_output: str = "03_preprocess_images"

    active_upscale: bool = False,
    active_grayscale: bool = True,
    active_noise_reduction: bool = False,
    active_binarization: bool = False,
    active_skew_correction: bool = False,
    active_normalization: bool = False,
    active_thinning: bool = False,
