# The Euro Coins Website (To Be Named)

Note to self: Update this later with information for non-devs.


## For Developers


### Initial Project Setup

To initially set everything up, you’re going to need the following:

- A relatively modern version of Python

- [Pipenv][1]

Once you’ve got those two, create a new Python virtual environment with
`pipenv` by running `pipenv shell` — and once that’s done — install the required
libraries with `pipenv install --dev`.

You should now be able to run the development environment with `python3
src/app.py` so long as you’ve got the virtual environment active.  You can enter
the virtual environment with `pipenv shell`.


### Making a Contribution

Just some general rules for contributing:

- Start your commit messages with capital letter

- Run `make format` to format your code _before_ you commit

  - This will require you to either be on a UNIX-like system, or to use WSL.
    But if you’re on Windows you should be using WSL anyways.

- Do each new thing on a seperate branch

  - Making 5 unrelated changes on the same branch is just annoying to deal with.
    `git branch` is your best friend.


[1]: https://pypi.org/project/pipenv/
