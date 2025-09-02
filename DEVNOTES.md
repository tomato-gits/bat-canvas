# Development notes

Initial goal is to set up a project that:
* provides CLI as main interface
* stores credentials for multiple instances of Canvas
* runs scripts to collect information from single instance (generate reports)
* runs scripts to compare results from multiple instances (validate schemas)
* maintains 100% coverage in unit tests

## project structure
* bat-canvas is top-level project
* pyproject.toml lists dependencies and other project installation md
  * scripts folder (temporary) is for reference during development, has example scripts to convert into automations
  * the bat/ module is the source file that contains all the python source for the installable module 
    * bat/tests submodule contains tests for stuff in bat 
  * tests folder contains unit tests for the bat-canvas project

## running tests
unit tests located in bat-canvas/bat/tests/ and submodules `pytest bat`

integration tests in bat-canvas/tests/integration/ 

end-to-end tests in bat-canvas/tests/e2e/ `pytest tests`

## project setup steps
### initial project setup
created basic project structure based on bat-template and batconf
* bat module copied relevant parts from bat-template to get basic configuration management, cli/argparser, and logging 
functionality and library with "hello_world" function, and associated unit tests
* created entrypoint to bat cli interface by defining it in pyproject.toml as bat = 'bat.cli:BATCLI' 
  * installing project `pip install -e .` provides bat-canvas environment with CLI access to commands defined in bat/cli.py, ex: `bat hello`

creating first project command 'check_assignment'
bat/tests/cli_test tests command, adds to commands list, uses mocks for print and hello world for unit test  
tests/cli_test executes check_assignment for e2e test

check_assignment is defined as command, when run as bat check_assignment returns the args
bat check_assignment --help returns a generic help string


I want to be able to: 
- pass in the course id and assignment id
- optionally pass in the instance? or have a default?
- get the instance url and api key from somewhere (file?)
- make the api call using canvasapi (need to install that, list as requirement)
- check return from api call, distinguish  between "no resource" and real data

For future: set up test course/assignments/etc in instances, make file that has course id, assignment id, etc
for various cases (published, assignment type etc) and them import those into test functions, instead of hard-coding 
id's in the test cases. 
Also create a wrapper for task functions that first calls get_config (maybe can take arg for instance, like 'prod' or 
'test'?) and then calls the task function (check_assignments_cfg and check_assignments)
The config will have the Canvas instance URL and the access token. Do we want to maintain the ability to pass in the 
token as a CLI arg?
Also replace requests with the canvasapi library