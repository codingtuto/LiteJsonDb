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
> [!NOTE]
> We’ve just added some awesome new utilities to `LiteJsonDb` to make your coding even smoother. For a quick overview and examples, check out our [wiki](https://github.com/codingtuto/LiteJsonDb/wiki/LiteJsonDb-Utility-Functions) for all the details.
---

## :eyes: Overview

Hey there! Welcome to **LiteJsonDb**, your friendly, lightweight JSON-based database. Inspired by the simplicity and real-time capabilities of Firestore, LiteJsonDb makes managing your data a breeze. It's packed with features like encryption, backups, and solid error handling—all without the heavy lifting.

## :thinking: Why LiteJsonDb?

Let's face it: sometimes you don't need a complex database setup. Maybe you're building a small project, a quick prototype, or you just want a straightforward way to store and retrieve JSON data. LiteJsonDb is here for those moments. It's simple, efficient, and gets the job done without any fuss.

## :hammer_and_wrench: Features

- **Easy Data Management**: Add, edit, retrieve, and delete data with just a few lines of code.
- **Data Encryption**: Keep your data secure with optional encryption (base64 or AES).
- **Backup and Restore**: Automatic backups to keep your data safe. Backup to Telegram.
- **Subcollections**: Organize your data in neat, nested structures.
- **Friendly Error Handling**: Helpful, colorful error messages to guide you.
- **Data Search**: Search for specific values within your database.
- **CSV Export**: Export your data to CSV format.

> [!NOTE]
> LiteJsonDb makes managing JSON data simple and enjoyable. Whether you're building a small app or just need a lightweight data storage solution, LiteJsonDb has you covered. Enjoy! 

## :man_technologist: Installation

Getting started is super easy. Just install the package via pip:

```bash
pip install litejsondb
```

To upgrade to a newer version, use:

```bash
pip install --upgrade litejsondb
```

## :crystal_ball: Usage

### :white_check_mark: Initial Setup

First, import the `JsonDB` class and initialize your database:

```python
import LiteJsonDb

# Initialize with base64 encryption (default)
db = LiteJsonDb.JsonDB()  

# Initialize with AES encryption (requires a key)
db = LiteJsonDb.JsonDB(encryption_method="aes", encryption_key="your_secret_key")

# Initialize without encryption
db = LiteJsonDb.JsonDB(encryption_method="none")

# Migrate data to a new encryption method (e.g., from base64 to AES)
# db.migrate_data(new_encryption_method="aes", new_encryption_key="your_new_secret_key")
```

### 🤗 Basic Operations

#### :heavy_plus_sign: Setting Data

```python
# Set data without extra data
db.set_data("posts")

# Set data with extra data
db.set_data("users/1", {"name": "Aliou", "age": 20})
db.set_data("users/2", {"name": "Coder", "age": 25})
```

#### :writing_hand: Editing Data

```python
# Edit data
db.edit_data("users/1", {"name": "Alex"})
```

#### :ballot_box_with_check: Getting Data

```python
# Get data
print(db.get_data("users/1"))  # Output: {'name': 'Alex', 'age': 20}
print(db.get_data("users/2"))  # Output: {'name': 'Coder', 'age': 25}

# Access specific data using paths
print(db.get_data("users/1/name"))  # Output: Alex
```

#### :wastebasket: Removing Data

```python
# Remove data
db.remove_data("users/2")
```

#### :package: Full Database Retrieval

```python
# Get the full database (readable format)
print(db.get_db(raw=True))

# Get the full database (encrypted/raw format depending on initialization)
print(db.get_db())
```

## 🔍 Search Data

This feature allows efficient searching for values within the database.

```python
# Basic search (anywhere in the database)
results = db.search_data("Aliou")
print("Basic Search Results:", results)

# Key-specific search
results = db.search_data("Aliou", key="users")
print("Key-specific Search Results:", results)
```

## 📦 Backup to Telegram

Securely back up your database to a Telegram chat.

```python
# Replace with your bot token and chat ID
db.backup_to_telegram("YOUR_BOT_TOKEN", "YOUR_CHAT_ID") 
```

See the "Backup to Telegram (new)" section above for how to obtain your token and chat ID.

## 📦 Export to CSV

Export data to CSV format for easy sharing and analysis.

```python
# Export a specific collection
db.export_to_csv("users") 

# Export the entire database
db.export_to_csv()
```

## 🐛 Error Handling

LiteJsonDb provides helpful error messages for various scenarios (key exists, key not found, file issues).

### :file_folder: Working with Subcollections

#### :heavy_plus_sign: Setting Subcollection Data

```python
db.set_subcollection("groups", "1", {"name": "Admins"})
```

#### :writing_hand: Editing Subcollection Data

```python
db.edit_subcollection("groups", "1", {"description": "Admin group"})
```

#### :ballot_box_with_check: Getting Subcollection Data

```python
print(db.get_subcollection("groups"))       # Entire subcollection
print(db.get_subcollection("groups", "1"))  # Specific item
```

#### :wastebasket: Removing Subcollection Data

```python
db.remove_subcollection("groups", "1")     # Specific item
db.remove_subcollection("groups")          # Entire subcollection
```

## :memo: Understanding `set_data` vs. Subcollections

<details>
<summary>Click to expand</summary>

### `set_data`

The `set_data` method is used to add or update data at a specific path. If the key already exists, you will need to use `edit_data` to modify it. This method is great for simple key-value pairs or straightforward data structures.

<pre>
# Set data
db.set_data("users/1", {"name": "Aliou", "age": 20})
</pre>

### Subcollections

Subcollections, on the other hand, are used to create and manage nested structures within your database. They allow you to group related data under a parent key, providing a more organized way to handle complex relationships. Subcollections are essentially collections within collections.

<pre>
# Set subcollection data
db.set_subcollection("groups", "1", {"name": "Admins"})
</pre>

### Key Differences

- **Structure**: `set_data` is used for flat data structures, while subcollections allow for hierarchical organization.
- **Usage**: Use `set_data` for simple key-value pairs and `set_subcollection` when you need nested collections.
- **Organization**: Subcollections help in maintaining a clear structure and grouping related data together, making it easier to manage and query complex relationships.

By understanding these differences, you can choose the appropriate method for your data management needs, ensuring a well-organized and efficient database.

</details>

## 🧾 TODO: What's Next for LiteJsonDb

We’re always striving to enhance LiteJsonDb. Here’s what’s on our radar:

- [x] Add support for data encryption to secure JSON content.
- [x] Implement automatic backups to ensure data safety.
- [x] Improve error handling with friendly, colorful messages.
- [x] Added french language documentation
- [x] Implement automated backups to send data to a Telegram bot.
- [ ] Fix any bugs that are discovered to ensure smooth operation.
- [ ] Reach 100 stars on GitHub and celebrate by adding more awesome features! 

## :hugs: Contributions and Community
We welcome contributions, suggestions, and feedback to make LiteJsonDb even better! If you have ideas for improvements or want to fix a bug, feel free to:

- **Submit a Pull Request (PR)**: Contribute new features or bug fixes by creating a pull request. Your changes will help improve LiteJsonDb for everyone!
- **Report Issues**: If you encounter any bugs or issues, please open an issue in the repository. Provide as much detail as possible so we can address it swiftly.
- **Suggest Features**: Have an idea for a new feature? Let us know! We’re always open to suggestions on how to enhance LiteJsonDb.

> Your feedback and contributions are greatly appreciated and help us keep LiteJsonDb growing and improving.

## :heart: Donations and Support: How You Can Help

LiteJsonDb is a labor of love, and your support can make a big difference! If you’re enjoying the project and want to show your appreciation, here are a few ways you can help:

### Fork and Star the Repo

One of the best ways to support LiteJsonDb is to fork the repository and give it a star on GitHub. It’s like a virtual high-five and helps us spread the word about the project. Plus, it shows us that you value the work we’re doing!

### Consider a Donation

If you’re feeling extra generous and want to contribute financially, we’d be incredibly grateful. Donations help us cover costs and keep the project running smoothly. You can support us in the following ways:

- **PayPal**: Send a donation directly to [my PayPal account](https://paypal.me/djibson35). Every little bit helps and is greatly appreciated!
- **Bitcoin**: Prefer cryptocurrency? You can also donate using Bitcoin to the following address: `1Nn15EttfT2dVBisj8bXCnBiXjcqk1ehWR`.

> Your support, whether through a star, a fork, or a donation, helps keep LiteJsonDb alive and thriving. Thank you for being awesome!

Cheers and happy coding! :rocket:
