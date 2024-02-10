# Parser Document
## Définition des nodes
* **Preprocess pdf**: Node convertissant une liste de document **List[Document]**(PyMuPDF) en une liste d'image **List[Image]**(Pillow).
* **Preprocess images**: Node convertissant une liste d'image **List[Image]**(Pillow) en une liste d'image **List[Image]**(Pillow) prétraité. Les images pretraité sont des images qui améliorent la capacité de "lecture" de l'OCR _(redimensionnement, la normalisation par exemple)_.
* **Clean img**: Node convertissant une liste d'image **List[Image]**(Pillow) en une liste d'image **List[Image]**(Pillow) nettoyé. Les images nettoyées sont des images qui ont été nettoyé de tout élément inutile _(réduction de bruit et l'amélioration du contraste, binarization, etc.)_.
* **OCR engine**: Node convertissant une liste d'image **List[Image]**(Pillow) en une liste de **List[Bbox]**(Custom) qui sont les coordonnées des boites englobantes des lignes de texte détecté.
* **Correction**: Node convertissant une liste d'image **List[Bbox]**(Custom) en une liste de **List[Bbox]**(Custom) qui sont les coordonnées des boites englobantes des lignes de texte corrigé. Le texte est corrigé en ayant précalculé une matrice de confusion de l'OCR pour permettre une correction des erreurs de l'OCR. Si nous avons le mot "H3llo" ou "HelIo" dans le texte, et que la matrice indique que l'OCR confond souvent le "3" avec le "e" et le "I" avec le "l", alors le mot sera corrigé en "Hello". Les fautes sont détecté grâce a un calcul de cohérence de lettre statistique basé sur un dictionnaire français.
* **Exctraction**: Node convertissant une liste d'image **List[Bbox]**(Custom) en une liste de **List[Bbox]**(Custom) qui sont les coordonnées des boites englobantes des lignes de texte extrait contenant des informations pertinentes. Les informations pertinentes sont des informations qui sont utiles pour l'analyse de document. Par exemple, si nous avons un document de facture, les informations pertinentes sont le montant, la date, le numéro de facture, etc. Ceux ci sont généralement trouvé en cherche des mots clés dans les bbox et en appliquant des filtres sur les Bbox qui sont à côté. Des techniques de segmentation peuvent être utilisé, et la Bbox la plus probable est sélectionné.
* **Classification**: Node convertissant une liste de **List[Bbox]**(Custom) en une sorite **Output** qui est une ligne du fichier csv de sortie. Celui-ci contiendra les informations extraites ainsi que la classification.

## Architecture du pipeline
Voici comment fonctionne le pipeline pour l'analyse des documents.
``` mermaid
sequenceDiagram
  autonumber
    
  Data->>Pipeline: Get raw documents
  Pipeline->>Nodes: Use preprocess pdf
  Nodes-->>Pipeline: Return images
  Pipeline-->>Data: Save in 02_raw_images
  Note left of Pipeline: Only with "analytic" mode
  
  Pipeline->>Nodes: Use preprocess images
  Nodes-->>Pipeline: Return preprocess images
  Pipeline-->>Data: Save in 03_preprocess_images
  Note left of Pipeline: Only with "analytic" mode
  
  Pipeline->>Nodes: Use clean img
  Nodes-->>Pipeline: Return clean images
  Pipeline-->>Data: Save in 04_clean_images
  Note left of Pipeline: Only with "analytic" mode
  
  Pipeline->>Nodes: Use OCR engine
  Nodes-->>Pipeline: Return list of bbox
  Pipeline-->>Data: Save in 05_extracted_bbox_img
  Note left of Pipeline: Only with "analytic" mode
  
  Pipeline->>Nodes: Use correction
  Nodes-->>Pipeline: Return list of bbox
  Pipeline-->>Data: Save in 07_detected_bbox_img
  Note left of Pipeline: Only with "analytic" mode
    
  Pipeline->>Nodes: Use exctraction
  Nodes-->>Pipeline: Return list of bbox
  Pipeline-->>Data: Save in 06_detected_bbox_img
  Note left of Pipeline: Only with "analytic" mode
  
  Pipeline->>Nodes: Use classification
  Nodes-->>Pipeline: Return output
  Pipeline->>Data: Save in output.csv
   
```



---

---

---
``` mermaid
graph LR
  A[Start] --> B{Error?};
  B -->|Yes| C[Hmm...];
  C --> D[Debug];
  D --> B;
  B ---->|No| E[Yay!];
```

---

``` mermaid
sequenceDiagram
  autonumber
  Alice->>John: Hello John, how are you?
  loop Healthcheck
      John->>John: Fight against hypochondria
  end
  Note right of John: Rational thoughts!
  John-->>Alice: Great!
  John->>Bob: How about you?
  Bob-->>John: Jolly good!
```

---

``` mermaid
classDiagram
  Person <|-- Student
  Person <|-- Professor
  Person : +String name
  Person : +String phoneNumber
  Person : +String emailAddress
  Person: +purchaseParkingPass()
  Address "1" <-- "0..1" Person:lives at
  class Student{
    +int studentNumber
    +int averageMark
    +isEligibleToEnrol()
    +getSeminarsTaken()
  }
  class Professor{
    +int salary
  }
  class Address{
    +String street
    +String city
    +String state
    +int postalCode
    +String country
    -validate()
    +outputAsLabel()  
  }
```

???+ note

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.