# LiteJsonDb : Votre base de données JSON légère de référence
![illustration](https://telegra.ph/file/374450a4f36c217b3a20b.jpg)
![Téléchargements PyPi](https://img.shields.io/pypi/dm/LiteJsonDb.svg) 
![Version du paquet PyPi](https://img.shields.io/pypi/v/LiteJsonDb.svg)
![Étoiles GitHub](https://img.shields.io/github/stars/codingtuto/LiteJsonDb)
![Forks GitHub](https://img.shields.io/github/forks/codingtuto/LiteJsonDb)

## :eyes: Aperçu

Salut ! Bienvenue sur **LiteJsonDb**, votre base de données conviviale et légère basée sur JSON. Inspirée par la simplicité et les capacités en temps réel de Firestore, LiteJsonDb facilite la gestion de vos données. Elle est dotée de fonctionnalités telles que le chiffrement, les sauvegardes et une gestion solide des erreurs, le tout sans effort supplémentaire.

## :thinking: Pourquoi LiteJsonDb ?

Soyons francs : parfois, vous n'avez pas besoin d'une configuration de base de données complexe. Peut-être construisez-vous un petit projet, un prototype rapide, ou vous voulez simplement un moyen simple de stocker et récupérer des données JSON. LiteJsonDb est là pour ces moments-là. C'est simple, efficace et fait le travail sans complications.

## :hammer_and_wrench: Fonctionnalités

- **Gestion facile des données** : Ajoutez, modifiez, récupérez et supprimez des données en quelques lignes de code.
- **Chiffrement des données** : Gardez vos données sécurisées avec un chiffrement optionnel. 
- **Sauvegarde et restauration** : Sauvegardes automatiques pour garder vos données en sécurité.
- **Sous-collections** : Organisez vos données dans des structures imbriquées ordonnées.
- **Gestion conviviale des erreurs** : Messages d'erreur utiles et colorés pour vous guider.

> [!NOTE]
> LiteJsonDb rend la gestion des données JSON simple et agréable. Que vous construisiez une petite application ou que vous ayez simplement besoin d'une solution de stockage de données légère, LiteJsonDb vous couvre. Profitez-en !

## :man_technologist: Installation

Commencer est super facile. Installez simplement le paquet via pip et vous êtes prêt :

```
pip install litejsondb
```

Une nouvelle version est disponible, tapez `pip install --upgrade litejsondb` pour mettre à jour

## :crystal_ball: Utilisation

### :white_check_mark: Configuration initiale

Tout d'abord, importez la classe `JsonDB` et initialisez votre base de données :

```python
import LiteJsonDb

# Initialiser la base de données avec le chiffrement activé
db = LiteJsonDb.JsonDB(crypted=True)
```

### 🤗 Opérations de base

#### :heavy_plus_sign: Définir des données

Ajouter des données est un jeu d'enfant. Utilisez simplement la méthode `set_data`. Si la clé existe déjà, vous obtiendrez un rappel amical d'utiliser `edit_data` à la place.

```python
# Définir des données sans données supplémentaires
db.set_data("posts")

# Définir des données avec des données supplémentaires
db.set_data("users/1", {"name": "Aliou", "age": 20})
db.set_data("users/2", {"name": "Coder", "age": 25})
```

#### :writing_hand: Modifier des données

Besoin de mettre à jour des données ? Pas de problème. Utilisez la méthode `edit_data`. Elle fusionne les nouvelles données avec les données existantes, donc rien n'est perdu.

```python
# Modifier des données
db.edit_data("users/1", {"name": "Alex"})
```

#### :ballot_box_with_check: Obtenir des données

Récupérer des données est aussi simple que possible. Utilisez la méthode `get_data`.

```python
# Obtenir des données
print(db.get_data("users/1"))  # Sortie : {'name': 'Alex', 'age': 20}
print(db.get_data("users/2"))  # Sortie : {'name': 'Coder', 'age': 25}
```

> [!TIP]
> Vous pouvez accéder directement à des données spécifiques en utilisant des chemins dans la méthode `get_data`. Par exemple, pour obtenir uniquement le nom de l'utilisateur, vous pouvez faire :
```python
print(db.get_data("users/1/name"))
```

Ici, vous obtenez le nom de l'utilisateur sans récupérer les autres parties des données.

#### :wastebasket: Supprimer des données

Besoin de supprimer quelque chose ? La méthode `remove_data` s'en occupe.

```python
# Supprimer des données
db.remove_data("users/2")
```

#### :package: Récupération complète de la base de données

Vous voulez tout voir ? Utilisez la méthode `get_db`. Définissez `raw=True` si vous voulez les données dans un format lisible.

```python
# Obtenir la base de données complète
print(db.get_db(raw=True))
```

### :file_folder: Travailler avec des sous-collections

## :file_folder: Sous-collections

Dans LiteJsonDb, les sous-collections sont un moyen d'organiser vos données de manière hiérarchique. Pensez-y comme des structures imbriquées qui vous permettent de regrouper des données connexes sous une clé parente. Cette fonctionnalité est particulièrement utile lorsque vous voulez gérer des relations de données complexes sans perdre la simplicité de JSON.

### :thinking: Que sont les sous-collections ?

Les sous-collections sont essentiellement des collections au sein de collections. Par exemple, si vous avez une collection principale d'utilisateurs, vous pourriez vouloir organiser leurs publications dans des sous-collections séparées. Voici comment vous pouvez travailler avec elles :

- **Définir des données de sous-collection** : Créer et peupler une sous-collection sous une clé parente spécifiée.
- **Modifier des données de sous-collection** : Mettre à jour des éléments existants dans une sous-collection.
- **Obtenir des données de sous-collection** : Récupérer les données stockées dans une sous-collection.
- **Supprimer des données de sous-collection** : Supprimer des éléments ou des sous-collections entières.

L'utilisation de sous-collections vous aide à maintenir une structure claire dans vos données, ce qui facilite leur gestion et leur interrogation.

#### :heavy_plus_sign: Définir des données de sous-collection

Organisez vos données avec des sous-collections. C'est simple comme bonjour.

```python
# Définir des données de sous-collection
db.set_subcollection("groups", "1", {"name": "Admins"})
```

#### :writing_hand: Modifier des données de sous-collection

Modifier des éléments dans une sous-collection ? Pas de souci.

```python
# Modifier des données de sous-collection
db.edit_subcollection("groups", "1", {"description": "Groupe admin"})
```

#### :ballot_box_with_check: Obtenir des données de sous-collection

Besoin de récupérer des sous-collections ou des éléments spécifiques ? Nous vous couvrons.

```python
# Obtenir des données de sous-collection
print(db.get_subcollection("groups"))

# Obtenir un élément personnalisé des données de sous-collection
print(db.get_subcollection("groups", "1"))
```

#### :wastebasket: Supprimer des données de sous-collection

Supprimer des éléments des sous-collections est tout aussi simple.

```python
# Supprimer des données de sous-collection
db.remove_subcollection("groups", "1")
```

## :bug: Gestion des erreurs

LiteJsonDb est conçu pour être utile. Voici quelques messages d'erreur amicaux et colorés pour vous guider :

- **Clé existante** : Si vous essayez de définir des données avec une clé existante, il vous suggérera d'utiliser `edit_data`.
- **Clé non trouvée** : Si une clé n'existe pas lorsque vous essayez d'obtenir ou de supprimer des données, il vous en informera avec un conseil sur la façon de procéder.
- **Problèmes de fichier** : S'il y a des problèmes de permission de fichier, il vous guidera sur la façon de les résoudre.

## :open_file_folder: Exemple de structure de projet

Voici à quoi pourrait ressembler votre projet si vous avez initialisé `LiteJsonDb` :

```
projet/
│
├── database/
│   ├── db.json
│   ├── db_backup.json
│   └── LiteJsonDb.log
└── votre_code.py
```

## :shipit: Exemple de `main.py`

Mettons tout cela ensemble avec un exemple de fichier `main.py` :

```python
import LiteJsonDb
  
# Initialiser la base de données avec le chiffrement activé
db = LiteJsonDb.JsonDB(crypted=True)

# Ajouter quelques données initiales
# Définir des données sans données supplémentaires
db.set_data("posts")

# Définir des données avec des données supplémentaires
db.set_data("users/1", {"name": "Aliou", "age": 20})
db.set_data("users/2", {"name": "Coder", "age": 25})

# Modifier des données existantes
db.edit_data("users/1", {"name": "Alex"})

# Récupérer et afficher des données
print(db.get_data("users/1"))
print(db.get_data("users/2"))

# Supprimer des données
db.remove_data("users/2")

# Récupérer la base de données complète
print(db.get_db(raw=True))

# Travailler avec des sous-collections
db.set_subcollection("groups", "1", {"name": "Admins"})
db.edit_subcollection("groups", "1", {"description": "Groupe admin"})
print(db.get_subcollection("groups"))
db.remove_subcollection("groups", "1")
```

## :memo: Comprendre `set_data` vs. Sous-collections

<details>
<summary>Cliquez pour développer</summary>

### `set_data`

La méthode `set_data` est utilisée pour ajouter ou mettre à jour des données à un chemin spécifique. Si la clé existe déjà, vous devrez utiliser `edit_data` pour la modifier. Cette méthode est idéale pour les paires clé-valeur simples ou les structures de données simples.

```python
# Définir des données
db.set_data("users/1", {"name": "Aliou", "age": 20})
```

### Sous-collections

Les sous-collections, en revanche, sont utilisées pour créer et gérer des structures imbriquées dans votre base de données. Elles vous permettent de regrouper des données connexes sous une clé parente, offrant une façon plus organisée de gérer des relations complexes. Les sous-collections sont essentiellement des collections au sein de collections.

```python
# Définir des données de sous-collection
db.set_subcollection("groups", "1", {"name": "Admins"})
```

### Différences clés

- **Structure** : `set_data` est utilisé pour des structures de données plates, tandis que les sous-collections permettent une organisation hiérarchique.
- **Utilisation** : Utilisez `set_data` pour des paires clé-valeur simples et `set_subcollection` lorsque vous avez besoin de collections imbriquées.
- **Organisation** : Les sous-collections aident à maintenir une structure claire et à regrouper des données connexes, facilitant la gestion et l'interrogation de relations complexes.

En comprenant ces différences, vous pouvez choisir la méthode appropriée pour vos besoins de gestion de données, assurant une base de données bien organisée et efficace.

</details>

## 🧾 TODO : Quoi de neuf pour Json2DB-Lite

Nous nous efforçons toujours d'améliorer Json2DB-Lite. Voici ce qui est dans notre viseur :

- [x] Ajouter le support du chiffrement des données pour sécuriser le contenu JSON.
- [x] Implémenter des sauvegardes automatiques pour assurer la sécurité des données.
- [x] Améliorer la gestion des erreurs avec des messages amicaux et colorés.
- [x] Ajout du langue française
- [ ] Implémenter des sauvegardes automatisées pour envoyer des données à un bot Telegram.
- [ ] Corriger tous les bugs découverts pour assurer un fonctionnement fluide.
- [ ] Atteindre 100 étoiles sur GitHub et célébrer en ajoutant plus de fonctionnalités géniales !

## :hugs: Contributions et Communauté
Nous accueillons les contributions, suggestions et retours pour rendre LiteJsonDb encore meilleur ! Si vous avez des idées d'améliorations ou si vous voulez corriger un bug, n'hésitez pas à :

- **Soumettre une Pull Request (PR)** : Contribuez avec de nouvelles fonctionnalités ou des corrections de bugs en créant une pull request. Vos changements aideront à améliorer LiteJsonDb pour tout le monde !
- **Signaler des problèmes** : Si vous rencontrez des bugs ou des problèmes, veuillez ouvrir un ticket dans le dépôt. Fournissez autant de détails que possible pour que nous puissions y remédier rapidement.
- **Suggérer des fonctionnalités** : Vous avez une idée pour une nouvelle fonctionnalité ? Faites-le nous savoir ! Nous sommes toujours ouverts aux suggestions sur la façon d'améliorer LiteJsonDb.

> Vos retours et contributions sont grandement appréciés et nous aident à maintenir LiteJsonDb en croissance et en amélioration.

## :heart: Dons et Support : Comment vous pouvez aider

Json2DB-Lite est un travail d'amour, et votre soutien peut faire une grande différence ! Si vous appréciez le projet et souhaitez montrer votre appréciation, voici quelques façons d'aider :

### Forker et Étoiler le Repo

L'une des meilleures façons de soutenir Json2DB-Lite est de forker le dépôt et de lui donner une étoile sur GitHub. C'est comme un "high-five" virtuel et nous aide à faire connaître le projet. De plus, cela nous montre que vous appréciez le travail que nous faisons !

### Envisager un don

Si vous vous sentez particulièrement généreux et souhaitez contribuer financièrement, nous en serions incroyablement reconnaissants. Les dons nous aident à couvrir les coûts et à maintenir le projet en bonne santé. Vous pouvez nous soutenir de la manière suivante :

- **PayPal** : Envoyez un don directement sur [mon compte PayPal](https://paypal.me/djibson35). Chaque petite contribution aide et est grandement appréciée !
- **Bitcoin** : Vous préférez la cryptomonnaie ? Vous pouvez également faire un don en utilisant Bitcoin à l'adresse suivante : `1Nn15EttfT2dVBisj8bXCnBiXjcqk1ehWR`.

> Votre soutien, que ce soit par une étoile, un fork ou un don, aide à maintenir Json2DB-Lite vivant et prospère. Merci d'être génial !

Bon codage ! :rocket:
