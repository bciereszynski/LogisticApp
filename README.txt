# Transport Optimization Application – Profit Maximization

This project is an application designed to support transportation companies by solving an **optimization problem focused on maximizing profit**. It was developed as part of an engineering thesis at Bialystok University of Technology.

The system generates optimal delivery routes for multiple drivers while considering **route length constraints** and **real road networks**. It uses a **heuristic algorithm based on local search operators** to provide near-optimal solutions efficiently.

---

## Features

- **Heuristic optimization algorithm**:
  - Greedy construction of initial routes
  - Local search operators:
    - **2-opt** (route improvement by segment reversal)
    - **Insert** (adding profitable points)
    - **Replace** (swapping points to improve profit)
    - **Disrupt** (perturbation to escape local optima)
  - Adjustable parameters (iterations, operators, disruption level)
- **Real map visualization** using OpenStreetMap and Folium
- **Route length constraints** (per driver)
- **Interactive GUI** built with PyQt
- **Relational database** (MariaDB + SQLAlchemy + Alembic migrations)
- **External APIs** (TrueWay Matrix & Directions) for real road distances and route plotting
- **Automated email dispatch** of routes to drivers (interactive map attachments)
- **Import/export of points** from files
- **Configurable algorithm parameters** through the UI

---

## Technologies Used

- **Python 3**
- **PyQt** (GUI)
- **Folium** (interactive maps)
- **OpenStreetMap** (geographical data)
- **TrueWay Matrix & Directions API** (road network distances and routes)
- **MariaDB** (database)
- **SQLAlchemy + Alembic** (ORM and migrations)
- **SMTP + MIME** (email sending)

---

## Installation

### Requirements
- Python 3.10+
- MariaDB server
- API keys for TrueWay Matrix and Directions

### Install dependencies:
```bash
pip install -r requirements.txt
```

### Database Setup

1. Configure MariaDB and create a database.
2. Apply migrations:
```bash
alembic upgrade head
```

## Configuration

On first run, the app will prompt for:
- Database connection details  
- API keys

## Algorithm Overview

The problem is modeled as a Team Orienteering Problem (TOP):
- Maximize total profit from visited points
- Each route has a maximum allowed length
- Drivers start and end at the same depot
- Routes are computed using local search heuristics to provide high-quality solutions in acceptable time.

Author
Bartosz Piotr Ciereszyński
Engineering Thesis – Bialystok University of Technology (2024)
