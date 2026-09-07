# Tehran Network Analysis

A Jupyter Notebook project for analyzing Tehran's road network and geographic accessibility using OpenStreetMap data.

## Project Overview

This project has two main parts:

### 1. Interactive Route Finder

An interactive map of Tehran lets the user select two points and displays the shortest driving route between them.

The implementation uses:

- OpenStreetMap road-network data
- Pyrosm for loading Tehran map data
- OSMnx for nearest-node calculations
- NetworkX for graph operations and shortest paths
- ipyleaflet for the interactive map

### 2. University Influence Area Analysis

The notebook also studies the accessibility/influence area of universities in Tehran.

It:

- Loads Tehran's driving road network
- Extracts universities and buildings
- Finds nearest road-network nodes
- Uses nearest-neighbor calculations with BallTree
- Calculates shortest-path distances
- Connects buildings to the road network
- Visualizes accessibility using a heatmap

## Requirements

- Python 3
- Jupyter Notebook or JupyterLab

Install the Python dependencies with:

```bash
pip install -r requirements.txt
```

## How to Run

Open a terminal in this folder and install the requirements:

```bash
pip install -r requirements.txt
```

Then start Jupyter:

```bash
jupyter notebook
```

Open:

```text
tehran_network.ipynb
```

and run the cells in order.

You can also use JupyterLab:

```bash
jupyter lab
```

## Main Libraries

- `pyrosm`
- `ipyleaflet`
- `networkx`
- `osmnx`
- `geopandas`
- `pandas`
- `scikit-learn`
- `numpy`
- `matplotlib`

## Data

The notebook loads Tehran OpenStreetMap data using `pyrosm.get_data()`.

An internet connection may be needed the first time the dataset or required map resources are downloaded.

## Project Structure

```text
05-tehran-network/
├── tehran_network.ipynb
├── requirements.txt
└── README.md
```

## About

This project was created as part of an Advanced Programming course.
It demonstrates graph analysis, shortest-path algorithms, geospatial data processing, interactive mapping, nearest-neighbor search, and data visualization in Python.
