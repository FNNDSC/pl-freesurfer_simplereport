# FreeSurfer Simple Reporting

[![Version](https://img.shields.io/docker/v/fnndsc/pl-freesurfer_simplereport?sort=semver)](https://hub.docker.com/r/fnndsc/pl-freesurfer_simplereport)
[![MIT License](https://img.shields.io/github/license/fnndsc/pl-freesurfer_simplereport)](https://github.com/FNNDSC/pl-freesurfer_simplereport/blob/main/LICENSE)
[![ci](https://github.com/FNNDSC/pl-freesurfer_simplereport/actions/workflows/ci.yml/badge.svg)](https://github.com/FNNDSC/pl-freesurfer_simplereport/actions/workflows/ci.yml)

`pl-freesurfer_simplereport` is a [_ChRIS_](https://chrisproject.org/)
_ds_ plugin which takes in ...  as input files and
creates ... as output files.

## Abstract

...

## Installation

`pl-freesurfer_simplereport` is a _[ChRIS](https://chrisproject.org/) plugin_, meaning it can
run from either within _ChRIS_ or the command-line.

[![Get it from chrisstore.co](https://ipfs.babymri.org/ipfs/QmaQM9dUAYFjLVn3PpNTrpbKVavvSTxNLE5BocRCW1UoXG/light.png)](https://chrisstore.co/plugin/pl-freesurfer_simplereport)

## Local Usage

To get started with local command-line usage, use [Apptainer](https://apptainer.org/)
(a.k.a. Singularity) to run `pl-freesurfer_simplereport` as a container:

```shell
singularity exec docker://fnndsc/pl-freesurfer_simplereport freesurfer_simplereport [--args values...] input/ output/
```

To print its available options, run:

```shell
singularity exec docker://fnndsc/pl-freesurfer_simplereport freesurfer_simplereport --help
```

## Examples

`freesurfer_simplereport` requires two positional arguments: a directory containing
input data, and a directory where to create output data.
First, create the input directory and move input data into it.

```shell
mkdir incoming/ outgoing/
mv some.dat other.dat incoming/
singularity exec docker://fnndsc/pl-freesurfer_simplereport:latest freesurfer_simplereport [--args] incoming/ outgoing/
```

## Development

Instructions for developers.

### Building

Build a local container image:

```shell
docker build -t localhost/fnndsc/pl-freesurfer_simplereport .
```

### Get JSON Representation

Run [`chris_plugin_info`](https://github.com/FNNDSC/chris_plugin#usage)
to produce a JSON description of this plugin, which can be uploaded to a _ChRIS Store_.

```shell
docker run --rm localhost/fnndsc/pl-freesurfer_simplereport chris_plugin_info > chris_plugin_info.json
```

### Local Test Run

Mount the source code `freesurfer_simplereport.py` into a container to test changes without rebuild.

```shell
docker run --rm -it --userns=host -u $(id -u):$(id -g) \
    -v $PWD/freesurfer_simplereport.py:/usr/local/lib/python3.10/site-packages/freesurfer_simplereport.py:ro \
    -v $PWD/in:/incoming:ro -v $PWD/out:/outgoing:rw -w /outgoing \
    localhost/fnndsc/pl-freesurfer_simplereport freesurfer_simplereport /incoming /outgoing
```
