""" Fichier contenant toutes les barres de progression personnalisées pour différents outils. """

from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn, TimeElapsedColumn

from src.core.progress.columns.iteration import IterationsPerSecondColumn

pipeline_progress = Progress(
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    IterationsPerSecondColumn(),
    TaskProgressColumn(),
    TimeRemainingColumn(),
    TimeElapsedColumn(),

)
