# LiteJsonDb

A lightweight JSON database for Python applications that need simple, reliable data storage without the complexity of a traditional database server.

![PyPI downloads](https://img.shields.io/pypi/dm/LiteJsonDb.svg)
![PyPI package version](https://img.shields.io/pypi/v/LiteJsonDb.svg)
![GitHub stars](https://img.shields.io/github/stars/codingtuto/LiteJsonDb)
![GitHub forks](https://img.shields.io/github/forks/codingtuto/LiteJsonDb)

[Documentation in French](./README.fr.md)

---

## Overview

LiteJsonDb is designed for developers who want a minimal persistence layer for local or small-scale applications. It stores data in JSON files and exposes a simple API for CRUD operations, nested data structures, backups, and optional encryption.

This project is especially useful for:

- small applications and prototypes
- local tooling and scripts
- configuration storage
- embedded or offline-first systems
- projects that need quick persistence without a database service

Unlike full database systems, LiteJsonDb keeps the model simple: a JSON file on disk, a few focused methods, and predictable behavior.

---

## Why use LiteJsonDb?

Many projects do not need the overhead of Postgres, MongoDB, or SQLite. In these cases, a file-based JSON store can be enough.

LiteJsonDb offers a practical balance between simplicity and functionality:

- easy to integrate into Python applications
- no external database server required
- file-based storage with JSON structure
- support for nested collections and hierarchical data
- optional backups and encryption
- atomic writes to reduce corruption risk

---

## Features

- CRUD operations for JSON data
- nested subcollections and hierarchical paths
- automatic backups
- optional encryption with Base64 or Fernet
- logging support for debugging
- external file change detection
- atomic saving with temp-file replacement
- batch writes for large imports
- CSV export support
- search functionality across stored values

---

## Installation

Install the package with pip:

```bash
pip install litejsondb
```

To upgrade to the latest version:

```bash
pip install --upgrade litejsondb
```

---

## Quick Start

```python
import LiteJsonDb

# Initialize the database
# All data is stored in a JSON file on disk.
db = LiteJsonDb.JsonDB()

# Create data
db.set_data("users/1", {"name": "Aliou", "age": 20})
db.set_data("users/2", {"name": "Coder", "age": 25})

# Read data
print(db.get_data("users/1"))

# Update data
 db.edit_data("users/1", {"age": 21})

# Delete data
# db.remove_data("users/2")

# Get the full database
print(db.get_db(raw=True))
```

---

## Configuration

The `JsonDB` constructor accepts several options depending on the behavior you need.

### Logging

```python
db = LiteJsonDb.JsonDB(enable_log=True)
```

Enable logging to trace database operations and debug issues more easily.

### Automatic backups

```python
db = LiteJsonDb.JsonDB(auto_backup=True)
```

With backup enabled, LiteJsonDb creates backup copies during saves to reduce the risk of data loss.

### Encryption

Base64 encryption is available by default when `crypted=True` is passed.

```python
db = LiteJsonDb.JsonDB(crypted=True)
```

Fernet encryption is also supported for stronger protection:

```python
db = LiteJsonDb.JsonDB(
    crypted=True,
    encryption_method="fernet",
    encryption_key="your-secret-key"
)
```

If you use Fernet and no key is provided, an error is raised to prevent insecure data handling.

### Pretty-printed JSON output

```python
db = LiteJsonDb.JsonDB(indent=4)
```

This writes a more readable JSON file instead of compact output.

---

## Core API

### set_data

Set a value at a specific path.

```python
db.set_data("posts", [])
db.set_data("users/1", {"name": "Aliou", "age": 20})
```

If the key exists, `set_data` will typically indicate that you should use `edit_data` instead.

### edit_data

Merge new data into an existing item.

```python
db.edit_data("users/1", {"name": "Alex"})
```

### get_data

Read data from a path.

```python
print(db.get_data("users/1"))
print(db.get_data("users/1/name"))
```

### remove_data

Delete a value by path.

```python
db.remove_data("users/2")
```

### get_db

Return the whole database contents.

```python
print(db.get_db(raw=True))
```

---

## Search

LiteJsonDb includes a search feature for looking up values across the database.

### Basic search

```python
results = db.search_data("Aliou")
print(results)
```

This searches for the value across the database.

### Search within a specific key

```python
results = db.search_data("Aliou", key="users")
print(results)
```

---

## Subcollections

Subcollections let you organize data in a hierarchical structure.

```python
db.set_subcollection("groups", "1", {"name": "Admins"})
db.edit_subcollection("groups", "1", {"description": "Admin group"})
print(db.get_subcollection("groups"))
print(db.get_subcollection("groups", "1"))
```

Use subcollections when you need a nested structure instead of flat key-value entries.

---

## Batch Writes

Batch mode is useful when you need to insert a large number of records efficiently.

```python
with db.batch():
    for i in range(100000):
        db.set_data(f"users/{i}", {"name": f"user{i}"})
```

Writes are deferred and executed once at the end of the block, which can significantly reduce disk overhead for large imports.

---

## Data Integrity and Reliability

LiteJsonDb includes a few safeguards to reduce common pitfalls in file-based storage:

- atomic writes through temporary file replacement
- detection of external file modification
- automatic reload when the JSON file changes outside the process
- backups to protect against accidental data loss

This makes it more reliable than a raw JSON file handler for stateful local applications.

---

## Export and Backup Features

### Export to CSV

```python
db.set_data("users", {
    "1": {"name": "Aliou", "age": 20},
    "2": {"name": "Coder", "age": 25}
})

db.export_to_csv("users")
# or export the full database
db.export_to_csv()
```

### Telegram backup

```python
db.backup_to_telegram("your_token", "your_chat_id")
```

This is useful if you want to send a database backup to a Telegram chat for monitoring or recovery.

---

## Example Project Structure

```text
project/
├── database/
│   ├── db.json
│   ├── db_backup.json
│   └── LiteJsonDb.log
└── main.py
```

---

## Full Example

```python
import LiteJsonDb

# Create a database instance
db = LiteJsonDb.JsonDB(
    enable_log=True,
    auto_backup=True,
    crypted=True,
    encryption_method="fernet",
    encryption_key="my-secure-key"
)

# Set data
db.set_data("posts")
db.set_data("users/1", {"name": "Aliou", "age": 20})
db.set_data("users/2", {"name": "Coder", "age": 25})

# Update and retrieve data
db.edit_data("users/1", {"name": "Alex"})
print(db.get_data("users/1"))
print(db.get_data("users/2"))

# Search data
print(db.search_data("Aliou"))
print(db.search_data("Aliou", key="users"))

# Subcollections
db.set_subcollection("groups", "1", {"name": "Admins"})
db.edit_subcollection("groups", "1", {"description": "Admin group"})
print(db.get_subcollection("groups"))

# Remove data
db.remove_data("users/2")

# Full database snapshot
print(db.get_db(raw=True))
```

---

## When to Use LiteJsonDb

LiteJsonDb is a good fit when you need:

- a simple persistent layer for local apps
- JSON-based storage without database setup
- quick prototyping and iteration
- lightweight configuration or metadata persistence
- small-scale document-style storage

It is not designed to replace a full relational or document database for high-concurrency, large-scale, or distributed workloads.

---

## Roadmap

Planned or ongoing improvements include:

- bug fixes and reliability improvements
- enhanced API consistency
- broader documentation examples
- additional data management utilities

---

## Contributing

Contributions are welcome. If you want to improve the project, fix a bug, or propose a feature, open an issue or submit a pull request.

The project benefits from community feedback, especially when it improves usability, reliability, and developer experience.

---

## License

This project is distributed under the license defined in the repository.

---

## Support

If you are using LiteJsonDb in a project and need help, open an issue in the repository with a clear description of the problem and the expected behavior.

This project is intentionally simple, but it is designed to be practical, reliable, and easy to adopt.
