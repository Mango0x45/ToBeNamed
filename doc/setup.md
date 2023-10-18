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

When running the development environment, it’s recommended to pass the `-d` or
`--debug` flags to enable debug mode.  This will cause the environment to
automatically update whenever you make changes to a file.  You can also pass an
extra hostname parameter if you would like to use a hostname that isn’t the
default ‘localhost’.  By default the server runs on port 5000, but this too can
be customized through the `-p` or `--port` flags.

## Example

Getting dependencies:

    $ pipenv shell
    $ pipenv install --dev

Different ways to run the server:

    $ python src/app.py -d
    $ python src/app.py --debug
    $ python src/app.py 127.0.0.1
    $ python src/app.py -d 127.0.0.1
    $ python src/app.py -d --port=1234

You can also just execute the server directly:

    $ src/app.py -d

[1]: https://pypi.org/project/pipenv/
