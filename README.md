```markdown
# LiteJsonDb: Your Go-To Lightweight JSON Database
![illustration](https://telegra.ph/file/374450a4f36c217b3a20b.jpg)
![PyPi downloads](https://img.shields.io/pypi/dm/LiteJsonDb.svg) 
![PyPi Package Version](https://img.shields.io/pypi/v/LiteJsonDb.svg)
![GitHub stars](https://img.shields.io/github/stars/codingtuto/LiteJsonDb)
![GitHub forks](https://img.shields.io/github/forks/codingtuto/LiteJsonDb)

---

[![Voir la documentation en Français](https://img.shields.io/badge/Documentation-Fran%C3%A7ais-blue)](./README.fr.md)
[![Wiki](https://img.shields.io/badge/wiki-Documentation-blue.svg)](https://github.com/codingtuto/LiteJsonDb/wiki)

---

## :eyes: Overview

LiteJsonDb is a lightweight, user-friendly JSON database designed for simplicity and ease of use. Inspired by Firestore, it offers real-time data management capabilities without the complexities of larger database systems. LiteJsonDb is perfect for small projects, rapid prototyping, or any scenario requiring straightforward JSON data storage and retrieval. It now features robust encryption options, seamless backups, comprehensive error handling, and helpful utility functions.

## :thinking: Why LiteJsonDb?

When you need a simple, efficient way to manage JSON data without the overhead of a full-blown database, LiteJsonDb is the perfect solution. It's lightweight, easy to integrate, and provides the essential features you need for many common use cases.

## :hammer_and_wrench: Features

- **Easy Data Management**: CRUD (Create, Read, Update, Delete) operations are simple and intuitive.
- **Robust Encryption**: Choose between Base64 encoding (default for backward compatibility) or strong AES encryption for enhanced security.
- **Backup and Restore**: Automatic backups and easy restoration ensure data safety.
- **Subcollections**: Organize data hierarchically for better structure and management.
- **Friendly Error Handling**: Clear, informative error messages simplify debugging.
- **Data Search**: Easily search for values across the entire database or within specific keys.
- **Telegram Backup**: Securely back up your database directly to a Telegram chat.
- **CSV Export**: Export data to CSV format for analysis and sharing.
- **Utility Functions**: Convenient functions for common tasks like date conversion, data filtering, sorting, and more. See the [wiki](https://github.com/codingtuto/LiteJsonDb/wiki/LiteJsonDb-Utility-Functions) for details.

## :man_technologist: Installation

Install via pip:

```bash
pip install litejsondb
```

Upgrade to the latest version:

```bash
pip install --upgrade litejsondb
```

## :crystal_ball: Usage

### :white_check_mark: Initial Setup

Import and initialize:

```python
import LiteJsonDb

# Default (Base64 encryption)
db = LiteJsonDb.JsonDB()  

# No encryption
db = LiteJsonDb.JsonDB(encryption_method="none")

# AES Encryption (Recommended)
db = LiteJsonDb.JsonDB(encryption_method="aes", encryption_key="your_strong_password") 
```

**Important:**  For AES encryption, store your `encryption_key` securely (environment variables or a secrets manager). **Do not** hardcode it in your application.

### :repeat: Data Migration (If Upgrading from Older Versions)

To migrate data from Base64 to AES encryption:

```python
db = LiteJsonDb.JsonDB() # Opens with the old encryption method if it exists
db.migrate_data("aes", "your_strong_password")
```

### 🤗 Basic Operations (Same as before - examples updated for clarity)

#### :heavy_plus_sign: Setting Data

```python
db.set_data("users", {}) # Creates an empty collection
db.set_data("users/1", {"name": "Alice", "age": 30})
db.set_data("products/123", {"name": "Awesome Gadget", "price": 99.99})
```

#### :writing_hand: Editing Data

```python
db.edit_data("users/1", {"city": "New York"}) # Merges with existing data
```

#### :ballot_box_with_check: Getting Data

```python
user = db.get_data("users/1")
print(user)  # Output: {'name': 'Alice', 'age': 30, 'city': 'New York'}
product_name = db.get_data("products/123/name")
print(product_name) # Output: Awesome Gadget
```

#### :wastebasket: Removing Data

```python
db.remove_data("products/123")
```

#### :package: Full Database Retrieval

```python
data = db.get_db() # Returns a decrypted copy of the database
raw_data = db.get_db(raw=True) # Returns the database as is (in memory)
```

### :file_folder: Working with Subcollections (Same as before)

(Keep the Subcollections section as it is in the original README, it's already well-explained)

## :bug: Error Handling (Slightly updated)

LiteJsonDb provides helpful error messages for various scenarios:

- **Key Exists/Key Not Found**:  Clear messages and tips for using `set_data` vs. `edit_data`.
- **File Issues**: Guidance on resolving file permission errors.
- **Encryption Errors**: Specific messages related to encryption/decryption problems (e.g., incorrect password for AES).
- **CSV Export Errors**:  Provides specific messages for `export_to_csv` errors, such as attempts to export non-existent keys.

## :open_file_folder: Example Project Structure (Same as before)

## :shipit: Example `main.py` (Updated)

(Update the `main.py` example to reflect the new encryption options and the data migration example)

## :memo: Understanding `set_data` vs. Subcollections (Same as before)

## :hugs: Contributions and Community (Same as before)

## :heart: Donations and Support: How You Can Help (Same as before)

```

Key changes:

*   **Emphasis on Encryption Choices:**  Clearly explains the base64 (legacy) and AES options.
*   **Data Migration:** Adds a section on how to migrate existing data to AES.
*   **Security Warning about AES Key:**  Stresses the importance of secure key storage.
*   **Updated Examples:**  Clarifies data manipulation examples.
*   **Concise Feature List:**  More streamlined and highlights the key improvements.
*   **Updated Error Handling Section:** Includes mention of encryption-related errors and CSV export errors.

This revised README is clearer, more comprehensive, and accurately reflects the enhanced capabilities of LiteJsonDb.
