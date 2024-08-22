# Development notes

Initial goal is to set up a project that:
* provides CLI as main interface
* stores credentials for multiple instances of Canvas
* runs scripts to collect information from single instance (generate reports)
* runs scripts to compare results from multiple instances (validate schemas)
* maintains 100% coverage in unit tests

## project structure
* bat-canvas is top-level project
* pyproject.toml lists dependencies and other project md
  * scripts folder (temporary) is for reference during development, has example scripts to convert into automations
  * the bat/ module is the source file that contains all the python source for the installable module 
    * bat/tests submodule contains tests for stuff in bat 
  * tests folder contains unit tests for the bat-canvas project

## running tests
unit tests located in /tests `pytest tests`

## project setup steps
### initial project setup
created basic project structure based on bat-template and batconf
* bat module copied relevant parts from bat-template to get basic configuration management, cli/argparser, and logging 
functionality and library with "hello_world" function, and associated unit tests
* created entrypoint to bat cli interface by defining it in pyproject.toml as bat = 'bat.cli:BATCLI' 
  * installing project `pip install -e .` provides bat-canvas environment with CLI access to commands defined in bat/cli.py, ex: `bat hello`



