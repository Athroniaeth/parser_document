import logging
from dataclasses import asdict
from pathlib import Path
from typing import Optional

import pandas
import typer

from src.core.progress.bar import pipeline_progress
from src.core.save import save_image, save_list_bbox
from src.data.config.cli import Config
from src.data.config.node import NodeConfig
from src.data.dataset import Dataset
from src.data.document import Document
from src.pipeline.classification import pipeline_classification
from src.pipeline.correction import pipeline_correction
from src.pipeline.exctraction import pipeline_extraction
from src.pipeline.image import pipeline_image
from src.pipeline.ocr import pipeline_ocr
from src.pipeline.preprocess import pipeline_preprocess


def _create_path_from_config(config: Config, config_node: NodeConfig) -> Optional[Path]:
    if config.path_analytic:
        return config.path_analytic / config_node.folder_output
    return None


def process(config: Config, document_path: Path) -> Document:
    """
    Lance le pipeline sur un document

    Args:
        config: Configuration de l'application
        document_path: Chemin du document à traiter

    Returns:
        Document: Document avec les informations extraites
    """
    document_stem = document_path.stem
    document_name = document_path.name  # with extension
    logging.info(f"Processing the document : '{document_stem}'")

    # Todo : Refactoriser le code, transformer monitor_process, process en classe MonitorPipeline, Pipeline, Node, etc..
    image = pipeline_image(document_path, config.pipeline.image)
    path = _create_path_from_config(config, config.pipeline.image)
    save_image(path, image, document_stem)

    image = pipeline_preprocess(image, config.pipeline.preprocess)
    path = _create_path_from_config(config, config.pipeline.preprocess)
    save_image(path, image, document_stem)

    list_bbox = pipeline_ocr(image)  # , config.pipeline.ocr)
    path = _create_path_from_config(config, config.pipeline.ocr)
    save_list_bbox(path, image, list_bbox, document_stem)

    list_bbox = pipeline_correction(list_bbox)
    path = _create_path_from_config(config, config.pipeline.correction)
    save_image(path, image, document_stem)

    document = pipeline_extraction(document_name, list_bbox)  # , config.pipeline.extraction)
    document = pipeline_classification(document)

    logging.info(f"Document finished processing : '{document_path.name}'")

    avg_confidence = sum([bbox.confidence for bbox in list_bbox]) / len(list_bbox)
    ###typer.echo(f"Average confidence : {avg_confidence:.2f}")
    ###typer.echo(f"Text detected : {[bbox.text for bbox in list_bbox[:8]]}")

    return document


def monitor_process(
        config: Config,
        dataset: Dataset,

) -> pandas.DataFrame:
    """
    Monitor the process of the application with a progress bar

    Args:
        config: Config file of the application
        dataset: Dataset of documents to process
    """
    list_exceptions = []

    # Get generator of documents (less memory)
    generator_document = dataset.get_documents()

    # Ajouter la tâche à la barre de progression
    task = pipeline_progress.add_task("Processing...", total=dataset.length)

    # Créer un dataframe vide (Reprend les colonnes de Document)
    columns = list(Document.__annotations__.keys())
    dataframe = pandas.DataFrame(columns=columns)

    # Afficher la barre de progression
    with pipeline_progress:

        # Pour chaque document
        for path_document in generator_document:
            try:
                # Lance l'application
                output = process(config, path_document)
                logging.info(f"Document '{path_document.name}' processed")

                # On sauvegarde le path_document
                line_data = asdict(output)
                df_dictionary = pandas.DataFrame([line_data])
                dataframe = pandas.concat([dataframe, df_dictionary], ignore_index=True)

                logging.info(f"Document '{path_document.name}' saved")
            except KeyboardInterrupt as exception:
                # Si l'utilisateur interrompt le processus, arrête le pipeline
                logging.error(f"Pipeline interrupted by the user")
                break
            except Exception as exception:
                # Ajoute l'erreur à la liste
                list_exceptions.append(exception)
                logging.error(f"Error processing the path_document '{path_document.name}': {exception}")

            finally:
                # Mettre à jour la barre de progression
                pipeline_progress.update(task, description=f"Processing {path_document.name[0:14]}..", advance=1)

                # Obtient le nombre d'erreurs
                number_errors = len(list_exceptions)
                conditions = (
                    config.limit_errors < number_errors,  # Si le nombre d'erreurs tolérées atteint
                    config.limit_errors != -1,  # Si l'utilisateur a spécifié un nombre d'erreurs tolérées
                )

                if all(conditions):
                    logging.error(f"Too many errors, stopping the pipeline: {number_errors} errors")
                    raise ExceptionGroup("Too many errors, stopping the pipeline", list_exceptions)

    return dataframe
