# Placeholders

A command-line tool to set and get variables embedded in image metadata

## Getting Started

To get started clone this repo, and if you don't want to install all the dependencies globally (and you shouldn't want to), make sure you have something like Virtualenv installed on your machine.

### Prerequisites

To avoid potential conflicts, create a virtual environment and activate it before following installation instructions.

```
virtualenv -p python3 env
. env/bin/activate
```

### Installing

Follow these steps to setup Placeholders.

```
pip install placeholders
```

### Basic Controls

Get variable embedded in image

```
placeholders image.py
```

Get variables for each image in a directory

```
placeholders ./example_directory
```

Set variable in image

```
placeholders test.jpg --tag variable_name
```

Set image variables according to yaml

```
placeholders tags.yaml
```

### Example yaml

```
/absolute/path/image.png test
/absolute/test.jpg test2
```

## Authors

- Austin Brown
