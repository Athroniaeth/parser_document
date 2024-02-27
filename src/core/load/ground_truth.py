from pathlib import Path

import pandas

from src.data.dataset import Dataset


def load_ground_truth(dataset: Dataset, path_ground_truth: Path) -> pandas.DataFrame:
    """
    Charge le ground truth et vérifie ses données.

    Args:
        dataset: Dataset des documents à traiter
        path_ground_truth: Chemin du fichier ground truth

    Returns:
        pandas.DataFrame: Le dataframe du ground truth
    """

    # Vérifie que le fichier ground truth existe
    if not path_ground_truth.exists():
        raise FileNotFoundError(f"Le fichier ground truth n'existe pas : '{path_ground_truth.absolute()}'")

    # Charge le ground truth, enlève la colonne 'comment'
    ground_truth = pandas.read_csv(path_ground_truth, delimiter=";")
    ground_truth = ground_truth.fillna("")
    ground_truth = ground_truth.drop(columns=["comment"])

    # Obtient la liste des fichiers dans le dataset (car c'est un générateur)
    list_files = list(path.name for path in dataset.get_documents())

    # Crée un dataframe avec les noms des fichiers
    dataframe_files = pandas.DataFrame(list_files, columns=["filename"])

    # Crée la matrice (bool) des PDF (dataset) presents
    dataset_matrix_present = dataframe_files["filename"].isin(ground_truth["filename"])

    # Inverse la matrice pour obtenir les fichiers absents
    dataset_matrix_missing = ~dataset_matrix_present

    # Calcule le pourcentage de fichiers absents
    number_missing = dataset_matrix_missing.sum()  # Todo : sum(1 for absent in dataset_matrix_missing if absent)
    percentage_missing = number_missing / dataframe_files.shape[0] * 100

    # Si des fichiers sont absents, retourne les PDFs manquant (dataset)
    if percentage_missing > 0:
        # Obtient les nom des fichiers absents
        list_lines_missing = dataframe_files[dataset_matrix_missing]

        # Converti le dataframe crée en string pour l'afficher
        string_list_lines_missing = list_lines_missing.dropna().to_string(index=False, header=False)

        raise ValueError(
            f"Des PDF dans le Dataset ne sont pas dans le ground_truth ({percentage_missing:.2f}%)\n"
            f"Voici les lignes concernées:\n{string_list_lines_missing}"
        )

    return ground_truth
