This project runs on Python and depends on the Tornado and CairoSVG packages. The frontend is written in vanilla HTML and JavaScript.

The Python dependencies are managed by Pipenv; to prepare the environment, install Pipenv and Python 3.9 and run `pipenv install` in the root directory of the project. Then, execute `pipenv run python server.py` to start the server application, or substitute in the other Python files to run their minimal built-in tests.

This program attempts to render PNGs using the font Liberation Sans. If it is not installed on your system, CairoSVG will presumably fall back on some weird default, so watch out for that.
