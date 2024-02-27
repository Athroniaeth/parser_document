from dataclasses import dataclass


@dataclass
class Bbox:
    """
    Classe représentant une bounding box contenant du texte

    Attributes:
        x: position x de la bounding box
        y: position y de la bounding box
        width: largeur de la bounding box
        height: hauteur de la bounding box

        text: texte contenu dans la bounding box
        confidence: confiance de la bounding box

        height_image: hauteur de l'image
        width_image: largeur de l'image
    """
    x: int
    y: int

    width: int
    height: int

    text: str
    confidence: float

    height_image: int
    width_image: int
