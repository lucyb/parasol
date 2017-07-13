# Parasol: Keeping you safe when the Cloud(TM) goes away.

Parasol is a python program to backup data from various on-line services, 
e.g Trello, Pinboard, Flickr and Tiny Tiny RSS. And, while not strictly an on-line service, it can also copy data, such as photos, from a mobile phone. 

It has been created with extensibility in mind, so additional on-line services are easy to add. See the [contributor guide](./CONTRIBUTING.md) for more information.

## Installation

Parasol is written in python 3. It can be installed using setuptools, by doing the following:

``` python
python setup.py install
```

This will also install the dependencies, which are stored in requirements.txt.

It can also be run without installing by:

``` python
python parasol.py
```

Once it's installed, just run 'parasol' with the list of services to backup as arguments or with no arguments to back them all up. You'll need to configure these services first though - see the configuration section below to find out how.

### Usage

``` shell
Usage: parasol [OPTIONS] [SERVICES]...

Options: 
--list         List services we know how to back up
--config PATH  Specify location of the config file  [default:     	  
               $HOME/.config/parasol/config.ini]
-v, --verbose  Verbose logging. Can be specified multiple times to    
               increase verbosity
-q, --quiet    Quiet logging. Reduce logging output to critical errors 
               only.
               Will be ignored if -v is specified
--help         Show this message and exit.
```

## Configuration
Some set up work needs to be done before using parasol for the first time. This is done by creating a config file, called 'config.ini'. There is an example configuration in example-config and you should use this as a template. It also contains some instructions for how to set up the different services.

Each service that is going to be backed-up needs an entry in the config file. If you have several accounts for one service, then specify each in its own section (i.e a service can be specified more than once), but be sure to give the sections unique names (e.g [Trello-Home] and [Trello-Work]).

The location of the config file can be specified using the --config option (see the output of --help for the default location).