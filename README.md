# Anagram finder:

### Dependencies:
* python3 (Tested with python3.6 and python3.8)
* make (Optional)

### Directions: 
From the project root:
* Run `make` to get a list of shortcut commands.
* Run directly: `./anagram_parser/anagram_parser.py {file path}`
* Or alternatively explicitly use system python or a virtual environment: `python3 anagram_parser/anagram_parser.py {file path}`

### Considerations:
* I've attempted to not use any third parties libraries.
* I've assumed that potentially end-users would directly use the program.
* I've used [bandit](https://github.com/PyCQA/bandit) for security checks and [black](https://black.readthedocs.io/en/stable/) for formatting.

### Ideas for improvement:
* Turning the program into a package by adding a `setup.py`
* Add an entry point for the script: https://stackoverflow.com/questions/774824/explain-python-entry-points
* Containerise use Docker/Docker-compose.
* Use fancier third-party libraries such as: [pytest](https://docs.pytest.org/en/stable/), [click](https://click.palletsprojects.com/en/7.x/)
