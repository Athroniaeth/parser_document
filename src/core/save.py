import json
from pathlib import Path
from typing import List, Optional

import cv2
import numpy
from PIL import Image

from src.data.bbox import Bbox


def save_image(path_save: Optional[Path], image: numpy.ndarray, document_name: str) -> None:
    """
    Save the image in the folder

    Args:
        path_save: Path to the folder
        image: Image to save in the folder
        document_name: Name of the document
    """
    if path_save is None:
        return

    image_pillow = Image.fromarray(image)
    image_pillow.save(path_save / f"{document_name}.png")


def save_list_bbox(path_save: Optional[Path], image: numpy.ndarray, list_bbox: List[Bbox], document_name: str) -> None:
    """
    Save the list of bounding boxes in the folder

    Args:
        config: Configuration of the application
        image: Image with the bounding boxes
        list_bbox: List of bounding boxes
        document_name: Name of the document
    """
    if path_save is None:
        return
    save_path = path_save / f"{document_name}.json"

    # Dump en JSON
    with open(save_path, 'w') as file:
        json.dump([bbox.__dict__ for bbox in list_bbox], file, indent=4, default=lambda x: x.__dict__)

    # Dump l'image avec le text des bbox
    for bbox in list_bbox:
        x, y, w, h = bbox.x, bbox.y, bbox.width, bbox.height
        cv2.rectangle(image, (x, y), (w, h), (0, 200, 50), 2)
        cv2.putText(image, bbox.text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 50), 2)

    save_image(path_save, image, document_name)
