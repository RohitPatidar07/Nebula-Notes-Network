 
# Nebula Notes Network
Develop a Tkinter application for creating, organizing, and searching notes, with data saved in both local files and a MySQL database
## Overview

**Nebula Notes Network** is a Tkinter-based application designed for creating, organizing, and searching notes. The notes are saved both in local text files and in a MySQL database, offering easy access and efficient management.

## Features

- **Create Notes**: Easily create new notes with a title and content.
- **Save Notes**: Notes are saved both locally (as text files) and in a MySQL database.
- **View Notes**: Select and view the details of any saved note from the list.
- **Organize Notes**: Notes are displayed in a table with their ID, Title, and Timestamp, making it easy to browse and manage them.

## Prerequisites

Before running the application, ensure the following are installed on your system:

- **Python 3.x**
- **Tkinter** (usually comes pre-installed with Python)
- **MySQL Server**
- **MySQL Connector for Python** (`mysql-connector-python`)

## Database Setup

 **Create the Database**:
   ```sql
   CREATE DATABASE tkinter;
