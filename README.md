# SNEWS Database Listener (and writer)
Listens to SNEWS detector messages and writes to Postgres database

This packages provides a Python API and CLI to **write observation messages** to the persistent SNEWS Postgres Database.

> Note: Make sure your hop credentials are set up !!<br>
> Follow the instructions in the [**Publishing Tools Quick Start**](https://snews-publishing-tools.readthedocs.io/en/latest/user/quickstart.html)


|                                                                                                                                                                                                                                                                                                                                                                                             |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| 
| **Fire-Drills**                                                                                                                                                                                                                                                                                                                                                                             |
| Also see [this page](https://snews-publishing-tools.readthedocs.io/en/latest/user/firedrills.html)                                                                                                                                                                                                                                                                                          |                                                                                                                                                                                                                                                                                                                                                                                            |                                                                                                                                                                                                                                                                                                                                                                                            |
| `snews_db` allows for fire-drill mode, currently this is the default option. <br/><br/> Later, it can be adjusted through `firedrill_mode=True/False` arguments in listener functions, and through `--firedrill/--no-firedrill` flags within the CLI tools. <br/>Make sure you have the correct [permissions](https://my.hop.scimma.org/hopauth/) to subscribe to these firedrill channels. |

## How to Install

### [Installation Guide](https://snews-publishing-tools.readthedocs.io/en/latest/user/installation.html)

## How to Publish and Subscribe

### [Publishing Guide](https://snews-publishing-tools.readthedocs.io/en/latest/user/publishing_protocols.html)
### [Subscribe Guide](https://snews-publishing-tools.readthedocs.io/en/latest/user/subscribing.html)


## Command Line Interface (CLI)
There also exists tools for command line interactions. These are explained in detail here;
### [CLI Tools](https://snews-publishing-tools.readthedocs.io/en/latest/user/command_line_interface.html)
