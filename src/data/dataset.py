from dataclasses import dataclass
from pathlib import Path
from typing import Generator


@dataclass
class Dataset:
    """
    Dataset class to handle the documents in a folder

    Attributes:
        path: Path of the folder
        length: Number of documents in the folder
        pattern: Pattern to filter the documents

    Methods:
        get_documents: Generator of documents in the folder

    Raises:
        FileNotFoundError: If the path does not exist
        NotADirectoryError: If the path is not a directory
        FileNotFoundError: If no document is found with the pattern

    Examples:
        >>> path = Path("path/to/folder")
        >>> dataset = Dataset(path)
        >>> for document in dataset.get_documents():
        >>>     print(document)
    """
    path: Path
    length: int
    pattern: str

    def __init__(self, path: Path, pattern="*.pdf"):
        # Compte le nombre de documents dans le dossier
        length = sum(1 for _ in path.glob(pattern))

        # Vérifie que le chemin existe
        if not path.exists():
            raise FileNotFoundError(f"The path does not exist '{path}'")

        # Vérifie que le chemin est un dossier
        if not path.is_dir():
            raise NotADirectoryError(f"The path is not a directory '{path}'")

        # Vérifie que le dossier contient des documents
        if length == 0:
            raise FileNotFoundError(f"No document found with '{pattern}' pattern in '{path}'")

        self.path = path
        self.length = length
        self.pattern = pattern

    def get_documents(self) -> Generator[Path, None, None]:
        """
        Generator of documents in the folder

        Returns:
            Generator[Path, None, None]: Generator of documents in the folder
        """
        for document in self.path.glob(self.pattern):
            yield document
