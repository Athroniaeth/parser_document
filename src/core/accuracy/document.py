import logging
from pathlib import Path

import pandas
import typer

from src.data.category import CategoryDocument
from src.data.document import Document


def calcul_accuracy(
        predictions: pandas.DataFrame,
        ground_truth: pandas.DataFrame,
) -> pandas.DataFrame:
    """
    Calcul de la précision des prédictions par rapport au ground truth.

    Notes:
        Le dataframe renvoyée contiendra les mêmes colonnes, mais remplacera
        les valeurs par des 1 si la prédiction est correcte, sinon 0. Cela permet
        de calculer la précision de chaque colonne, ligne, ou du dataframe entier.

    Args:
        predictions (pd.DataFrame): Le dataframe contenant les prédictions.
        ground_truth (pd.DataFrame): Le dataframe contenant la vérité terrain.

    Returns:
        pd.DataFrame: Le dataframe contenant les scores de précision.

    Examples:

        filename | year | commune | ...
        - - - - - - - - - - - - - - - -
           1.jpg |    1 |       0 | ...
           2.jpg |    1 |       1 | ...
    """

    # Fusionne les deux Dataframes, '_pred' pour les prédictions, '_truth' pour la vérité terrain
    merged_dataframe = predictions.merge(ground_truth, on="filename", suffixes=("_pred", "_truth"))

    # Créer le DataFrame des Scores
    score_df = pandas.DataFrame()
    score_df['filename'] = merged_dataframe['filename']

    not_calcul = {
        CategoryDocument.CROQUIS: ['letter'],
        CategoryDocument.DMPC: ['year'],
        CategoryDocument.ANONYME: ['year'],

    }

    for col in list(Document.__annotations__.keys())[:]:
        if col != 'filename':
            score_df[col] = merged_dataframe[col + '_pred'] == merged_dataframe[col + '_truth']
            score_df[col] = score_df[col].astype(int)

    # Calcul le score en ignorant les colonnes pour X categories
    for category, columns in not_calcul.items():
        score_df_category = score_df.drop(columns=columns)

        # Filtre la colonne 'category' pour ne garder que la catégorie actuelle
        category_df = ground_truth[ground_truth['category'] == category]
        score_df_category = score_df_category[score_df_category['filename'].isin(category_df['filename'])]

        # Affiche le score moyen global (print)
        avg_global = score_df_category.drop(columns='filename').mean().mean() * 100
        ###typer.echo(f"[{category}] Global Accuracy: {avg_global:.2f}%")

        # Affiche le score moyen par colonne (print)
        avg_per_columns = (score_df_category.drop(columns='filename').mean() * 100).to_dict()
        ###typer.echo(f"[{category}] Accuracy per columns: {avg_per_columns}")

    # Affiche le score moyen global (print)
    avg_global = score_df.drop(columns='filename').mean().mean() * 100
    # Affiche le score moyen par colonne (print)
    avg_per_columns = (score_df.drop(columns='filename').mean() * 100).to_dict()
    """# Affiche le score moyen par categorie (print)
    for category in ground_truth['category'].unique():
        category_df = ground_truth[ground_truth['category'] == category]
        score_df_category = score_df[score_df['filename'].isin(category_df['filename'])]
        score_df_category = score_df_category.drop(columns='filename')
        avg_per_category = score_df_category.mean().mean() * 100 or 0.0
        logging.info(f"Accuracy for category {category}: {avg_per_category}")"""

    ###typer.echo(f"Global Accuracy: {avg_global:.2f}%")
    ###typer.echo(f"Accuracy per columns: {avg_per_columns}")

    # Affiche le score moyen global (sans category
    avg_global = score_df.drop(columns=['filename', 'category']).mean().mean() * 100
    # Affiche le score moyen par colonne (print)
    avg_per_columns = (score_df.drop(columns=['filename', 'category']).mean() * 100).to_dict()

    ###typer.echo(f"Global Accuracy: {avg_global:.2f}%")
    ###typer.echo(f"Accuracy per columns: {avg_per_columns}")

    return score_df


def calculate_similarity(row: pandas.Series) -> float:
    total = 0
    match = 0
    for col in row.index:
        if col != 'filename':
            total += 1
            if row[col + '_pred'] == row[col + '_truth']:
                match += 1
    return (match / total) * 100
