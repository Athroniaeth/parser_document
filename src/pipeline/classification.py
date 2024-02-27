from src.data.category import CategoryDocument
from src.data.document import Document


def pipeline_classification(document: Document) -> Document:
    """
    Extract the information from the bounding boxes

    Args:
        document: Document with the information extracted

    Returns:
        Document: Document with the information extracted
    """
    document.category = CategoryDocument.DMPC
    return document
