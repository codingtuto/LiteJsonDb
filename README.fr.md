# LiteJsonDb

![LiteJsonDb](https://telegra.ph/file/374450a4f36c217b3a20b.jpg)

![Téléchargements PyPI](https://img.shields.io/pypi/dm/LiteJsonDb.svg)
![Version PyPI](https://img.shields.io/pypi/v/LiteJsonDb.svg)
![GitHub Stars](https://img.shields.io/github/stars/codingtuto/LiteJsonDb)
![GitHub Forks](https://img.shields.io/github/forks/codingtuto/LiteJsonDb)

[Documentation française](./README.fr.md) · [Wiki](https://github.com/codingtuto/LiteJsonDb/wiki)

LiteJsonDb est une base de données locale légère basée sur JSON pour les projets Python qui n'ont pas besoin d'un serveur de base de données.

Elle fournit une API simple pour stocker, modifier, récupérer et supprimer des données, tout en proposant des fonctionnalités complémentaires comme :

* le chiffrement des données ;
* les sauvegardes automatiques ;
* les sous-collections ;
* la recherche de données ;
* l'export CSV ;
* la sauvegarde vers Telegram ;
* la journalisation des opérations ;
* une gestion explicite des erreurs.

L'objectif est de conserver une API simple tout en offrant suffisamment de fonctionnalités pour les scripts, prototypes, outils internes et petites applications.

---

## Sommaire

* [Installation](#installation)
* [Démarrage rapide](#démarrage-rapide)
* [Configuration](#configuration)

  * [Journalisation](#journalisation)
  * [Sauvegardes automatiques](#sauvegardes-automatiques)
  * [Chiffrement](#chiffrement)
  * [Chiffrement Fernet](#chiffrement-fernet)
* [Opérations de base](#opérations-de-base)

  * [`set_data`](#set_data)
  * [`edit_data`](#edit_data)
  * [`get_data`](#get_data)
  * [`remove_data`](#remove_data)
  * [`get_db`](#get_db)
* [Recherche](#recherche)

  * [`search_data`](#search_data)
* [Sous-collections](#sous-collections)

  * [`set_subcollection`](#set_subcollection)
  * [`edit_subcollection`](#edit_subcollection)
  * [`get_subcollection`](#get_subcollection)
  * [`remove_subcollection`](#remove_subcollection)
* [Sauvegarde Telegram](#sauvegarde-telegram)
* [Export CSV](#export-csv)
* [Gestion des erreurs](#gestion-des-erreurs)
* [Structure de projet](#structure-de-projet)
* [Exemple complet](#exemple-complet)
* [`set_data` vs sous-collections](#set_data-vs-sous-collections)
* [Roadmap](#roadmap)
* [Contribuer](#contribuer)
* [Soutenir le projet](#soutenir-le-projet)

---

## Installation

Installez LiteJsonDb depuis PyPI :

```bash
pip install litejsondb
```

Pour mettre à jour une installation existante :

```bash
pip install --upgrade litejsondb
```

Vérifiez ensuite que le package peut être importé :

```python
import LiteJsonDb
```

---

## Démarrage rapide

La création d'une base de données ne nécessite qu'une initialisation de `JsonDB`.

```python
import LiteJsonDb

db = LiteJsonDb.JsonDB()
```

Vous pouvez ensuite créer une collection :

```python
db.set_data("posts")
```

Ou créer directement une entrée :

```python
db.set_data(
    "users/1",
    {
        "name": "Aliou",
        "age": 20
    }
)
```

Récupérez ensuite les données avec :

```python
user = db.get_data("users/1")

print(user)
```

Résultat :

```python
{
    "name": "Aliou",
    "age": 20
}
```

---

# Configuration

`JsonDB` accepte plusieurs paramètres permettant d'adapter le comportement de la base de données.

Exemple :

```python
db = LiteJsonDb.JsonDB(
    enable_log=True,
    auto_backup=True,
    crypted=True,
    encryption_method="fernet",
    encryption_key="ma-clé-sécurisée"
)
```

Les options sont indépendantes. Vous pouvez activer uniquement celles dont votre application a besoin.

---

## Journalisation

La journalisation permet d'enregistrer les opérations effectuées par LiteJsonDb.

Activez-la avec `enable_log=True` :

```python
db = LiteJsonDb.JsonDB(enable_log=True)
```

Cette option peut être utile lorsque vous souhaitez :

* suivre les opérations effectuées sur la base ;
* diagnostiquer un problème ;
* surveiller le comportement d'une application ;
* conserver un historique technique des opérations.

Si la journalisation n'est pas nécessaire, laissez l'option désactivée :

```python
db = LiteJsonDb.JsonDB(enable_log=False)
```

---

## Sauvegardes automatiques

L'option `auto_backup` permet de créer automatiquement une sauvegarde lorsqu'une modification est enregistrée.

Activation :

```python
db = LiteJsonDb.JsonDB(auto_backup=True)
```

Désactivation :

```python
db = LiteJsonDb.JsonDB(auto_backup=False)
```

Cette option est particulièrement utile pour les applications dans lesquelles la perte du fichier JSON principal serait problématique.

---

## Chiffrement

LiteJsonDb permet d'activer le chiffrement avec l'option `crypted`.

```python
db = LiteJsonDb.JsonDB(crypted=True)
```

Lorsque `crypted=True`, LiteJsonDb utilise par défaut son mécanisme de chiffrement minimal basé sur Base64.

```python
db = LiteJsonDb.JsonDB(
    crypted=True
)
```

### À propos de Base64

Base64 ne doit pas être considéré comme un mécanisme de chiffrement sécurisé destiné à protéger des données sensibles.

Il s'agit principalement d'un encodage.

Si votre application nécessite une protection cryptographique réelle, utilisez le mode Fernet décrit ci-dessous.

---

## Chiffrement Fernet

LiteJsonDb prend également en charge le chiffrement Fernet.

Exemple :

```python
db = LiteJsonDb.JsonDB(
    crypted=True,
    encryption_method="fernet",
    encryption_key="votre-clé-secrète"
)
```

Les paramètres utilisés sont :

| Paramètre           | Valeur     | Description                       |
| ------------------- | ---------- | --------------------------------- |
| `crypted`           | `True`     | Active le chiffrement             |
| `encryption_method` | `"fernet"` | Sélectionne le chiffrement Fernet |
| `encryption_key`    | chaîne     | Clé utilisée pour le chiffrement  |

Une clé doit être fournie lorsque Fernet est utilisé.

```python
db = LiteJsonDb.JsonDB(
    crypted=True,
    encryption_method="fernet"
)
```

Cette configuration provoquera une erreur si aucune clé n'est disponible.

### Configuration complète

Vous pouvez combiner les différentes options :

```python
import LiteJsonDb

db = LiteJsonDb.JsonDB(
    enable_log=True,
    auto_backup=True,
    crypted=True,
    encryption_method="fernet",
    encryption_key="ma-clé-sécurisée"
)
```

---

# Opérations de base

LiteJsonDb fournit quatre opérations principales pour manipuler les données :

* `set_data` : créer des données ;
* `edit_data` : modifier des données existantes ;
* `get_data` : récupérer des données ;
* `remove_data` : supprimer des données.

Une cinquième méthode, `get_db`, permet de récupérer la base entière.

---

## `set_data`

`set_data` permet de créer une entrée à un chemin donné.

### Créer une collection vide

```python
db.set_data("posts")
```

### Créer une entrée avec des données

```python
db.set_data(
    "users/1",
    {
        "name": "Aliou",
        "age": 20
    }
)
```

Vous pouvez créer plusieurs entrées :

```python
db.set_data(
    "users/1",
    {
        "name": "Aliou",
        "age": 20
    }
)

db.set_data(
    "users/2",
    {
        "name": "Coder",
        "age": 25
    }
)
```

### Important

`set_data` est destiné à la création de données.

Si la clé existe déjà, LiteJsonDb vous indiquera d'utiliser `edit_data` pour effectuer une modification.

---

## `edit_data`

`edit_data` permet de modifier une entrée existante.

Les nouvelles valeurs sont fusionnées avec les données déjà présentes.

```python
db.edit_data(
    "users/1",
    {
        "name": "Alex"
    }
)
```

Si la donnée initiale est :

```python
{
    "name": "Aliou",
    "age": 20
}
```

Après la modification :

```python
{
    "name": "Alex",
    "age": 20
}
```

La valeur `age` est conservée parce qu'elle n'a pas été remplacée.

---

## `get_data`

`get_data` permet de récupérer les données associées à un chemin.

```python
print(db.get_data("users/1"))
```

Exemple de résultat :

```python
{
    "name": "Alex",
    "age": 20
}
```

Pour récupérer une autre entrée :

```python
print(db.get_data("users/2"))
```

### Accéder directement à une valeur

Les chemins peuvent être utilisés pour cibler une valeur précise.

```python
print(db.get_data("users/1/name"))
```

Au lieu de récupérer :

```python
{
    "name": "Alex",
    "age": 20
}
```

la méthode cible directement :

```text
Alex
```

Cette notation est utile lorsque vous n'avez pas besoin de charger l'ensemble de l'objet.

---

## `remove_data`

`remove_data` permet de supprimer une entrée.

```python
db.remove_data("users/2")
```

La donnée située à `users/2` est alors supprimée.

---

## `get_db`

`get_db` permet de récupérer l'ensemble de la base de données.

```python
db.get_db()
```

Pour demander les données dans un format brut et lisible :

```python
print(
    db.get_db(raw=True)
)
```

L'option `raw=True` est particulièrement utile pour inspecter le contenu de la base pendant le développement.

---

# Recherche

LiteJsonDb fournit `search_data` pour rechercher une valeur dans les données existantes.

La méthode peut être utilisée de deux façons :

1. rechercher dans l'ensemble de la base ;
2. limiter la recherche à une clé spécifique.

---

## Recherche globale

Pour rechercher une valeur dans toute la base :

```python
results = db.search_data("Aliou")

print(results)
```

Cette recherche parcourt les données disponibles afin de trouver la valeur recherchée.

---

## Recherche dans une clé spécifique

Vous pouvez limiter la recherche à une clé avec le paramètre `key`.

```python
results = db.search_data(
    "Aliou",
    key="users"
)

print(results)
```

Dans cet exemple, la recherche est limitée à `users`.

Cette approche est préférable lorsque votre base contient plusieurs collections et que vous connaissez déjà la zone dans laquelle rechercher.

---

# Sauvegarde Telegram

LiteJsonDb permet d'envoyer un fichier de sauvegarde vers une conversation Telegram à l'aide d'un bot.

La méthode concernée est :

```python
backup_to_telegram()
```

Elle nécessite deux informations :

* le token du bot Telegram ;
* l'identifiant de la conversation destinataire.

---

## 1. Créer le bot Telegram

Créez votre bot avec [@BotFather](https://t.me/BotFather).

Après la création du bot, Telegram fournit un token.

Le token doit être conservé de manière sécurisée et ne doit pas être publié dans un dépôt Git public.

---

## 2. Récupérer l'identifiant de conversation

L'identifiant de conversation peut être obtenu avec [@MissRose_bot](https://t.me/MissRose_bot).

Utilisez :

```text
/id
```

Le bot vous retournera l'identifiant de la conversation.

---

## 3. Envoyer la sauvegarde

Utilisez ensuite :

```python
db.backup_to_telegram(
    "votre_token",
    "votre_identifiant_de_conversation"
)
```

Le fichier de sauvegarde est envoyé à la conversation correspondant à l'identifiant fourni.

### Exemple

```python
import LiteJsonDb

db = LiteJsonDb.JsonDB(
    auto_backup=True
)

db.backup_to_telegram(
    "123456:ABCDEF...",
    "-100123456789"
)
```

### Sécurité

Ne stockez pas le token directement dans votre code si le projet est versionné.

Évitez notamment :

```python
db.backup_to_telegram(
    "TOKEN_REEL",
    "CHAT_ID"
)
```

dans un dépôt public.

Préférez des variables d'environnement ou un système de configuration adapté à votre environnement d'exécution.

---

# Export CSV

LiteJsonDb permet d'exporter les données au format CSV avec :

```python
export_to_csv()
```

L'export peut être effectué sur une collection spécifique ou sur l'ensemble de la base.

---

## Préparer les données

Exemple de structure :

```python
db.set_data(
    "users",
    {
        "1": {
            "name": "Aliou",
            "age": 20
        },
        "2": {
            "name": "Coder",
            "age": 25
        }
    }
)
```

---

## Exporter une collection

Pour exporter uniquement `users` :

```python
db.export_to_csv("users")
```

Le paramètre correspond au nom de la collection à exporter.

---

## Exporter toute la base

Pour exporter l'ensemble de la base :

```python
db.export_to_csv()
```

Aucun nom de collection n'est nécessaire.

---

## Limites actuelles

La fonctionnalité d'export CSV est expérimentale et peut ne pas prendre en charge tous les formats de données.

Si vous essayez d'exporter une collection inexistante ou une structure non prise en charge, une erreur peut être retournée.

Exemple :

```text
Oups ! Une erreur s'est produite lors de l'exportation CSV : ...
```

En cas de problème reproductible, ouvrez une issue dans le dépôt avec :

* la version de LiteJsonDb ;
* votre version de Python ;
* la structure des données concernées ;
* le code permettant de reproduire le problème ;
* le message d'erreur complet.

---

# Sous-collections

Les sous-collections permettent de représenter des données hiérarchiques.

Elles sont utiles lorsque plusieurs données appartiennent à une même collection parent.

Par exemple :

```text
groups
├── 1
│   ├── name
│   └── description
└── 2
    ├── name
    └── description
```

Les principales opérations disponibles sont :

* `set_subcollection` ;
* `edit_subcollection` ;
* `get_subcollection` ;
* `remove_subcollection`.

---

## `set_subcollection`

Crée une entrée dans une sous-collection.

```python
db.set_subcollection(
    "groups",
    "1",
    {
        "name": "Admins"
    }
)
```

Les paramètres correspondent à :

| Paramètre            | Description             |
| -------------------- | ----------------------- |
| `"groups"`           | collection parent       |
| `"1"`                | identifiant de l'entrée |
| `{"name": "Admins"}` | données à enregistrer   |

---

## `edit_subcollection`

Modifie une entrée existante dans une sous-collection.

```python
db.edit_subcollection(
    "groups",
    "1",
    {
        "description": "Groupe d'administrateurs"
    }
)
```

Cette opération permet d'ajouter ou de modifier des champs dans l'entrée ciblée.

---

## `get_subcollection`

Pour récupérer une sous-collection complète :

```python
print(
    db.get_subcollection("groups")
)
```

Pour récupérer une entrée spécifique :

```python
print(
    db.get_subcollection(
        "groups",
        "1"
    )
)
```

La première forme récupère la collection.

La seconde cible une entrée précise.

---

## `remove_subcollection`

Pour supprimer une entrée d'une sous-collection :

```python
db.remove_subcollection(
    "groups",
    "1"
)
```

---

# Gestion des erreurs

LiteJsonDb fournit des messages permettant d'identifier plusieurs erreurs courantes.

## Clé déjà existante

Si vous utilisez `set_data` sur une clé qui existe déjà, LiteJsonDb vous indique d'utiliser `edit_data`.

Exemple :

```python
db.set_data(
    "users/1",
    {
        "name": "Alex"
    }
)
```

Si `users/1` existe déjà, utilisez :

```python
db.edit_data(
    "users/1",
    {
        "name": "Alex"
    }
)
```

---

## Clé inexistante

Si vous essayez de récupérer ou de supprimer une clé qui n'existe pas, LiteJsonDb signale que la clé n'a pas été trouvée.

Exemple :

```python
db.get_data("users/999")
```

ou :

```python
db.remove_data("users/999")
```

Vérifiez le chemin utilisé avant d'effectuer l'opération.

---

## Problèmes de fichiers

LiteJsonDb dépend du système de fichiers local pour stocker ses données.

Des problèmes de permissions peuvent donc empêcher :

* la création de fichiers ;
* la modification de fichiers ;
* la création de sauvegardes ;
* l'écriture des journaux.

Dans ce cas, vérifiez les permissions du répertoire utilisé par votre application.

---

# Structure de projet

Une structure possible pour une application utilisant LiteJsonDb :

```text
projet/
├── base_de_données/
│   ├── db.json
│   ├── db_backup.json
│   └── LiteJsonDb.log
└── votre_code.py
```

Les noms et emplacements exacts peuvent dépendre de la configuration et de la manière dont LiteJsonDb est initialisé.

---

# Exemple complet

Voici un exemple regroupant les principales fonctionnalités de LiteJsonDb dans un même fichier.

```python
import LiteJsonDb


# Initialisation de la base de données
db = LiteJsonDb.JsonDB()


# Création d'une collection
db.set_data("posts")


# Création d'utilisateurs
db.set_data(
    "users/1",
    {
        "name": "Aliou",
        "age": 20
    }
)

db.set_data(
    "users/2",
    {
        "name": "Coder",
        "age": 25
    }
)


# Modification d'un utilisateur
db.edit_data(
    "users/1",
    {
        "name": "Alex"
    }
)


# Récupération des utilisateurs
print(
    db.get_data("users/1")
)

print(
    db.get_data("users/2")
)


# Suppression d'un utilisateur
db.remove_data("users/2")


# Recherche globale
results = db.search_data("Aliou")

print(
    "Résultats de la recherche globale:",
    results
)


# Recherche limitée à une collection
results = db.search_data(
    "Aliou",
    key="users"
)

print(
    "Résultats de la recherche dans users:",
    results
)


# Récupération de la base complète
print(
    db.get_db(raw=True)
)


# Création d'une sous-collection
db.set_subcollection(
    "groups",
    "1",
    {
        "name": "Admins"
    }
)


# Modification de la sous-collection
db.edit_subcollection(
    "groups",
    "1",
    {
        "description": "Groupe d'administrateurs"
    }
)


# Récupération de la sous-collection
print(
    db.get_subcollection("groups")
)


# Suppression d'une entrée de sous-collection
db.remove_subcollection(
    "groups",
    "1"
)
```

---

# Sauvegarde Telegram dans l'exemple

Si vous souhaitez envoyer une sauvegarde vers Telegram :

```python
db.backup_to_telegram(
    "votre_token",
    "votre_identifiant_de_conversation"
)
```

Cette opération peut être appelée après les modifications importantes de la base.

---

# Export CSV dans l'exemple

Pour exporter une collection :

```python
db.export_to_csv("users")
```

Pour exporter l'ensemble de la base :

```python
db.export_to_csv()
```

---

# `set_data` vs sous-collections

Les deux systèmes permettent de structurer des données, mais ils répondent à des besoins différents.

## `set_data`

`set_data` convient aux données directement accessibles via un chemin.

Exemple :

```python
db.set_data(
    "users/1",
    {
        "name": "Aliou",
        "age": 20
    }
)
```

Le chemin :

```text
users/1
```

permet d'identifier directement l'entrée.

Utilisez cette approche lorsque votre structure de données reste relativement simple.

---

## Sous-collections

Les sous-collections permettent de représenter une relation hiérarchique.

Exemple :

```python
db.set_subcollection(
    "groups",
    "1",
    {
        "name": "Admins"
    }
)
```

Ici :

```text
groups
└── 1
    └── name
```

La sous-collection permet donc de regrouper plusieurs entrées sous une même collection parent.

---

## Différences principales

| Critère                 | `set_data`      | Sous-collections                    |
| ----------------------- | --------------- | ----------------------------------- |
| Structure               | Directe         | Hiérarchique                        |
| Méthode de création     | `set_data()`    | `set_subcollection()`               |
| Méthode de modification | `edit_data()`   | `edit_subcollection()`              |
| Méthode de lecture      | `get_data()`    | `get_subcollection()`               |
| Méthode de suppression  | `remove_data()` | `remove_subcollection()`            |
| Cas d'utilisation       | Données simples | Données regroupées et hiérarchiques |

### Utiliser `set_data`

```python
db.set_data(
    "users/1",
    {
        "name": "Aliou"
    }
)
```

### Utiliser une sous-collection

```python
db.set_subcollection(
    "groups",
    "1",
    {
        "name": "Admins"
    }
)
```

En pratique, choisissez `set_data` lorsque vos données peuvent être organisées simplement par chemin et utilisez les sous-collections lorsque la relation entre les données nécessite une structure hiérarchique.

---

# API rapide

## Initialisation

```python
LiteJsonDb.JsonDB(
    enable_log=False,
    auto_backup=False,
    crypted=False,
    encryption_method=None,
    encryption_key=None
)
```

Les paramètres permettent de configurer le comportement général de la base.

---

## Données principales

### Créer

```python
db.set_data(path, data)
```

### Modifier

```python
db.edit_data(path, data)
```

### Lire

```python
db.get_data(path)
```

### Supprimer

```python
db.remove_data(path)
```

### Lire toute la base

```python
db.get_db(raw=True)
```

---

## Recherche

### Recherche globale

```python
db.search_data(value)
```

### Recherche dans une clé

```python
db.search_data(
    value,
    key="users"
)
```

---

## Sous-collections

### Créer

```python
db.set_subcollection(
    parent,
    key,
    data
)
```

### Modifier

```python
db.edit_subcollection(
    parent,
    key,
    data
)
```

### Lire

```python
db.get_subcollection(
    parent
)
```

ou :

```python
db.get_subcollection(
    parent,
    key
)
```

### Supprimer

```python
db.remove_subcollection(
    parent,
    key
)
```

---

## Sauvegarde Telegram

```python
db.backup_to_telegram(
    bot_token,
    chat_id
)
```

---

## Export CSV

Exporter une collection :

```python
db.export_to_csv(
    "users"
)
```

Exporter toute la base :

```python
db.export_to_csv()
```

---

# Roadmap

Les fonctionnalités suivantes sont actuellement présentes ou prévues.

* [x] Chiffrement des données JSON
* [x] Sauvegardes automatiques
* [x] Gestion des erreurs
* [x] Documentation française
* [x] Sauvegarde vers Telegram
* [x] Recherche de données
* [x] Export CSV
* [x] Sous-collections
* [ ] Corriger les bugs actuellement connus
* [ ] Continuer à améliorer la stabilité du package
* [ ] Atteindre 100 étoiles sur GitHub
* [ ] Ajouter de nouvelles fonctionnalités

La roadmap peut évoluer en fonction des besoins du projet et des contributions de la communauté.

---

# Contribuer

Les contributions sont ouvertes.

Vous pouvez contribuer de plusieurs manières :

## Corriger un bug

Si vous trouvez un problème, ouvrez une issue dans le dépôt.

Incluez autant d'informations que possible :

* version de LiteJsonDb ;
* version de Python ;
* système d'exploitation ;
* code permettant de reproduire le problème ;
* erreur complète ;
* comportement attendu ;
* comportement observé.

---

## Ajouter une fonctionnalité

Pour proposer une nouvelle fonctionnalité :

1. créez une branche dédiée ;
2. implémentez la modification ;
3. testez le comportement ;
4. documentez l'API ajoutée ;
5. ouvrez une Pull Request.

Exemple :

```bash
git checkout -b feature/nouvelle-fonctionnalite
```

Après vos modifications :

```bash
git add .
git commit -m "feat: ajouter une nouvelle fonctionnalité"
git push origin feature/nouvelle-fonctionnalite
```

Puis ouvrez une Pull Request sur GitHub.

---

## Améliorer la documentation

Les corrections de documentation sont également les bienvenues.

Vous pouvez notamment améliorer :

* les exemples ;
* les explications de l'API ;
* les cas d'utilisation ;
* les messages d'erreur ;
* la documentation française ;
* les exemples de configuration.

---

# Soutenir le projet

Si LiteJsonDb vous est utile, plusieurs formes de contribution sont possibles.

## GitHub

Vous pouvez :

* utiliser le projet ;
* signaler des bugs ;
* proposer des fonctionnalités ;
* contribuer au code ;
* forker le dépôt ;
* donner une étoile au projet.

Une étoile GitHub permet également de rendre le projet plus visible auprès d'autres développeurs.

---

## Don

Vous pouvez également soutenir financièrement le projet.

### PayPal

[Effectuer un don via PayPal](https://paypal.me/djibson35)

### Bitcoin

Adresse Bitcoin :

```text
1Nn15EttfT2dVBisj8bXCnBiXjcqk1ehWR
```

---

# Documentation

Pour les fonctionnalités complémentaires et les exemples détaillés, consultez le wiki :

https://github.com/codingtuto/LiteJsonDb/wiki

Documentation française :

```text
./README.fr.md
```

---

# Licence et utilisation

Reportez-vous aux fichiers du dépôt pour connaître les conditions de licence applicables au projet.

---

# Auteur et projet

LiteJsonDb est développé et maintenu autour d'une idée simple : fournir une interface JSON locale suffisamment légère pour les projets Python qui n'ont pas besoin d'une infrastructure de base de données complète.

Le projet reste volontairement simple dans son utilisation :

```python
import LiteJsonDb

db = LiteJsonDb.JsonDB()

db.set_data(
    "users/1",
    {
        "name": "Aliou"
    }
)

print(
    db.get_data("users/1")
)
```

Pour des besoins plus avancés, les fonctionnalités de chiffrement, sauvegarde, recherche, sous-collections et export permettent d'étendre cette base sans changer complètement l'API.

---

## Liens

* [PyPI](https://pypi.org/project/LiteJsonDb/)
* [GitHub](https://github.com/codingtuto/LiteJsonDb)
* [Wiki](https://github.com/codingtuto/LiteJsonDb/wiki)
* [Documentation française](./README.fr.md)

---

Bon code.
