# Project Structure

The structure of the project looks a little bit like this:

    .
    ├── doc
    └── src
        ├── blueprints
        ├── data
        ├── scripts
        ├── static
        ├── templates
        ├── translations
        └── xtypes

## `doc/`

This directory contains all of the documentation, regardless of if it’s intended
for users, developers, or anyone else.  This document is current in this same
directory


## `src/`

Anything that isn’t a tool configuration or documentation is included in this
directory.


### `src/blueprints/`

All our blueprints go here.  Blueprints handle the routing of different sections
of the site.  All pages under `domain.com/coins` are routed by the `coins`
blueprint, for example.


### `src/data/`

All the data files that we need are stored here.  That includes stuff like
mintage figures for various coins.


### `src/scripts/`

This directory contains random scripts that might be helpful.  `rm-bg` for
example can be found here, and acts as a user-friendly wrapper around `convert`
to turn JPEG files into transparent PNGs.


### `src/static/`

Here you can find all the static files.  Things like CSS stylesheets, images,
and fonts will be located under this directory.


### `src/templates/`

All the Jinja/HTML files can be found here.  The folder structure under this
directory should be pretty self-explanitory, and follows the same structure as
the website itself.


### `src/translations/`

All the translation files can be found here.  Each locale has it’s own
subdirectory containing an `LC_MESSAGES/` directory.  It seems rather redundant,
but as far as I’m aware we just have to do it that way.


### `src/xtypes/`

This directory contains all the different types and classes we define.  Things
like the `Denomination` and `CaseInsensitiveString` types.  Preferably this
would be called `src/types/`, but `types` is a pretty heavily-conflicting word
so `xtypes` it is.
