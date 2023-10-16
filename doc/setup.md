# Project Setup

To initially set everything up you’re going to need the following:

- Python 3.11
- [Pipenv][1]

Once you’ve got those two, create a new Python virtual environment with `pipenv`
by running `pipenv shell` — and once that’s done — install the required
libraries with `pipenv install --dev`.

You should now be able to run the development environment with `python3
src/app.py` so long as you’ve got the virtual environment active.  You can enter
the virtual environment with `pipenv shell`.

When running the development environment, it’s recommended to pass the `-d` flag
to enable debug mode.  This will cause the environment to automatically update
whenever you make changes to a file.

## Example

    $ pipenv shell
    $ pipenv install --dev
    $ python src/app.py -d


[1]: https://pypi.org/project/pipenv/
