from pathlib import Path
from typing import List

from src.data.bbox import Bbox
from src.data.category import CategoryDocument
from src.data.document import Document
from src.nodes.extraction.commune import extract_commune_info
from src.nodes.extraction.reference import extract_reference_info
from src.nodes.extraction.year import extract_year


def pipeline_extraction(document_name: str, list_bbox: List[Bbox]) -> Document:
    """
    Extract the information from the bounding boxes

    Args:
        document_name: Name of the document
        list_bbox: List of bounding boxes of the text

    Returns:
        Document: Document with the information extracted
    """
    document = Document(
        filename=document_name,
        category=CategoryDocument.UNDEFINED,
        insee="",
        prefix="000",  # Valeur la plus probable
        year=1957,  # Valeur la plus probable
        reference=0,
        letter="",  # Valeur la plus probable
    )

    document = extract_reference_info(document, list_bbox)  # reference / letter
    document = extract_commune_info(document, list_bbox)  # insee / prefix
    document = extract_year(document, list_bbox)  # year

    return document
