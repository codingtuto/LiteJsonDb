# LiteJsonDb: Your Go-To Lightweight JSON Database
![illustration](https://telegra.ph/file/374450a4f36c217b3a20b.jpg)
![PyPi downloads](https://img.shields.io/pypi/dm/LiteJsonDb.svg) 
![PyPi Package Version](https://img.shields.io/pypi/v/LiteJsonDb.svg)
![GitHub stars](https://img.shields.io/github/stars/codingtuto/LiteJsonDb)
![GitHub forks](https://img.shields.io/github/forks/codingtuto/LiteJsonDb)
---
[![Voir la documentation en Français](https://img.shields.io/badge/Documentation-Fran%C3%A7ais-blue)](./README.fr.md)
[![Wiki](https://img.shields.io/badge/wiki-Documentation-blue.svg)](https://github.com/codingtuto/LiteJsonDb/wiki)

## :eyes: Overview

Hey there! Welcome to **LiteJsonDb**, your friendly, lightweight JSON-based database. Inspired by the simplicity and real-time capabilities of Firestore, LiteJsonDb makes managing your data a breeze. It's packed with features like encryption, backups, and solid error handling—all without the heavy lifting.

## :thinking: Why LiteJsonDb?

Let's face it: sometimes you don't need a complex database setup. Maybe you're building a small project, a quick prototype, or you just want a straightforward way to store and retrieve JSON data. LiteJsonDb is here for those moments. It's simple, efficient, and gets the job done without any fuss.

## :hammer_and_wrench: Features

- **Easy Data Management**: Add, edit, retrieve, and delete data with just a few lines of code.
- **Data Encryption**: Keep your data secure with optional encryption. 
- **Backup and Restore**: Automatic backups to keep your data safe.
- **Subcollections**: Organize your data in neat, nested structures.
- **Friendly Error Handling**: Helpful, colorful error messages to guide you.

> [!NOTE]
> LiteJsonDb makes managing JSON data simple and enjoyable. Whether you're building a small app or just need a lightweight data storage solution, LiteJsonDb has you covered. Enjoy! 

## :man_technologist: Installation

Getting started is super easy. Just install the package via pip and you're good to go:

<pre>
pip install litejsondb
</pre>

A new version is available type `pip install --upgrade litejsondb` to update

## :crystal_ball: Usage

### :white_check_mark: Initial Setup

First things first, import the `JsonDB` class and initialize your database:

<pre>
import LiteJsonDb

# Initialize the database with encryption enabled
db = LiteJsonDb.JsonDB(crypted=True)
</pre>

### 🤗 Basic Operations

#### :heavy_plus_sign: Setting Data

Adding data is a breeze. Just use the `set_data` method. If the key already exists, you'll get a friendly reminder to use `edit_data` instead.

<pre>
# Set data without extra-data
db.set_data("posts")

# Set data with extra-data
db.set_data("users/1", {"name": "Aliou", "age": 20})
db.set_data("users/2", {"name": "Coder", "age": 25})
</pre>

#### :writing_hand: Editing Data

Need to update data? No problem. Use the `edit_data` method. It merges the new data with the existing data, so nothing gets lost.

<pre>
# Edit data
db.edit_data("users/1", {"name": "Alex"})
</pre>

#### :ballot_box_with_check: Getting Data

Retrieving data is as simple as it gets. Use the `get_data` method.

<pre>
# Get data
print(db.get_data("users/1"))  # Output: {'name': 'Alex', 'age': 20}
print(db.get_data("users/2"))  # Output: {'name': 'Coder', 'age': 25}
</pre>

> [!TIP]
> You can directly access specific data by using paths in the `get_data` method. For example, to get only the user's name, you can do:
<pre>
print(db.get_data("users/1/name"))
</pre>

Here, you get the user's name without retrieving other parts of the data.

#### :wastebasket: Removing Data

Need to delete something? The `remove_data` method has you covered.

<pre>
# Remove data
db.remove_data("users/2")
</pre>

#### :package: Full Database Retrieval

Want to see everything? Use the `get_db` method. Set `raw=True` if you want the data in a readable format.

<pre>
# Get the full database
print(db.get_db(raw=True))
</pre>

### :file_folder: Working with Subcollections

## :file_folder: Subcollections

In LiteJsonDb, subcollections are a way to organize your data hierarchically. Think of them as nested structures that allow you to group related data together under a parent key. This feature is especially useful when you want to manage complex data relationships without losing the simplicity of JSON.

### :thinking: What Are Subcollections?

Subcollections are essentially collections within collections. For example, if you have a main collection of users, you might want to organize their posts into separate subcollections. Here’s how you can work with them:

- **Setting Subcollection Data**: Create and populate a subcollection under a specified parent key.
- **Editing Subcollection Data**: Update existing items in a subcollection.
- **Getting Subcollection Data**: Retrieve the data stored within a subcollection.
- **Removing Subcollection Data**: Delete items or entire subcollections.

Using subcollections helps you maintain a clear structure in your data, making it easier to manage and query.

#### :heavy_plus_sign: Setting Subcollection Data

Organize your data with subcollections. Easy peasy.

<pre>
# Set subcollection data
db.set_subcollection("groups", "1", {"name": "Admins"})
</pre>

#### :writing_hand: Editing Subcollection Data

Editing items within a subcollection? No sweat.

<pre>
# Edit subcollection data
db.edit_subcollection("groups", "1", {"description": "Admin group"})
</pre>

#### :ballot_box_with_check: Getting Subcollection Data

Need to retrieve specific subcollections or items? We've got you.

<pre>
# Get subcollection data
print(db.get_subcollection("groups"))

# Get custom item from the subcollection data
print(db.get_subcollection("groups", "1"))
</pre>

#### :wastebasket: Removing Subcollection Data

Removing items from subcollections is just as simple.

<pre>
# Remove subcollection data
db.remove_subcollection("groups", "1")
</pre>

## :bug: Error Handling

LiteJsonDb is all about being helpful. Here are some friendly, colorful error messages to guide you:

- **Key Exists**: If you try to set data with an existing key, it will suggest using `edit_data`.
- **Key Not Found**: If a key does not exist when you try to get or remove data, it will notify you with a tip on how to proceed.
- **File Issues**: If there are file permission problems, it will guide you on how to fix them.

## :open_file_folder: Example Project Structure

Here's how your project might look if your initialized `LiteJssonDb`:

<pre>
project/
│
├── database/
│   ├── db.json
│   ├── db_backup.json
│   └── LiteJsonDb.log
└── your_code.py
</pre>

## :shipit: Example `main.py`

Let's put it all together with an example `main.py` file:

<pre>
import LiteJsonDb
  
# Initialize the database with encryption enabled
db =  LiteJsonDb.JsonDB(crypted=True)

# Add some initial data
# Set data without extra-data
db.set_data("posts")

# Set data with extra-data
db.set_data("users/1", {"name": "Aliou", "age": 20})
db.set_data("users/2", {"name": "Coder", "age": 25})

# Modify existing data
db.edit_data("users/1", {"name": "Alex"})

# Retrieve and print data
print(db.get_data("users/1"))
print(db.get_data("users/2"))

# Remove data
db.remove_data("users/2")

# Retrieve the full database
print(db.get_db(raw=True))

# Work with subcollections
db.set_subcollection("groups", "1", {"name": "Admins"})
db.edit_subcollection("groups", "1", {"description": "Admin group"})
print(db.get_subcollection("groups"))
db.remove_subcollection("groups", "1")
</pre>

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

## 🧾 TODO: What's Next for Json2DB-Lite

We’re always striving to enhance Json2DB-Lite. Here’s what’s on our radar:

- [x] Add support for data encryption to secure JSON content.
- [x] Implement automatic backups to ensure data safety.
- [x] Improve error handling with friendly, colorful messages.
- [x] Added french language documentation
- [ ] Implement automated backups to send data to a Telegram bot.
- [ ] Fix any bugs that are discovered to ensure smooth operation.
- [ ] Reach 100 stars on GitHub and celebrate by adding more awesome features! 

## :hugs: Contributions and Community
We welcome contributions, suggestions, and feedback to make LiteJsonDb even better! If you have ideas for improvements or want to fix a bug, feel free to:

- **Submit a Pull Request (PR)**: Contribute new features or bug fixes by creating a pull request. Your changes will help improve LiteJsonDb for everyone!
- **Report Issues**: If you encounter any bugs or issues, please open an issue in the repository. Provide as much detail as possible so we can address it swiftly.
- **Suggest Features**: Have an idea for a new feature? Let us know! We’re always open to suggestions on how to enhance LiteJsonDb.

> Your feedback and contributions are greatly appreciated and help us keep LiteJsonDb growing and improving.

## :heart: Donations and Support: How You Can Help

Json2DB-Lite is a labor of love, and your support can make a big difference! If you’re enjoying the project and want to show your appreciation, here are a few ways you can help:

### Fork and Star the Repo

One of the best ways to support Json2DB-Lite is to fork the repository and give it a star on GitHub. It’s like a virtual high-five and helps us spread the word about the project. Plus, it shows us that you value the work we’re doing!

### Consider a Donation

If you’re feeling extra generous and want to contribute financially, we’d be incredibly grateful. Donations help us cover costs and keep the project running smoothly. You can support us in the following ways:

- **PayPal**: Send a donation directly to [my PayPal account](https://paypal.me/djibson35). Every little bit helps and is greatly appreciated!
- **Bitcoin**: Prefer cryptocurrency? You can also donate using Bitcoin to the following address: `1Nn15EttfT2dVBisj8bXCnBiXjcqk1ehWR`.

> Your support, whether through a star, a fork, or a donation, helps keep Json2DB-Lite alive and thriving. Thank you for being awesome!

Cheers and happy coding! :rocket:
