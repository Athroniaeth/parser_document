import cv2
import numpy

from src.data.config.nodes.preprocess import ConfigPreprocess


def upscale(config: ConfigPreprocess, image: numpy.ndarray) -> numpy.ndarray:
    """
    Upscale the image to make it more understandable for the OCR

    Args:
        image: Image of the document

    Returns:
        Image: Image upscaled
    """
    return cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)


def grayscale(config: ConfigPreprocess, image: numpy.ndarray) -> numpy.ndarray:
    """
    Convert the image to grayscale to make it more understandable for the OCR

    Args:
        image: Image of the document

    Returns:
        Image: Image in grayscale
    """
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)


def noise_reduction(config: ConfigPreprocess, image: numpy.ndarray) -> numpy.ndarray:
    """
    Reduce the noise of the image to make it more understandable for the OCR

    Args:
        image: Image of the document

    Returns:
        Image: Image with the noise reduced
    """
    return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)


def binarization(config: ConfigPreprocess, image: numpy.ndarray) -> numpy.ndarray:
    """
    Binarize the image to make it more understandable for the OCR

    Args:
        image: Image of the document

    Returns:
        Image: Image binarized
    """
    adaptive_threshold_mean = cv2.adaptiveThreshold(
        image,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        5,
        6
    )

    return adaptive_threshold_mean


def skew_correction(config: ConfigPreprocess, image: numpy.ndarray) -> numpy.ndarray:
    """
    Correct the skew of the image to make it more understandable for the OCR

    Args:
        image: Image of the document

    Returns:
        Image: Image with the skew corrected
    """
    thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    coords = numpy.column_stack(numpy.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated


def normalization(config: ConfigPreprocess, image: numpy.ndarray) -> numpy.ndarray:
    """
    Normalize the image to make it more understandable for the OCR

    Args:
        image: Image of the document

    Returns:
        Image: Image normalized
    """
    return cv2.normalize(image, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)


def thinning(config: ConfigPreprocess, image: numpy.ndarray) -> numpy.ndarray:
    """
    Thinning the image to make it more understandable for the OCR

    Args:
        image: Image of the document

    Returns:
        Image: Image thinned
    """
    kernel = numpy.ones((5, 5), numpy.uint8)
    erosion = cv2.erode(image, kernel, iterations=1)
    return erosion
