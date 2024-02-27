from functools import lru_cache
from typing import List

import numpy
from easyocr import easyocr

from src.data.bbox import Bbox


@lru_cache(maxsize=1)
def get_ocr():
    return easyocr.Reader(['fr'])


def pipeline_ocr(image: numpy.ndarray) -> List[Bbox]:
    """
    Extract the text from the image

    Args:
        image: Image of the document

    Returns:
        List[Bbox]: List of bounding boxes of the text
    """
    reader = get_ocr()
    result = reader.readtext(
        image,
        low_text=0.3,
        blocklist="=[].!@#$%^&*()_+{}|;,<>?ª~:;`•Z",
     )

    height_image, width_image = image.shape

    list_bbox = []
    for bbox in result:
        x, y, weight, height = int(bbox[0][0][0]), int(bbox[0][1][1]), int(bbox[0][2][0]), int(bbox[0][2][1])
        text, confidence = bbox[1], bbox[2]
        list_bbox.append(Bbox(x, y, weight, height, text, confidence, height_image, width_image))

    return list_bbox
