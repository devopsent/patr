# patr


Stands for Pretty Awesome Template Renderer

## About

Helps operator to create a file from template with validation.
It consumes information from user provided the template, the data and possibly validation rules.

## What it does

Based on user provided input map generates ansible inventory for further use of various processes

The inventory is undergoing basic validation written inside `validation_rules.yml` searched for in the folder the script is running in
Validation rules can be extended/changed


## Installation


Run in virtualenv:

    pip install <patr package>


# Usage

## Prerequisites:


require pip to install, pulls its other dependencies by itself

## Normally:

Run:

    patr

Please refer to ``--help``, which shows default locations it's looking for the yaml files.


# Known issues


no known issues

# Contributing


Patches/pull/feature requests are welcome to improve the code/fix bugs.
Note I'm quite a busy person, so if you can fix/add it - send me a patch/pull-request.


[SeaHorse](https://wiki.gnome.org/Apps/Seahorse)

# Author

Max Kovgan <maxk@devopsent.biz>
