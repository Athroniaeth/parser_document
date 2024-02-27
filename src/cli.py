import logging
from io import StringIO
from pathlib import Path
from typing import Annotated

import typer

from src import DATA_PATH
from src import PROJECT_PATH
from src.core.accuracy.document import calcul_accuracy
from src.core.load.ground_truth import load_ground_truth
from src.data.config.cli import Config
from src.data.dataset import Dataset
from src.process import monitor_process

app = typer.Typer(pretty_exceptions_enable=False, no_args_is_help=True)

log_stream = StringIO()
logging.basicConfig(stream=log_stream, level=logging.INFO)
formatter = logging.Formatter('%(levelname)s:%(name)s: %(message)s\n')
handler = logging.StreamHandler()
handler.setFormatter(formatter)


def _pipeline(
        config: Config,
        name_log: str = "log",
        name_scores: str = "scores",
        name_prediction: str = "predictions",
):
    """
    Mode principal du pipeline, lance le pipeline avec la configuration donnée.

    Args:
        config: Chemin du fichier de configuration
    """

    # Crée le chemin du fichier de log
    path_log = config.path_output / f"{name_log}.log"

    # Crée les chemins de sortie
    path_scores = config.path_output / f"{name_scores}.csv"
    path_predictions = config.path_output / f"{name_prediction}.csv"

    # Create the dataset from folder
    dataset = Dataset(config.path_input)

    # Charge le ground truth et vérifie ses données
    if config.path_ground_truth:
        ground_truth = load_ground_truth(dataset, config.path_ground_truth)

    # Lance l'application avec la barre de progression
    predictions = monitor_process(config, dataset)
    predictions.to_csv(path_predictions, index=False)

    # Calcul de la précision si un ground truth est fourni
    if config.path_ground_truth:
        # noinspection PyUnboundLocalVariable
        scores = calcul_accuracy(predictions, ground_truth)
        scores.to_csv(path_scores, index=False)

    # Sauvegarde les logs
    path_log.write_text(log_stream.getvalue())


@app.command()
def greed_search(path_folder: Annotated[str, typer.Argument()]):
    """
    Mode de recherche de la meilleure configuration du pipeline.
    """
    list_config = []
    logging.info("Starting the greed search pipeline")

    # Converti le chemin en Path
    path_folder = Path(path_folder)

    # Vérifie que les configurations sont valides
    for filepath in path_folder.glob("*.toml"):
        config = Config.from_toml(filepath)
        list_config.append(config)

    # Si un fichier de configuration avec un doublons
    have_duplicate = False
    for config in list_config:
        list_config_name = [other_config.name for other_config in list_config]
        condition = list_config_name.count(config.name) > 1
        if condition:
            have_duplicate = True
            ###typer.echo(f"Duplicate configuration : '{config.name}'")

    # Si un fichier de configuration avec un doublons en nom est trouvé
    if have_duplicate:
        raise ValueError("Duplicate configuration found")

    # Lance le pipeline pour chaque configuration
    for config in list_config:
        logging.info(f"Starting the pipeline with the configuration : '{config.name}'")
        _pipeline(config, name_scores=f"scores_{config.name}", name_prediction=f"predictions_{config.name}")


@app.command()
def pipeline(path_config: Annotated[str, typer.Argument()] = "config.toml"):
    """
    Mode principal du pipeline, lance le pipeline avec la configuration donnée.

    Args:
        path_config: Chemin du fichier de configuration
    """
    logging.info("Starting the pipeline")

    # Converti le chemin en Path
    path_config = Path(path_config)

    # Crée la configuration à partir du fichier toml
    config = Config.from_toml(PROJECT_PATH / path_config)

    # Lance le pipeline
    _pipeline(config)


if __name__ == "__main__":
    app()
