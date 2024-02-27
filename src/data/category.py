from enum import StrEnum


class CategoryDocument(StrEnum):
    """
    Enumerates the different categories of documents.

    Notes:
        Undefined is the category given if
        the document category is not recognized.
    """
    UNDEFINED = "UNDEFINED"

    DMPC = "DMPC"
    CROQUIS = "CROQUIS"
    ANONYME = "ANONYME"
