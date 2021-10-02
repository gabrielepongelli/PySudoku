# PySudoku

A simple Sudoku Game developed by a university computer science student.

![Presentation Image](/images/Presentation_Image.png)

<details open="open">
    <summary>Table of Contents</summary>
    <ol>
        <li>
            <a href="#about-the-project">About The Project</a>
            <ul>
                <li><a href="#built-with">Built With</a></li>
            </ul>
        </li>
        <li>
            <a href="#getting-started">Getting Started</a>
            <ul>
                <li><a href="#prerequisites">Prerequisites</a></li>
                <li><a href="#installation">Installation</a></li>
            </ul>
        </li>
        <li><a href="#usage">Usage</a></li>
        <li><a href="#license">License</a></li>
    </ol>
</details>
<br>

## About The Project

This is a little project made for fun and in order to practice with python and some concepts relative to the SAT problem.

### Built With

This project is built using:
* [PyQt5](https://pypi.org/project/PyQt5/)
* [PySAT](https://pypi.org/project/python-sat/)


<br>

## Getting Started

The code of this project is compatible with Linux, MacOS and Windows.

### Prerequisites

To be able to use this project you need python3 installed.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/gabrielepongelli/PySudoku.git && cd PySudoku
   ```
2. Create a python virtual environment
   ```sh
   python3 -m venv env
   ```
3. Activate the virtual environment<br>
   On Windows:
   ```powershell
   PS env\Scripts\Activate.ps1
   ```
   On MacOS/Linux:
   ```sh
   source env/bin/activate
   ```
4. Install the project requirements
   ```sh
   python3 -m pip install -r requirements.txt
   ```


<br>

## Usage

After completing the [installation procedure](#installation) in order to start the game just execute:
```sh
python3 main.py
```


<br>

## License

PySudoku is licensed under [GPL-3.0 License](LICENSE).