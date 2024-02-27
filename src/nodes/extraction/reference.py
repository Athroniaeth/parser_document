import itertools
import re
from typing import List

import rapidfuzz
import typer

from src.data.bbox import Bbox
from src.data.document import Document
from src.nodes.matching import match_list_box_regex, match_list_bbox, get_list_bbox_next_bbox

list_black_word = [
    "Feuille", "Echelle", "Section", "CERTIFICATION", "Qualité", "Support", "Tableau assemblage"
]


def extract_reference_info(document: Document, list_bbox: List[Bbox]) -> Document:
    """
    Extrait les information de la reference du document

    Args:
        document: Document sur lequel stocker l'année
        list_bbox: Liste de bounding list_bbox contenant le texte

    Returns:
        Document: Document avec la référence extraite
    """
    keyword_num = ["N°", "Numéro", "N"]
    keyword_order = ["d'Ordre ", "d Ordre ", "Ordre "]

    combined_keyword = itertools.product(keyword_num, keyword_order)
    keyword = list(map(lambda x: " ".join(x), combined_keyword))

    best_candidate = Bbox(0, 0, 0, 0, "", 0, 0, 0)

    list_regex = [
        r"\d{1,5}",  # Contiens un nombre de 1 à 5 chiffres
        r"\d{1,5}[a-z]",  # Contiens un nombre de 1 à 5 chiffres et une lettre à la fin
    ]

    custom_list_black_word = list_black_word + ["DEPARTEMENT", "COMMUNE", "EXTRAIT DU PLAN CADASTRAL", "Article",
                                                "Arpentage", "Commune", "Mutations pour", "Tournée pour", "Croquis de", "N  3520"]

    list_bbox_candidate = [bbox for bbox in list_bbox if bbox.x >= bbox.width_image // 2]
    bbox_order = match_list_bbox(
        list_bbox_candidate,
        keyword,
        list_black_word=custom_list_black_word,
        threshold=70,
        processor=rapidfuzz.utils.default_process
    )

    # Si une bbox d'ordre est trouvé
    if bbox_order:
        # Obtenir les bbox a côté de celle de la bbox d'ordre
        list_bbox = get_list_bbox_next_bbox(bbox_order, list_bbox, (0, 0.1, 2, 0.2))

        ###for bbox in list_bbox:
            ###typer.echo(f"[Reference] Candidat '{bbox.text}', '{bbox.x}', '{bbox.y}', '{bbox.confidence}'")

        """        # Chercher les bbox qui contiennent 7 caractères (peu importe lesquelles)
        list_bbox = match_list_box_regex(list_bbox, r"^.{1,7}$")

        for bbox in list_bbox:
            ###typer.echo(f"[Reference] Candidat REGEX '{bbox.text}', '{bbox.x}', '{bbox.y}', '{bbox.confidence}'")"""

    else:
        # Pas de filtre car on ne sait pas où chercher
        pass

    for regex in list_regex:
        # Chercher les bbox qui matchent le regex
        boxes = match_list_box_regex(list_bbox, regex)

        # Prend la bbox avec le plus grand score
        if len(boxes) > 0:
            best_candidate = max(boxes, key=lambda box: box.confidence)

            """if len(boxes) > 1:
                # Si il y a plus d'une bbox avec un nombre, prendre le plus proche de la médiane
                match_numbers = [int(re.search(r"\d{1,5}", box.text).group()) for box in boxes]
                index = np.argmin(np.abs(np.median(match_numbers) - match_numbers))
                best_candidate = boxes[index]"""

    # Netoyyer la réference (enlever les espaces, les caractères spéciaux, garder que les chiffres sauf si il y a une lettre à la fin) (\d{1,5})([a-z])?
    result = re.search(r"\d{1,5}[a-z]?", best_candidate.text)
    best_candidate.text = result.group() if result else ""

    ###typer.echo(f"[Reference] Candidat '{best_candidate.text}', '{best_candidate.confidence}'")
    if best_candidate.text:
        document.reference = best_candidate.text if best_candidate.text.isdecimal() else best_candidate.text[:-1]
        document.character = best_candidate.text if best_candidate.text[-1].isalpha() else ""

    return document
