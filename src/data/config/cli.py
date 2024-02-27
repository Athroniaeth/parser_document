import tomllib
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Extra

from src.core.path import path_converter
from src.data.config.pipeline import PipelineConfig


@path_converter
class Config(BaseModel):
    """
    Configuration de l'application (CLI).

    Args:
        name (str): Nom de la configuration (permet de différencier les config dans le mode greedy search)
        limit_errors (int): Nombre d'erreurs tolérées dans le pipeline

        path_input (Path): Chemin d'accès du dossier d'entrée (PDF)
        path_output (Path): Chemin d'accès du dossier de sortie (CSV)
        path_analytic (Path): Chemin d'accès ou stocké les données pour l'analyse (images, json, ...)

        path_ground_truth (Optional[Path]): Chemin d'accès du fichier ground truth
    """
    pipeline: PipelineConfig = PipelineConfig()

    name: str = "main"
    limit_errors: int = 0

    path_input: Path = Path("data/pipeline/01_raw_documents")
    path_output: Path = Path("data/pipeline/07_output")

    path_analytic: Optional[Path] = Path("data/pipeline")
    path_ground_truth: Optional[Path] = Path("data/ground_truth.csv")

    class Config:
        extra = Extra.forbid

    @classmethod
    def from_toml(cls, path: Path):
        content = path.read_text()
        content_toml = tomllib.loads(content)

        return cls.model_validate(content_toml)
