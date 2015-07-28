# Backup Services

Set of python scripts to backup various online services and from my 
mobile phone. 

## How does it work?

You'll need python 3, click, paramiko and requests. To get these, the easiest
way is to run

``` sh
pip install -r requirements.txt
```

Then just run it with the list of services to backup as arguments or no
arguments to back them all up.

## Usage

``` shell
Usage: backup.py [OPTIONS] SERVICES

Options:
  --help                  Show this message and exit.
```
