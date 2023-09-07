# SpeckApp Documentation | NON-OFFICAL

**SpeckApp** is a Python application designed to assist users in manually validating documents stored in a MongoDB database. It provides a graphical interface for reviewing and updating document records, along with the ability to view associated files and copy document IDs to the clipboard. This documentation provides an overview of the SpeckApp code, its functionality, and how to use it.

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Functionality](#functionality)
6. [Example Document](#example-document)
7. [Developer Information](#developer-information)

## Introduction

SpeckApp is a helper application for the [SPECK Project](https://spritz.math.unipd.it/projects/speck/) developed by the SPRITZ Research Group. It assists users in manually validating documents stored in a MongoDB database. Below are some key resources related to the SPECK Project:

- [SPECK Project Website](https://spritz.math.unipd.it/projects/speck/)
- [SPECK GitHub Repository](https://github.com/SPRITZ-Research-Group/SPECK)

## Prerequisites

Before using SpeckApp, ensure you have the following prerequisites:

- Python 3
- The following Python packages, which can be installed using `pip`:
  - `pymongo`
  - `pyperclip`
  - `flet`

## Installation

To set up SpeckApp on your local machine, follow these steps:

1. Clone or download the SpeckApp repository to your local machine.

2. Navigate to the SpeckApp directory.

3. Ensure you have the required Python packages installed by running the following command:

   ```bash
   pip install pymongo pyperclip flet
   ```

4. Run the SpeckApp application using the following command:

   ```bash
   python app.py
   ```

## Usage

Once SpeckApp is running, you can use the graphical interface to review and update document records in the MongoDB database. The application consists of two main sections: information display and control buttons.

### Information Display Section

- **MongoDB URI Input**: Enter your MongoDB connection URI in this text field and click "Connect to DB" to establish a connection.

- **Console View**: This section displays status messages and error notifications. It provides feedback on database connections and other operations.

- **JSON View**: Displays the JSON representation of the current document for review. You can see and edit the document's details here.

- **Rule View**: Shows the rule associated with the current document for reference.

### Control Buttons Section

- **Prev**: Navigate to the previous document in the database.

- **False & Next**: Mark the current document as "False" and move to the next document.

- **True & Next**: Mark the current document as "True" and move to the next document.

- **Next**: Move to the next document without marking the current one.

- **Show In Editor**: Open the associated file of the current document in the default text editor.

- **Copy ID**: Copy the unique document ID to the clipboard for reference.

### Reviewing Documents

1. Enter the MongoDB URI in the input field and click "Connect to DB" to establish a connection.

2. Use the control buttons to navigate through documents, review their details in the JSON View, and update their validation status and comments.

3. Click "Show In Editor" to open the associated file in your text editor (if available).

4. Click "Copy ID" to copy the document's unique ID to the clipboard for reference.

## Functionality

SpeckApp offers the following functionality:

- **Connect to MongoDB**: SpeckApp allows you to connect to a MongoDB database using a provided URI.

- **Document Navigation**: You can navigate through documents in the database using "Prev" and "Next" buttons.

- **Validation**: You can mark documents as "True" or "False" to indicate their validity.

- **Commenting**: You can add comments to documents for additional information.

- **File Viewing**: SpeckApp provides an option to open associated files in the default text editor.

- **Clipboard Copy**: You can copy the document ID to the clipboard for reference.

- **Logging**: The application logs document updates to a CSV file for record-keeping.

## Example Document

[Include an example document here if applicable]

## Developer Information

The SpeckApp code is written in Python and uses the following libraries:

- `pymongo`: for connecting to the MongoDB database.
- `pyperclip`: for copying document IDs to the clipboard.
- `flet`: a user interface library for creating the graphical interface.

If you're a developer looking to extend or modify SpeckApp, you can explore the code in `app.py`. The code includes comments and explanations for various functions and components used in the application. Customize it to meet your specific needs.