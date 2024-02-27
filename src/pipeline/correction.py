from typing import List

from src.data.bbox import Bbox


def pipeline_correction(list_bbox: List[Bbox]) -> List[Bbox]:
    """
    Correct the text extracted from the image

    Args:
        list_bbox: List of bounding boxes of the text

    Returns:
        List[Bbox]: List of corrected bounding boxes of the text
    """
    return list_bbox
