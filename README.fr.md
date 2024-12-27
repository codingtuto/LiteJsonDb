# LiteJsonDb : Votre base de données JSON légère de référence
![illustration](https://telegra.ph/file/374450a4f36c217b3a20b.jpg)
![Téléchargements PyPi](https://img.shields.io/pypi/dm/LiteJsonDb.svg)
![Version du package PyPi](https://img.shields.io/pypi/v/LiteJsonDb.svg)
![Étoiles GitHub](https://img.shields.io/github/stars/codingtuto/LiteJsonDb)
![Forks GitHub](https://img.shields.io/github/forks/codingtuto/LiteJsonDb)

---

[![Voir la documentation en Français](https://img.shields.io/badge/Documentation-Fran%C3%A7ais-blue)](./README.fr.md)
[![Wiki](https://img.shields.io/badge/wiki-Documentation-blue.svg)](https://github.com/codingtuto/LiteJsonDb/wiki)

---
> [!NOTE]
> Nous venons d'ajouter de nouvelles fonctionnalités géniales à `LiteJsonDb` pour rendre votre codage encore plus fluide. Pour un aperçu rapide et des exemples, consultez notre [wiki](https://github.com/codingtuto/LiteJsonDb/wiki/LiteJsonDb-Utility-Functions) pour tous les détails.
---

## :eyes: Aperçu

Salut ! Bienvenue sur **LiteJsonDb**, votre base de données conviviale et légère basée sur JSON. Elle est simple et dotée de fonctionnalités telles que le chiffrement, les sauvegardes et une gestion solide des erreurs, le tout sans les aspects contraignants.

## :thinking: Pourquoi LiteJsonDb ?

Avouons-le : parfois, vous n'avez pas besoin d'une configuration de base de données complexe. Peut-être que vous construisez un petit projet, un prototype rapide, ou que vous voulez simplement une façon simple de stocker et de récupérer des données JSON. LiteJsonDb est là pour ces moments-là. C'est simple, efficace, et ça fait le travail sans chichis.

## :hammer_and_wrench: Fonctionnalités

-   **Gestion facile des données** : Ajoutez, modifiez, récupérez et supprimez des données avec seulement quelques lignes de code.
-   **Chiffrement des données** : Gardez vos données en sécurité grâce au chiffrement optionnel.
-   **Sauvegarde et restauration** : Sauvegardes automatiques pour garder vos données en sécurité.
-   **Sous-collections** : Organisez vos données dans des structures imbriquées et ordonnées.
-   **Gestion conviviale des erreurs** : Messages d'erreur colorés et utiles pour vous guider.

> [!NOTE]
> LiteJsonDb rend la gestion des données JSON simple et agréable. Que vous construisiez une petite application ou que vous ayez simplement besoin d'une solution de stockage de données légère, LiteJsonDb est là pour vous. Profitez-en !

## :man_technologist: Installation

Commencer est super facile. Il suffit d'installer le package via pip et vous êtes prêt à partir :

<pre>
pip install litejsondb
</pre>

Une nouvelle version est disponible, tapez `pip install --upgrade litejsondb` pour mettre à jour

# :crystal_ball: Utilisation

## :white_check_mark: Configuration initiale

Tout d'abord, importez la classe `JsonDB` et initialisez votre base de données :

<pre><code>
import LiteJsonDb

# Initialiser la base de données avec le chiffrement activé
db = LiteJsonDb.JsonDB()  # Certains paramètres peuvent être passés ici
</code></pre>

---

<details>
<summary>Cliquez pour voir le code et l'aperçu des paramètres</summary>

## :gear: Aperçu des paramètres

### Journalisation
Activez la journalisation pour suivre toutes les opérations de la base de données. Ceci est utile pour le débogage ou la surveillance des activités :

<pre><code>
db = LiteJsonDb.JsonDB(enable_log=True)
</code></pre>

### Sauvegardes automatiques
Évitez de perdre vos données en activant les sauvegardes automatiques. Un fichier de sauvegarde est créé chaque fois que vous enregistrez des modifications :

<pre><code>
db = LiteJsonDb.JsonDB(auto_backup=True)
</code></pre>

### Chiffrement BASE64
Par défaut, si vous passez `crypted` à `True`, il utilisera le système de chiffrement minimal (Base64)
<pre><code>
db = LiteJsonDb.JsonDB(crypted=True)
</code></pre>

### Chiffrement Fernet
Sécurisez vos données avec le chiffrement Fernet
<pre><code>
db = LiteJsonDb.JsonDB(crypted=True, encryption_method="fernet", encryption_key="votre-clé-secrète")
</code></pre>
Si aucune clé n'est fournie, le système générera une erreur pour garantir la sécurité de vos données.
</details>

## :memo: Exemple récapitulatif

Combinez la journalisation, les sauvegardes automatiques et le chiffrement en un seul flux de travail :

<details>
<summary>Cliquez pour voir le code</summary>

<pre><code>
import LiteJsonDb

# Initialiser la base de données avec la journalisation, la sauvegarde automatique et le chiffrement
db = LiteJsonDb.JsonDB(
    enable_log=True, 
    auto_backup=True, 
    crypted=True, 
    encryption_method="fernet",
    encryption_key="ma-clé-sécurisée"
)
</code></pre>

</details>

---

### 🤗 Opérations de base

#### :heavy_plus_sign: Définition des données

L'ajout de données est un jeu d'enfant. Utilisez simplement la méthode `set_data`. Si la clé existe déjà, vous recevrez un rappel amical pour utiliser `edit_data` à la place.

<pre>
# Définir les données sans données supplémentaires
db.set_data("posts")

# Définir les données avec des données supplémentaires
db.set_data("users/1", {"name": "Aliou", "age": 20})
db.set_data("users/2", {"name": "Coder", "age": 25})
</pre>

#### :writing_hand: Modification des données

Besoin de mettre à jour des données ? Pas de problème. Utilisez la méthode `edit_data`. Elle fusionne les nouvelles données avec les données existantes, pour que rien ne soit perdu.

<pre>
# Modifier les données
db.edit_data("users/1", {"name": "Alex"})
</pre>

#### :ballot_box_with_check: Obtention des données

La récupération des données est on ne peut plus simple. Utilisez la méthode `get_data`.

<pre>
# Obtenir les données
print(db.get_data("users/1"))  # Sortie: {'name': 'Alex', 'age': 20}
print(db.get_data("users/2"))  # Sortie: {'name': 'Coder', 'age': 25}
</pre>

> [!TIP]
> Vous pouvez accéder directement à des données spécifiques en utilisant des chemins dans la méthode `get_data`. Par exemple, pour obtenir uniquement le nom de l'utilisateur, vous pouvez faire :
<pre>
print(db.get_data("users/1/name"))
</pre>

Ici, vous obtenez le nom de l'utilisateur sans récupérer les autres parties des données.

#### :wastebasket: Suppression des données

Besoin de supprimer quelque chose ? La méthode `remove_data` est là pour vous.

<pre>
# Supprimer les données
db.remove_data("users/2")
</pre>

#### :package: Récupération complète de la base de données

Vous voulez tout voir ? Utilisez la méthode `get_db`. Définissez `raw=True` si vous voulez les données dans un format lisible.

<pre>
# Obtenir la base de données complète
print(db.get_db(raw=True))
</pre>

## 🔍 Recherche de données (nouveau)

Cette nouvelle fonctionnalité a été intégrée en réponse à la [question](https://github.com/codingtuto/LiteJsonDb/issues/2) soulevée concernant l'amélioration des capacités de recherche de données. Cette fonction vous permet de rechercher des valeurs dans votre base de données, soit dans l'ensemble de la base de données, soit dans une clé spécifique. Cette amélioration rend la recherche de vos données beaucoup plus facile et efficace.

### Comment utiliser

La fonction `search_data` offre deux modes de recherche principaux :

1.  **Recherche de base** : Recherche une valeur n'importe où dans la base de données.
2.  **Recherche spécifique à une clé** : Recherche une valeur dans une clé spécifique.

### Intégration

1.  **Utiliser la fonction `search_data`**

    Voici comment vous pouvez utiliser la fonction `search_data` :

    -   **Recherche de base** : Pour rechercher une valeur dans l'ensemble de la base de données, utilisez le code suivant :

        ```python
        results = db.search_data("Aliou")
        print(results)
        ```

        Ceci recherchera la valeur `"Aliou"` dans toutes les clés de votre base de données.

    -   **Recherche spécifique à une clé** : Pour rechercher une valeur dans une clé spécifique, utilisez le code suivant :

        ```python
        results = db.search_data("Aliou", key="users")
        print(results)
        ```

        Ceci recherchera la valeur `"Aliou"` spécifiquement dans la clé `"users"`.

## 📦 Sauvegarde vers Telegram (nouveau)

Cette fonctionnalité a été intégrée pour vous aider à sauvegarder facilement vos fichiers, tels que votre base de données, directement dans une conversation Telegram. En utilisant cette méthode, vous pouvez sauvegarder en toute sécurité les fichiers importants automatiquement dans une conversation Telegram.

### Comment utiliser

La fonction `backup_to_telegram` vous permet de sauvegarder n'importe quel fichier sur Telegram via un bot. Vous aurez besoin de deux informations essentielles : le **token du bot** et l'**identifiant de la conversation** où le fichier sera envoyé.

### Intégration

1.  **Obtenir votre token de bot Telegram**
    Pour utiliser cette fonctionnalité, vous devez d'abord créer un bot sur Telegram en utilisant [@BotFather](https://t.me/BotFather). Une fois que votre bot est créé, BotFather vous fournira un token que vous utiliserez pour l'authentification.

2.  **Trouver votre identifiant de conversation**
    Vous pouvez obtenir votre identifiant de conversation en utilisant [@MissRose_bot](https://t.me/MissRose_bot) et en tapant `/id`. Il vous donnera votre identifiant de conversation unique.

3.  **Utiliser la fonction `backup_to_telegram`**
    Voici comment utiliser la fonction `backup_to_telegram` :

    <pre><code>python
    db.backup_to_telegram("votre_token", "votre_identifiant_de_conversation")
    </code></pre>

    Ceci enverra le fichier de sauvegarde à l'identifiant de conversation spécifié en utilisant votre bot Telegram.

## 📦 Exportation vers CSV (nouveau)

Cette fonctionnalité a été intégrée pour vous permettre d'exporter facilement vos données au format CSV. Cela facilite le partage et l'analyse de vos données en dehors de l'application en créant des fichiers CSV qui peuvent être ouverts avec des tableurs comme Excel ou Google Sheets.

### Comment utiliser

La méthode `export_to_csv` vous permet d'exporter soit une collection spécifique, soit l'ensemble de la base de données. Voici comment l'utiliser :

### Intégration

1.  **Préparer vos données**
    Assurez-vous que les données que vous souhaitez exporter sont bien structurées. Vous pouvez avoir vos données sous forme de dictionnaires ou de listes de dictionnaires. Par exemple :

    <pre><code>
    # Ajouter des données d'exemple
    db.set_data("users", {
        "1": {"name": "Aliou", "age": 20},
        "2": {"name": "Coder", "age": 25}
    })
    </code></pre>

2.  **Utiliser la méthode `export_to_csv`**
    Voici comment appeler la méthode pour exporter les données :

    #### Exporter une collection spécifique

    Pour exporter une collection spécifique, vous devez fournir la clé correspondante :

    <pre><code>
    # Exporter une collection spécifique
    db.export_to_csv("users")
    </code></pre>

    #### Exporter l'ensemble de la base de données

    Si vous souhaitez exporter toutes les données de la base de données, vous pouvez appeler la méthode sans paramètres :

    <pre><code>
    # Exporter l'ensemble de la base de données
    db.export_to_csv()
    </code></pre>

## 🐛 Gestion des erreurs

Cette fonctionnalité est expérimentale et peut ne pas prendre en charge tous les formats de données. Si vous essayez d'exporter une collection qui n'existe pas, un message d'erreur s'affichera :

Si vous recevez des erreurs comme celle-ci : `Oups ! Une erreur s'est produite lors de l'exportation CSV : ...`, nous vous recommandons d'ouvrir une issue dans notre dépôt afin que nous puissions y remédier. Vos commentaires sont précieux, et nous apprécions votre patience alors que nous continuons à améliorer cette fonctionnalité !

### :file_folder: Travailler avec les sous-collections

## :file_folder: Sous-collections

Dans LiteJsonDb, les sous-collections sont un moyen d'organiser vos données de manière hiérarchique. Considérez-les comme des structures imbriquées qui vous permettent de regrouper les données associées sous une clé parent. Cette fonctionnalité est particulièrement utile lorsque vous souhaitez gérer des relations de données complexes sans perdre la simplicité du JSON.

### :thinking: Que sont les sous-collections ?

Les sous-collections sont essentiellement des collections au sein de collections. Par exemple, si vous avez une collection principale d'utilisateurs, vous pouvez organiser leurs publications dans des sous-collections distinctes. Voici comment vous pouvez travailler avec elles :

-   **Définition des données de sous-collection** : Créez et remplissez une sous-collection sous une clé parent spécifiée.
-   **Modification des données de sous-collection** : Mettez à jour les éléments existants dans une sous-collection.
-   **Obtention des données de sous-collection** : Récupérez les données stockées dans une sous-collection.
-   **Suppression des données de sous-collection** : Supprimez les éléments ou des sous-collections entières.

L'utilisation de sous-collections vous aide à maintenir une structure claire dans vos données, ce qui facilite leur gestion et leur interrogation.

#### :heavy_plus_sign: Définition des données de sous-collection

Organisez vos données avec des sous-collections. Facile comme bonjour.

<pre>
# Définir les données de sous-collection
db.set_subcollection("groups", "1", {"name": "Admins"})
</pre>

#### :writing_hand: Modification des données de sous-collection

Modifier des éléments dans une sous-collection ? Pas de problème.

<pre>
# Modifier les données de sous-collection
db.edit_subcollection("groups", "1", {"description": "Groupe d'administrateurs"})
</pre>

#### :ballot_box_with_check: Obtention des données de sous-collection

Besoin de récupérer des sous-collections ou des éléments spécifiques ? On s'en occupe.

<pre>
# Obtenir les données de sous-collection
print(db.get_subcollection("groups"))

# Obtenir un élément personnalisé des données de sous-collection
print(db.get_subcollection("groups", "1"))
</pre>

#### :wastebasket: Suppression des données de sous-collection

La suppression d'éléments de sous-collections est tout aussi simple.

<pre>
# Supprimer les données de sous-collection
db.remove_subcollection("groups", "1")
</pre>

## :bug: Gestion des erreurs

LiteJsonDb est là pour vous aider. Voici quelques messages d'erreur colorés et conviviaux pour vous guider :

-   **La clé existe** : Si vous essayez de définir des données avec une clé existante, il vous suggérera d'utiliser `edit_data`.
-   **La clé n'a pas été trouvée** : Si une clé n'existe pas lorsque vous essayez d'obtenir ou de supprimer des données, il vous avertira avec un conseil sur la façon de procéder.
-   **Problèmes de fichiers** : S'il y a des problèmes de permissions de fichiers, il vous guidera sur la façon de les résoudre.

## :open_file_folder: Exemple de structure de projet

Voici à quoi pourrait ressembler votre projet si vous initialisez `LiteJssonDb` :

<pre>
projet/
│
├── base_de_données/
│   ├── db.json
│   ├── db_backup.json
│   └── LiteJsonDb.log
└── votre_code.py
</pre>

## :shipit: Exemple `main.py`

Mettons tout cela ensemble avec un exemple de fichier `main.py` :

<pre>
import LiteJsonDb
  
# Initialiser la base de données avec le chiffrement activé
db =  LiteJsonDb.JsonDB()

# Ajouter des données initiales
# Définir les données sans données supplémentaires
db.set_data("posts")

# Définir les données avec des données supplémentaires
db.set_data("users/1", {"name": "Aliou", "age": 20})
db.set_data("users/2", {"name": "Coder", "age": 25})

# Modifier les données existantes
db.edit_data("users/1", {"name": "Alex"})

# Récupérer et afficher les données
print(db.get_data("users/1"))
print(db.get_data("users/2"))

# Supprimer les données
db.remove_data("users/2")

# Effectuer une recherche de base
results = db.search_data("Aliou")
print("Résultats de la recherche de base:", results)

# Effectuer une recherche spécifique à une clé
results = db.search_data("Aliou", key="users")
print("Résultats de la recherche spécifique à une clé:", results)

# Récupérer la base de données complète
print(db.get_db(raw=True))

# Travailler avec des sous-collections
db.set_subcollection("groups", "1", {"name": "Admins"})
db.edit_subcollection("groups", "1", {"description": "Groupe d'administrateurs"})
print(db.get_subcollection("groups"))
db.remove_subcollection("groups", "1")

# SI VOUS VOULEZ SAUVEGARDER LA BASE DE DONNÉES SUR TELEGRAM
# db.backup_to_telegram("votre_token", "votre_identifiant_de_conversation")

""" SI VOUS VOULEZ EXPORTER VOS DONNÉES AU FORMAT CSV
# Exporter une collection spécifique
db.export_to_csv("users")

# Exporter l'ensemble de la base de données
db.export_to_csv()
"""
</pre>

## :memo: Comprendre `set_data` vs. Sous-collections

<details>
<summary>Cliquez pour développer</summary>

### `set_data`

La méthode `set_data` est utilisée pour ajouter ou mettre à jour des données à un chemin spécifique. Si la clé existe déjà, vous devrez utiliser `edit_data` pour la modifier. Cette méthode est idéale pour les paires clé-valeur simples ou les structures de données directes.

<pre>
# Définir les données
db.set_data("users/1", {"name": "Aliou", "age": 20})
</pre>

### Sous-collections

Les sous-collections, d'autre part, sont utilisées pour créer et gérer des structures imbriquées dans votre base de données. Elles vous permettent de regrouper les données associées sous une clé parent, offrant ainsi une manière plus organisée de gérer les relations complexes. Les sous-collections sont essentiellement des collections au sein de collections.

<pre>
# Définir les données de sous-collection
db.set_subcollection("groups", "1", {"name": "Admins"})
</pre>

### Principales différences

-   **Structure** : `set_data` est utilisé pour les structures de données plates, tandis que les sous-collections permettent une organisation hiérarchique.
-   **Utilisation** : Utilisez `set_data` pour les paires clé-valeur simples et `set_subcollection` lorsque vous avez besoin de collections imbriquées.
-   **Organisation** : Les sous-collections aident à maintenir une structure claire et à regrouper les données associées, ce qui facilite la gestion et l'interrogation des relations complexes.

En comprenant ces différences, vous pouvez choisir la méthode appropriée pour vos besoins de gestion de données, en assurant une base de données bien organisée et efficace.

</details>

## 🧾 TODO : Prochaines étapes pour LiteJsonDb

Nous nous efforçons toujours d'améliorer LiteJsonDb. Voici ce que nous avons en vue :

-   [x] Ajouter la prise en charge du chiffrement des données pour sécuriser le contenu JSON.
-   [x] Mettre en œuvre des sauvegardes automatiques pour assurer la sécurité des données.
-   [x] Améliorer la gestion des erreurs avec des messages conviviaux et colorés.
-   [x] Ajout de la documentation en français
-   [x] Mettre en œuvre des sauvegardes automatisées pour envoyer les données à un bot Telegram.
-   [ ] Corriger tous les bugs découverts pour assurer un fonctionnement sans heurts.
-   [ ] Atteindre 100 étoiles sur GitHub et célébrer cela en ajoutant d'autres fonctionnalités impressionnantes !

## :hugs: Contributions et communauté

Nous accueillons les contributions, les suggestions et les commentaires pour rendre LiteJsonDb encore meilleur ! Si vous avez des idées d'améliorations ou si vous voulez corriger un bug, n'hésitez pas à :

-   **Soumettre une demande d'extraction (PR)** : Contribuez de nouvelles fonctionnalités ou des corrections de bugs en créant une demande d'extraction. Vos modifications aideront à améliorer LiteJsonDb pour tout le monde !
-   **Signaler les problèmes** : Si vous rencontrez des bugs ou des problèmes, veuillez ouvrir un problème dans le dépôt. Fournissez autant de détails que possible afin que nous puissions y remédier rapidement.
-   **Suggérer des fonctionnalités** : Vous avez une idée pour une nouvelle fonctionnalité ? Faites-le nous savoir ! Nous sommes toujours ouverts aux suggestions sur la façon d'améliorer LiteJsonDb.

> Vos commentaires et contributions sont grandement appréciés et nous aident à maintenir la croissance et l'amélioration de LiteJsonDb.

## :heart: Dons et soutien : Comment vous pouvez aider

LiteJsonDb est une œuvre d'amour, et votre soutien peut faire une grande différence ! Si vous appréciez le projet et que vous voulez montrer votre gratitude, voici quelques façons dont vous pouvez aider :

### Forkez et mettez une étoile au dépôt

L'une des meilleures façons de soutenir LiteJsonDb est de forker le dépôt et de lui donner une étoile sur GitHub. C'est comme un high-five virtuel et cela nous aide à faire connaître le projet. De plus, cela nous montre que vous appréciez le travail que nous faisons !

### Envisagez un don

Si vous vous sentez particulièrement généreux et que vous souhaitez contribuer financièrement, nous vous en serions incroyablement reconnaissants. Les dons nous aident à couvrir les coûts et à assurer le bon fonctionnement du projet. Vous pouvez nous soutenir des manières suivantes :

-   **PayPal** : Envoyez un don directement à [mon compte PayPal](https://paypal.me/djibson35). Chaque petite contribution aide et est grandement appréciée !
-   **Bitcoin** : Vous préférez les cryptomonnaies ? Vous pouvez également faire un don en utilisant Bitcoin à l'adresse suivante : `1Nn15EttfT2dVBisj8bXCnBiXjcqk1ehWR`.

> Votre soutien, que ce soit par une étoile, un fork ou un don, contribue à maintenir LiteJsonDb vivant et florissant. Merci d'être génial !

Bon code et bonne continuation ! :rocket:
