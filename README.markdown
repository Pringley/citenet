# CiteNet

CiteNet contains Python implementations of several citation network algorithms
for use with [NetworkX](http://networkx.github.io) graphs.

## Installation

To install (including all dependencies), simply run:

    python setup.py install

## Configuration

Create a configuration file using JSON, e.g.:

```javascript
{
    "graph": {
        "filename": "PATH/TO/GRAPH.csv"
    },
    "metadata": [
        {
            "filename": "PATH/TO/METADATA1.csv",
            "id_field": "node"
        },
        {
            "filename": "PATH/TO/METADATA2.csv",
            "id_field": "node"
        }
    ],
    "reports": {
        "function": "metadata_histogram",
        "output": "PATH/TO/OUTPUT.csv",
        "options": {
            "field": "author"
        }
    }
    "options": {}
}
```

## Usage

Generate reports with:

    citenet reports config.json

Spin up an interactive Python shell using:

    citenet interact config.json
