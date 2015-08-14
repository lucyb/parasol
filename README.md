# Parasol: Keeping you safe when The Cloud(TM) goes away.

A set of python scripts to backup various online services, and data from a mobile phone. 

## How does it work?

You'll need python 3.  You will also need the click, paramiko and requests
libraries. To get these, the easiest way is to run

``` sh
pip install -r requirements.txt
```

Then just run it with the list of services to backup as arguments or no
arguments to back them all up.

## Usage

``` shell
Usage: parasol.py [OPTIONS] SERVICES

Options:
  --list                 List services we know how to back up
  --config TEXT          Specify location of the config file
  -v                     Verbose logging. Can be specified multiple times to increase
                         verbosity
  --help                 Show this message and exit.
```