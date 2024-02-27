from dataclasses import dataclass
from typing import Optional

from src.data.category import CategoryDocument


@dataclass
class Document:
    """
    Document class to represent a document in the dataset.

    Attributes:
        filename: nom du fichier (ex: 04006_000_00457C.pdf)
        category: catégorie du document (ex: DMPC, CROQUIS, ANONYME, ...)
        insee: code INSEE de la Commune (ex: 69120)
        prefix: préfixe de la Commune (ex: 000)
        year: année du document (ex: 1954)
        reference: Nombre de situant dans la réference du document (ex: 457)
        letter: lettre située (parfois) dans la réference du document (après le nombre) (ex: C)

    """
    filename: str
    category: CategoryDocument
    insee: str
    prefix: str
    year: int
    reference: int
    letter: str
