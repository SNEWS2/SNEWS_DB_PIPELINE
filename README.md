# SNEWS Database Listener (and writer)
Listens to SNEWS detector messages and writes to Postgres database

This packages provides a Python API and CLI to **write observation messages** to the persistent SNEWS Postgres Database. The main components of the package are one, a docker setup for a Postgre database, and two, a function that listens to a Kafka pipeline for snews messages and then writes those messages to the Postgre database. The code for the Kafka pipeline listener can be found in snews_db/kafka_listener.py.

> Note: Make sure your hop credentials are set up !!<br>
> Follow the instructions in the [**Publishing Tools Quick Start**](https://snews-publishing-tools.readthedocs.io/en/latest/user/quickstart.html)


|                                                                                                                                                                                                                                                                                                                                                                                             |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| 
| **Fire-Drills**                                                                                                                                                                                                                                                                                                                                                                             |
| Also see [this page](https://snews-publishing-tools.readthedocs.io/en/latest/user/firedrills.html)                                                                                                                                                                                                                                                                                          |                                                                                                                                                                                                                                                                                                                                                                                            |                                                                                                                                                                                                                                                                                                                                                                                            |
| `snews_db` allows for fire-drill mode, currently this is the default option. <br/><br/> Later, it can be adjusted through `firedrill_mode=True/False` arguments in listener functions, and through `--firedrill/--no-firedrill` flags within the CLI tools. <br/>Make sure you have the correct [permissions](https://my.hop.scimma.org/hopauth/) to subscribe to these firedrill channels. The snews_db CLI is explained in more detail in the CLI section below. |

## How to Install

### [Installation Guide for SNEWs](https://snews-publishing-tools.readthedocs.io/en/latest/user/installation.html)

### SNEWS_DB specific installation guidelines
1) Install docker desktop if not already.
2) Run `poetry lock` followed by `poetry install` to install all relevant packages.
3) Make sure in the `pyproject.toml` file that any snews dependency packages are installed in developer/editable mode. For instance, if you are also developing snews publisher tools, you want to make sure that you have 
`snews-pt = { path = "../SNEWS_Publishing_Tools", develop = true }` (note this path assumes you have the SNEWS_Publishing_Tools repo one level above your SNEWS_DB_PIPELINE repo).
4) Modify `test-config.env` in `snews_db/tests/etc` with the Postgre configurations parameters you want to use. 
5) Run `bash start_containers.sh` to start the docker container with the Postgre SQL database. 


## How to Publish and Subscribe

### [Publishing Guide](https://snews-publishing-tools.readthedocs.io/en/latest/user/publishing_protocols.html)
### [Subscribe Guide](https://snews-publishing-tools.readthedocs.io/en/latest/user/subscribing.html)


## Command Line Interface (CLI)
There also exists tools for command line interactions. These are explained in detail here;
### [CLI Tools](https://snews-publishing-tools.readthedocs.io/en/latest/user/command_line_interface.html)

SNEWS_DB also supports various tools via a CLI. For instance, to run the Kafka pipeline listener, run the following command
`snews_db listen-to-detectors [--firedrill/--no-firedrill]`.

## Testing
To run all test cases, simply run `pytest` from the root directory of the repo. 
