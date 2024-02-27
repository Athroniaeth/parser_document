from typing import List

from src.data.bbox import Bbox
from src.data.document import Document


def extract_year(document: Document, list_bbox: List[Bbox]) -> Document:
    """
    Extrait l'année du document

    Args:
        document: Document sur lequel stocker l'année
        list_bbox: Liste de bounding boxes contenant le texte

    Returns:
        Document: Document avec l'année extraite
    """
    return document
