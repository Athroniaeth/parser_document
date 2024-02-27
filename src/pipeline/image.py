from pathlib import Path

import fitz
import numpy

from src.data.config.nodes.image import ConfigImage


def pipeline_image(document_path: Path, config: ConfigImage) -> numpy.ndarray:
    """
    Load the image from the document path

    Args:
        document_path: Path of the document
        config: Configuration of the pipeline

    Returns:
        Image: Image of the document
    """
    document: fitz.Document

    # noinspection PyUnresolvedReferences
    with fitz.open(document_path) as document:
        page = document.load_page(0)
        pix = page.get_pixmap(dpi=config.dpi, alpha=0)  # test 100, 125, 150, 200, 300, best it's 125
        numpy_array = numpy.frombuffer(pix.samples, dtype=numpy.uint8)
        numpy_array = numpy_array.reshape(pix.h, pix.w, pix.n)

    return numpy_array
