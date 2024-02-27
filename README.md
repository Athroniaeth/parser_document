# Parser Document
## 1. Introduction
Ceci est une application servant de pipeline pour la lecture et l'extraction d'information de document cadastraux. 

## 2. Installation
Il vous faudra installer les dépendances suivantes pour faire fonctionner l'application. 
* Miniconda
* WSL (Ubuntu 22.04)

Pour installer l'application, il suffit de cloner le repository et d'installer les dépendances. 
```bash
git clone XXX_XXX_XXX
cd XXX_XXX_XXX
```

Créez un environnement conda et installez les dépendances. 
```bash
conda create -f environment.yml
conda activate geofoncier
```

Normalement, vous devriez être pouvoir voir '(geofoncier)' en ouvrant un nouveau terminal en début de ligne. 
Cela signifie que vous êtes dans l'environnement conda.

Maintenant, vous pouvez installer les dépendances python.
```bash
pip install -r requirements.txt
```

## 3. Utilisation
Pour utiliser l'application, il suffit de lancer le script principal. 
```bash
python main.py
```