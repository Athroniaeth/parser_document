import statistics
from collections import deque
from typing import Deque

from rich.progress import ProgressColumn, Task


class IterationsPerSecondColumn(ProgressColumn):
    """
    Affiche la vitesse de traitement en it/s

    Notes:
        Si la vitesse n'est pas disponible, on affiche 0 it/s
        Si la vitesse est supérieure à 1, on affiche la vitesse en it/s
        Sinon, on affiche la vitesse en s/it
    """
    deque_speed: Deque[float] = deque(maxlen=100)

    def render(self, task: Task) -> str:
        speed = task.speed

        # Si la vitesse n'est pas disponible, on affiche 0 it/s
        if speed is None:
            return "0 it/s"

        self.deque_speed.append(speed)
        speed = statistics.median(self.deque_speed)

        # On affiche la vitesse en it/s
        if speed > 1:
            return f"{speed:.2f} it/s"

        # On affiche la vitesse en s/it
        return f"{1/speed:.2f} s/it"
