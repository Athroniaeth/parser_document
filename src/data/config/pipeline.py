from pydantic import BaseModel

from src.data.config.nodes.correction import ConfigCorrection
from src.data.config.nodes.exctraction import ConfigExtraction
from src.data.config.nodes.image import ConfigImage

from src.data.config.node import NodeConfig
from src.data.config.nodes.ocr import ConfigOCR
from src.data.config.nodes.preprocess import ConfigPreprocess


class PipelineConfig(BaseModel):
    """
    Configuration du pipeline

    Args:
        image (NodeConfig): Dossier ou sera stocké les images
        preprocess (NodeConfig): Dossier ou sera stocké les images préprocessées
        ocr (NodeConfig): Dossier ou sera stocké les fichiers json des bbox
        correction (NodeConfig): Dossier ou sera stocké les images corrigées
        extraction (NodeConfig): Dossier ou sera stocké les fichiers csv des informations extraites
    """
    image: ConfigImage = ConfigImage()
    preprocess: ConfigPreprocess = ConfigPreprocess()
    ocr: ConfigOCR = ConfigOCR()
    correction: ConfigCorrection = ConfigCorrection()
    extraction: ConfigExtraction = ConfigExtraction()
