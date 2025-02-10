# Analysistool-heterogeneous-vehicle-trajectory-data-sets

## Overview
This tool is designed to analyze heterogeneous vehicle trajectory datasets from different sources. It provides functionalities for filtering and selecting data on a map, followed by various scripts for in-depth analysis. The key principles behind the tool are:
- **Modular Design**: Components are designed to be reusable and interchangeable.
- **Object-Oriented (OO) Approach**: The tool follows OO principles to ensure maintainability and clarity.
- **Easy Extendability**: Developers can seamlessly add new features and analysis scripts.

## Features
- Import and process trajectory data from multiple heterogeneous sources.
- Visualize traffic data on a map for filtering and selection.
- Perform spatial and statistical analysis using various scripts.
- Store and query data efficiently using a PostgreSQL database with PostGIS support.
- Modular and extendable architecture for custom analysis and data handling.

## Installation & Execution

### Prerequisites
Ensure you have the following installed:
- **Docker** (for PostgreSQL with PostGIS)
- **Python** (ensure dependencies are installed)
- **PostgreSQL with PostGIS** (for database storage and querying)

### Setup Instructions
1. **Build JSON Files**:
   - Navigate to the `src` folder.
   - Execute the build script to generate necessary JSON files in `src/dictionary/`.

2. **Database Setup**:
   - Install and run the Docker container for PostgreSQL with PostGIS:
     ```sh
     docker pull lauraxrb/pseanalysistool
     docker run -d --name traffic-db -p 5432:5432 lauraxrb/pseanalysistool
     ```
   - If you want to use a custom database, configure it as follows:
     - The application connects via a user called `analysisUser`.
     - Set the password for `analysisUser` to `1234`.
     - The database name should be `Analysistool`.
     - Adjust these settings in `src/dictionary/sql_connection.json` if needed.
     - Ensure that PostGIS is enabled for spatial queries.

3. **Install Dependencies**:
   - If not installed automatically, install dependencies manually:
     ```sh
     pip install -r requirements.txt
     ```

4. **Start the Application**:
   - Run the main method in the `Application` class:
     ```sh
     python src/main.py
     ```

5. **Import & Open Datasets**:
   - Import datasets before usage.
   - When using HighD data, ensure you select three datasets together.

## Data Representation
- Traffic data is represented as **trajectories**, capturing movement patterns.
- The tool allows **filtering and selection** of trajectories on a map for targeted analysis.

## Modular Architecture
This tool is built with modularity and extendability in mind:
- **Data Handling**: Easily add new data formats.
- **Filtering Methods**: Extend the filtering functionalities by adding new spatial or attribute-based filters.
- **Analysis Scripts**: New analysis scripts can be incorporated with minimal changes to the existing codebase.
- **Database Management**: Flexible database connection settings enable easy migration to other database solutions if needed.

## Future Enhancements
- Support for real-time data streaming.
- Integration with additional GIS tools.
- Advanced machine learning-based trajectory prediction.
