# LiteJsonDb: Your Go-To Lightweight JSON Database
![illustration](https://telegra.ph/file/374450a4f36c217b3a20b.jpg)
![PyPi downloads](https://img.shields.io/pypi/dm/LiteJsonDb.svg) 
![Supported Python versions](https://img.shields.io/pypi/pyversions/LiteJsonDb.svg)
![PyPi Package Version](https://img.shields.io/pypi/v/LiteJsonDb.svg)

## 👀 Overview

Hey there! Welcome to **LiteJsonDb**, your friendly, lightweight JSON-based database. Inspired by the simplicity and real-time capabilities of Firestore, LiteJsonDb makes managing your data a breeze. It's packed with features like encryption, backups, and solid error handling—all without the heavy lifting.

## 🤔 Why LiteJsonDb?

Let's face it: sometimes you don't need a complex database setup. Maybe you're building a small project, a quick prototype, or you just want a straightforward way to store and retrieve JSON data. LiteJsonDb is here for those moments. It's simple, efficient, and gets the job done without any fuss.

## 🛠 Features

- **Easy Data Management**: Add, edit, retrieve, and delete data with just a few lines of code.
- **Data Encryption**: Keep your data secure with optional encryption. 
- **Backup and Restore**: Automatic backups to keep your data safe.
- **Subcollections**: Organize your data in neat, nested structures.
- **Friendly Error Handling**: Helpful, colorful error messages to guide you.

> LiteJsonDb makes managing JSON data simple and enjoyable. Whether you're building a small app or just need a lightweight data storage solution, LiteJsonDb has you covered. Enjoy! 

## 👨‍💻 Installation

Getting started is super easy. Just install package via pip and you're good to go:

´´´
pip install LiteJsonDb
´´´

## 🔮 Usage

### ✅ Initial Setup

First things first, import the `JsonDB` class and initialize your database:

´´´
import LiteJsonDb

# Initialize the database with encryption enabled
db = LiteJsonDb.JsonDB(crypted=True)
´´´

### 🤗 Basic Operations

#### ➕ Setting Data

Adding data is a breeze. Just use the `set_data` method. If the key already exists, you'll get a friendly reminder to use `edit_data` instead.

´´´
# Set data
db.set_data("users/1", {"name": "Aliou", "age": 20})
db.set_data("users/2", {"name": "Coder", "age": 25})
´´´

#### ✍ Editing Data

Need to update data? No problem. Use the `edit_data` method. It merges the new data with the existing data, so nothing gets lost.

´´´
# Edit data
db.edit_data("users/1", {"name": "Alex"})
´´´

#### 🗳 Getting Data

Retrieving data is as simple as it gets. Use the `get_data` method.

´´´
# Get data
print(db.get_data("users/1"))  # Output: {'name': 'Alex', 'age': 20}
print(db.get_data("users/2"))  # Output: {'name': 'Coder', 'age': 25}
´´´

#### 🗑 Removing Data

Need to delete something? The `remove_data` method has you covered.

´´´
# Remove data
db.remove_data("users/2")
´´´

#### 📦 Full Database Retrieval

Want to see everything? Use the `get_db` method. Set `raw=True` if you want the data in a readable format.

´´´
# Get the full database
print(db.get_db(raw=True))
´´´

### 🗂 Working with Subcollections

## 📁 Subcollections

In LiteJsonDb, subcollections are a way to organize your data hierarchically. Think of them as nested structures that allow you to group related data together under a parent key. This feature is especially useful when you want to manage complex data relationships without losing the simplicity of JSON.

### 🧐 What Are Subcollections?

Subcollections are essentially collections within collections. For example, if you have a main collection of users, you might want to organize their posts into separate subcollections. Here’s how you can work with them:

- **Setting Subcollection Data**: Create and populate a subcollection under a specified parent key.
- **Editing Subcollection Data**: Update existing items in a subcollection.
- **Getting Subcollection Data**: Retrieve the data stored within a subcollection.
- **Removing Subcollection Data**: Delete items or entire subcollections.

Using subcollections helps you maintain a clear structure in your data, making it easier to manage and query.

#### ➕ Setting Subcollection Data

Organize your data with subcollections. Easy peasy.

´´´
# Set subcollection data
db.set_subcollection("groups", "1", {"name": "Admins"})
´´´

#### ✍ Editing Subcollection Data

Editing items within a subcollection? No sweat.

´´´
# Edit subcollection data
db.edit_subcollection("groups", "1", {"description": "Admin group"})
´´´

#### 🗳 Getting Subcollection Data

Need to retrieve specific subcollections or items? We've got you.

´´´
# Get subcollection data
print(db.get_subcollection("groups"))

# Get custom item from the subcollection data
print(db.get_subcollection("groups", "1"))
´´´

#### 🗑 Removing Subcollection Data

Removing items from subcollections is just as simple.

´´´
# Remove subcollection data
db.remove_subcollection("groups", "1")
´´´

## 🐞 Error Handling

LiteJsonDb is all about being helpful. Here are some friendly, colorful error messages to guide you:

- **Key Exists**: If you try to set data with an existing key, it will suggest using `edit_data`.
- **Key Not Found**: If a key does not exist when you try to get or remove data, it will notify you with a tip on how to proceed.
- **File Issues**: If there are file permission problems, it will guide you on how to fix them.

## 📂 Example Project Structure

Here's how your project might look:

´´´
project/
│
├── database/
│   ├── db.json
│   ├── db_backup.json
│   └── LiteJsonDb.log
└── your_code.py
´´´

## Example `main.py`

Let's put it all together with an example `main.py` file:

´´´
import LiteJsonDb

# Initialize the database with encryption enabled
db = LiteJsonDb.JsonDB(crypted=True)

# Add some initial data
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
´´´

## 🤗 Contributions and Community
We welcome contributions, suggestions, and feedback to make LiteJsonDb even better! If you have ideas for improvements or want to fix a bug, feel free to:

- **Submit a Pull Request (PR)**: Contribute new features or bug fixes by creating a pull request. Your changes will help improve LiteJsonDb for everyone!
- **Report Issues**: If you encounter any bugs or issues, please open an issue in the repository. Provide as much detail as possible so we can address it swiftly.
- **Suggest Features**: Have an idea for a new feature? Let us know! We’re always open to suggestions on how to enhance LiteJsonDb.

> Your feedback and contributions are greatly appreciated and help us keep LiteJsonDb growing and improving.

## ❤ Donations and Support: How You Can Help

Json2DB-Lite is a labor of love, and your support can make a big difference! If you’re enjoying the project and want to show your appreciation, here are a few ways you can help:

### Fork and Star the Repo

One of the best ways to support Json2DB-Lite is to fork the repository and give it a star on GitHub. It’s like a virtual high-five and helps us spread the word about the project. Plus, it shows us that you value the work we’re doing!

### Consider a Donation

If you’re feeling extra generous and want to contribute financially, we’d be incredibly grateful. Donations help us cover costs and keep the project running smoothly. You can support us in the following ways:

- **PayPal**: Send a donation directly to [my PayPal account](https://paypal.me/djibson35). Every little bit helps and is greatly appreciated!
- **Bitcoin**: Prefer cryptocurrency? You can also donate using Bitcoin to the following address: `1Nn15EttfT2dVBisj8bXCnBiXjcqk1ehWR`.

> Your support, whether through a star, a fork, or a donation, helps keep Json2DB-Lite alive and thriving. Thank you for being awesome!

Cheers and happy coding! 🚀✨