<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="guardianpy/src/guardianpy.png" alt="Project logo"></a>
</p>

<h3 align="center">Guardianpy</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/Salvatore-Rendo/guardianpy.svg)](https://github.com/Salvatore-Rendo/guardianpy/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/Salvatore-Rendo/guardianpy.svg)](https://github.com/Salvatore-Rendo/guardianpy/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> An easy to use Password Manager made with Python 
    <br> 
</p>

## 📝 Table of Contents

- [📝 Table of Contents](#-table-of-contents)
- [🧐 About ](#-about-)
  - [How it works](#how-it-works)
- [🏁 Getting Started ](#-getting-started-)
  - [Prerequisites](#prerequisites)
  - [Installing](#installing)
- [🎈 Usage ](#-usage-)
- [⛏️ Built Using ](#️-built-using-)
- [✍️ Authors ](#️-authors-)

## 🧐 About <a name = "about"></a>

Guardianpy is a Python-based password manager designed to enhance the security and convenience of managing your online credentials. With Guardianpy, you can securely store your passwords, retrieve them when needed, and generate strong, unique passwords for your accounts. The project prioritizes the privacy and safety of user data by implementing strong encryption techniques.

<b> Guardianpy is still in his beta version, i recommend to wait till version 1.0 at least for a polished and safer release </b>

### How it works

During the login session, the user credentials are checked and the master password is stored for the session.
After the login, the user is redirected to the main window where he can store or retrive the passwords inside the database.
The password are safely stored and retrived using a key generation method using the master password and salt.
During the store session is possible to use a password generetor in which the user can decide the characters and length of the password.

<img src="guardianpy/src/guardianpy-diagram.png">

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 


### Prerequisites

[Tinker](https://docs.python.org/3/library/tkinter.html):
- If not alredy installed:
```
sudo apt-get install python3-tk
```
- for MacOS
```
brew install python3-tk
```

### Installing



```
git clone https://github.com/Salvatore-Rendo/guardianpy
```

```
cd guardianpy
```

```
pip3 install -r requirements.txt
```

## 🎈 Usage <a name="usage"></a>

```
python3 main.py
```


[[TODO -> Images showing how to use]] ////////////////////////////

## ⛏️ Built Using <a name = "built_using"></a>

- [SQLite](https://www.sqlite.org/index.html) - Database
- [Python](https://www.python.org/) - Framework
- [TKinter](https://docs.python.org/3/library/tkinter.html) - GUI Framework
- [Flaticon](https://www.flaticon.com/) Icon

## ✍️ Authors <a name = "authors"></a>

- [@Salvatore-Rendo](https://github.com/Salvatore-Rendo) - Idea & Initial work

