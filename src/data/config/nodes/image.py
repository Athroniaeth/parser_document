from dataclasses import dataclass

from src.data.config.node import NodeConfig



class ConfigImage(NodeConfig):
    """
    Configuration de la pipeline de l'image

    Args:
        dpi (int): Résolution de l'image retournée par PyMuPDF
    """
    folder_output: str = "02_raw_images"
    dpi: int = 300
