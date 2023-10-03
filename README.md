# smhw-api

[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![License](https://img.shields.io/github/license/EpicGamerCodes/smhw-api)

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Dependencies](#dependencies)
5. [Disclaimer](#disclaimer)
6. [License](#license)

## Introduction

The `smhw-api` project allows users to connect to the Satchel: One API using their user credentials. The project is designed to run on Python 3.11.
The responses are returned as objects which are fully type hinted (see `src/smhw_api/objects.py`).
Please note that there is no rate limiting kept by the script yet, so make sure you send API requests appropriately. The script uses the Web client ids by default (to switch to the mobile app client, use the function `Client.change_client()`).

To view and install the latest changes (and for some bug fixes), use the [dev branch](https://github.com/EpicGamerCodes/smhw-api/tree/dev).

If you would like to make a suggestion, simply create an issue! (same for bugs too)

## Features

As of now, the project can perform the following tasks (examples can be viewed in `/examples/`):

- Fetching the user's todo list
- Fetching a specific task and its details
- Fetching quiz data (Questions and previous tries)
- Fetching the user's specific data
- Fetching the user's school data
- Fetching the user's parents data
- Fetching employee data from the school
- Fetching the user's calendar
- Fetching the entire school's calendar
- Fetching the user's behavior (praise points and behavior points)
- Sending Quiz answers
- Sending comments on tasks
- Marking tasks as complete
- Marking tasks as viewed
- Fetching the user's timetable
- Fetching public school data (used to login)
- Fetching student attendance
- Fetching student detentions
- Searching for tasks
- Fetching Notifications

## Installation

### From Github Releases

1. Download the latest wheel file from the [Releases](https://github.com/EpicGamerCodes/smhw-api/releases) page.
2. Install the wheel file using pip:

     ```bash
     pip install /path/to/wheel/file
     ```

### From Source

1. Clone the repository: (use `-b dev` to use new commits)

     ```bash
     git clone https://github.com/EpicGamerCodes/smhw-api.git
     ```

2. Navigate into the cloned repository:

     ```bash
     cd smhw-api
     ```

3. Install the project:

     ```bash
     pip install .
     ```

## Dependencies

The project requires 3 dependencies for running:

- `httpx` - Use HTTP/2 requests
- `h2` - For supporting HTTP/2 requests
- `loguru` - For simple and better formatted logs

## Disclaimer

Users are responsible for their own actions while using this API. Please ensure to comply with any guidelines provided by Satchel: One API. Any consequences resulting from the misuse of this API are solely the user's responsibility.

This project does not use the exact same headers as the Web or Android client yet, therefore Satchel: One can detect if you are using this project.

## License

The project is licensed under the GPL v3 license.
