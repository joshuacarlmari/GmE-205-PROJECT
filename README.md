# Python-Based Spatial Land Administration Tool for Easement Analysis Along Transmission Lines
## Description
### This project is a Python-based geospatial application developed to automate the analysis of transmission line easements and assess their impact on nearby land parcels. The system uses object-oriented programming principles and spatial analysis techniques to identify affected parcels, calculate overlap areas and distances from transmission lines, detect building presence, and classify parcels according to risk levels.

### The application processes parcel, transmission line, and building datasets in GeoJSON format and generates multiple outputs, including CSV reports, JSON reports, and risk maps. The system is designed to support land administration, easement monitoring, infrastructure planning, and decision-making by providing an efficient alternative to manual GIS-based workflows.

## Key Features
### Automated transmission line easement analysis
### Parcel overlap and proximity assessment
### Building detection within affected parcels
### Risk classification (High Risk and Moderate Risk)
### CSV and JSON report generation
### Automated risk map visualization
### Object-oriented design using encapsulation, inheritance, abstraction, and polymorphism

## Technologies Used
### Python
### Shapely
### GeoPandas
### Matplotlib
### Contextily
### GeoJSON

## Study Area

### The project is demonstrated using parcel and transmission line data from Barangay Poblacion and Barangay New Agutaya in the Municipality of San Vicente, Palawan, Philippines, where a proposed transmission line corridor is planned.

## Project Structure
### spatial.py – Spatial object classes and geometry operations
### admin_units.py – Administrative hierarchy classes
### analysis.py – Easement analysis and risk assessment
### report.py – Report generation and map visualization
### main_project.py – Main application workflow
### demo.py – Demonstration

## Methodology
### System Logic
#### The system reads parcel, building, and transmission line datasets from GeoJSON files.
#### Geometries are validated and converted into spatial objects for analysis.
#### Each parcel is linked to its administrative location (Province, Municipality, Barangay).
#### Transmission lines are buffered to create easement corridors.
#### The system evaluates each parcel against the easement corridor and computes overlap area, distance, and building presence.

### Computational Approach
#### Buffer analysis is used to generate transmission line easement zones.
#### Intersection analysis identifies parcels overlapping the corridor.
#### Distance analysis determines parcel proximity to transmission lines.
#### Rule-based classification is applied to assign risk levels:
##### High Risk: overlap or within 30 m
##### Moderate Risk: within 30–100 m
##### Low Risk: beyond 100 m
### Object-Oriented Design
#### SpatialObject serves as the parent class for spatial entities.
#### Parcel and TransmissionLineEasement inherit common spatial operations.
#### Administrative units are modeled using Province, Municipality, and Barangay classes.
#### Analysis and reporting are separated into dedicated modules to improve maintainability and scalability.
### Problem-Solving Strategy
#### Automated repetitive GIS tasks that would otherwise require manual inspection.
#### Organized spatial data using hierarchical administrative units.
#### Applied modular OOP design to simplify future system expansion and maintenance.

## Results and Discussion
### System Functionality
#### Successfully loaded and processed parcel, building, and transmission line datasets.
#### Automatically identified parcels affected by transmission line easements.
#### Computed overlap area, distance from transmission lines, and building presence.
#### Generated CSV reports, JSON reports, and risk maps.

## Key Results
### 177 parcels were identified within or overlapping the transmission line easement corridor.
### 351 parcels were classified as High Risk.
### 207 parcels were classified as Moderate Risk.

## Performance Insights
### Automated spatial analysis significantly reduced manual GIS processing.
### Object-oriented design improved code organization and reusability.
### Modular implementation enabled efficient integration of analysis, reporting, and visualization components.

## Demonstration of Computational Thinking
### Decomposed the problem into data loading, spatial modeling, analysis, classification, and reporting.
### Used algorithmic workflows to evaluate parcel-easement relationships.
### Applied object-oriented principles to represent real-world entities and manage system complexity.

