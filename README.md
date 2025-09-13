<p align="center">
  <img width="100" height="100" alt="image" src="https://github.com/user-attachments/assets/1bd037dc-2513-4d4c-9664-c4f38028064a" />
</p>

# Screener-Vector : Daily-Stock-Screener-Ranking-Pipeline

**A comprehensive ETL (Extract, Transform, Load) data processing pipeline built with Python, Docker, and Concourse CI/CD integration.**

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Running with Docker](#running-with-docker)
  - [Running Individual Components](#running-individual-components)
- [Pipeline Configuration](#pipeline-configuration)
- [Data Processing Modules](#data-processing-modules)
- [CI/CD Integration](#cicd-integration)
- [Monitoring and Logging](#monitoring-and-logging)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Changelog](#changelog)

---

## Project Overview

This project implements a scalable, containerized ETL data pipeline designed to extract, transform, and load data from Screener.in. The pipeline is built with modern data engineering best practices, featuring Docker containerization, automated CI/CD workflows, and comprehensive data processing capabilities.

### Purpose

The ETL pipeline serves to:
- **Extract** data from multiple heterogeneous sources
- **Transform** raw data into clean, structured formats
- **Load** processed data into target storage systems
- **Monitor** data quality and pipeline performance
- **Automate** deployment and scaling processes

### Key Benefits

- **Scalability**: Containerized architecture supports horizontal scaling
- **Reliability**: Built-in error handling and retry mechanisms
- **Maintainability**: Modular design with clear separation of concerns
- **Observability**: Comprehensive logging and monitoring capabilities
- **Automation**: Complete CI/CD integration with Concourse

---

### Technology Stack

- **Language**: Python 3.8+
- **Containerization**: Docker & Docker Compose
- **CI/CD**: Concourse CI
- **Data Processing**: Pandas, NumPy
- **Configuration**: YAML-based configuration files
- **Monitoring**: Built-in logging and metrics collection

---

## Features

### Core ETL Capabilities
- ✅ Multi-source data extraction
- ✅ Configurable data transformations
- ✅ Batch and streaming processing support
- ✅ Data validation and quality checks
- ✅ Error handling and recovery
- ✅ Incremental data loading

### Operations & DevOps
- ✅ Docker containerization
- ✅ Docker Compose orchestration
- ✅ Concourse CI/CD pipelines
- ✅ Environment-specific configurations
- ✅ Health monitoring and alerting
- ✅ Automated testing and deployment

### Data Processing Features
- ✅ Column selection and filtering
- ✅ Data type conversion and validation
- ✅ Table extraction and parsing
- ✅ File format conversion
- ✅ Data quality assessment
- ✅ Automated data profiling

---

## Prerequisites

Before running this project, ensure you have the following installed:

### Required Software
- **Docker**: Version 20.10+ ([Install Docker](https://docs.docker.com/get-docker/))
- **Docker Compose**: Version 2.0+ ([Install Docker Compose](https://docs.docker.com/compose/install/))
- **Python**: Version 3.8+ (for local development)
- **Git**: Latest version for version control

### System Requirements
- **Memory**: Minimum 4GB RAM (8GB+ recommended)
- **Storage**: 10GB+ available disk space
- **CPU**: Multi-core processor recommended for optimal performance
- **Network**: Internet connection for downloading dependencies

### Optional Tools
- **Make**: For using provided Makefile commands
- **Concourse CLI (fly)**: For CI/CD pipeline management
- **Python virtual environment**: For isolated development

---

## Installation

### Quick Start

1. **Clone the repository:**
```bash
git clone <repository-url>
cd <repository-name>
```

2. **Set up environment variables:**
```bash
cp credentials.yml.template credentials.yml
# Edit credentials.yml with your specific configuration
```

3. **Build and start the pipeline:**
```bash
docker-compose up -d --build
```

4. **Verify installation:**
```bash
docker-compose ps
docker-compose logs
```

### Development Setup

1. **Create Python virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Install pre-commit hooks (optional):**
```bash
pre-commit install
```

---

## Configuration

### Environment Configuration

The pipeline uses YAML-based configuration files:

#### `credentials.yml`
Contains sensitive configuration data:
```yaml
database:
  host: "your-database-host"
  port: 5432
  username: "your-username"
  password: "your-password"

api_keys:
  external_service: "your-api-key"

storage:
  bucket_name: "your-s3-bucket"
  access_key: "your-access-key"
```

#### `docker-compose.yml`
Defines the containerized services and their configurations:
- Service definitions
- Environment variables
- Volume mappings
- Network configurations
- Port mappings

### Pipeline Configuration

#### `All pipelines.yml`
Main pipeline configuration defining:
- Data source connections
- Transformation rules
- Loading destinations
- Scheduling parameters
- Monitoring settings

---

## Usage

### Running with Docker

#### Start All Services
```bash
# Start all services in the background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

#### Individual Service Management
```bash
# Start specific service
docker-compose up service-name

# Restart a service
docker-compose restart service-name

# Scale a service
docker-compose up -d --scale worker=3
```

### Running Individual Components

#### ETL Processing
```bash
# Run main ETL pipeline
python ETL.py

# Run specific ETL component
python ETL_Input.py
python ETL2.pyth
```

#### Data Processing Utilities
```bash
# Extract and convert tables
python table_extractor.py

# Select specific columns
python select_columns.py

# Convert data formats
python converter.py

# Process with file watching
python click_watchdog.py
```

#### Configuration and Setup
```bash
# Run configuration setup
python config.py

# Execute login procedures
python login.py

# Run all processing steps
bash run_all.sh
```

---

## Pipeline Configuration

### Data Source Configuration

Configure data sources in your pipeline YAML files:

```yaml
sources:
  - name: "primary_database"
    type: "postgresql"
    connection:
      host: "${DB_HOST}"
      port: 5432
      database: "production"
    
  - name: "api_source"
    type: "rest_api"
    endpoint: "https://api.example.com/data"
    auth_type: "bearer_token"
```

### Transformation Configuration

Define transformation steps:

```yaml
transformations:
  - name: "data_cleaning"
    operations:
      - remove_duplicates: true
      - handle_nulls: "drop"
      - standardize_columns: true
      
  - name: "data_enrichment"
    operations:
      - join_lookup_tables: true
      - calculate_derived_fields: true
```

### Loading Configuration

Specify target destinations:

```yaml
destinations:
  - name: "data_warehouse"
    type: "postgresql"
    mode: "append"
    batch_size: 1000
    
  - name: "analytics_storage"
    type: "s3"
    bucket: "analytics-data"
    format: "parquet"
```

---

## Data Processing Modules

### Core ETL Components

#### `Main.py`
Main ETL orchestration module:
- Coordinates extraction, transformation, and loading
- Manages pipeline execution flow
- Handles error propagation and recovery

### Utility Modules

#### `table_extractor.py`
Specialized table extraction:
- PDF table extraction
- HTML table parsing
- Structured data extraction

#### `select_columns.py`
Column selection and filtering:
- Dynamic column selection
- Schema evolution handling
- Data type validation

#### `converter.py`
Data format conversion:
- Cross-format data conversion
- Encoding handling
- Compression support

#### `click_watchdog.py`
File system monitoring:
- Real-time file watching
- Automatic processing triggers
- Event-driven ETL execution

#### `common_methods.csv`
Shared utility functions:
- Common data processing operations
- Reusable transformation logic
- Standard validation functions

---

## CI/CD Integration

### Concourse CI Pipeline

The project includes comprehensive CI/CD pipeline configuration:

#### Pipeline Features
- **Automated Testing**: Unit tests, integration tests, and data validation
- **Code Quality**: Linting, formatting, and security scanning
- **Build Process**: Docker image building and artifact creation
- **Deployment**: Automated deployment to staging and production
- **Monitoring**: Pipeline health monitoring and alerting

#### Setting Up Concourse

1. **Install Concourse CLI:**
```bash
# Download and install fly CLI
curl -L -o fly "https://github.com/concourse/concourse/releases/download/v7.8.0/fly-7.8.0-linux-amd64.tgz"
chmod +x fly
sudo mv fly /usr/local/bin/
```

2. **Login to Concourse:**
```bash
fly -t main login -c http://your-concourse-url
```

3. **Set Pipeline:**
```bash
fly -t main set-pipeline -p etl-pipeline -c All\ pipelines.yml
fly -t main unpause-pipeline -p etl-pipeline
```

#### Pipeline Configuration Files

- **`All pipelines.yml`**: Main CI/CD pipeline definition
- **`netpipelines.yml`**: Network and distributed processing pipelines

---

## Monitoring and Logging

### Logging Configuration

The pipeline implements comprehensive logging:

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('etl_pipeline.log'),
        logging.StreamHandler()
    ]
)
```

### Health Monitoring

#### Health Check Endpoints
- `/health`: Overall system health
- `/metrics`: Performance metrics
- `/status`: Pipeline execution status

#### Key Metrics
- **Processing Rate**: Records processed per second
- **Error Rate**: Percentage of failed operations
- **Latency**: End-to-end processing time
- **Resource Utilization**: CPU, memory, and disk usage

### Alerting

Configure alerts for:
- Pipeline failures
- Data quality issues
- Resource exhaustion
- Performance degradation

---

## Development

### Project Structure

```
.
├── Main/                          # Main application directory
│   ├── corporate/                 # Corporate-specific modules
│   ├── workspace/                 # Working directory for processing
│   └── checkpoints/              # Processing checkpoints
├── credentials.yml               # Configuration credentials (template)
├── docker-compose.yml           # Docker Compose configuration
├── requirements.txt             # Python dependencies
├── All pipelines.yml           # Main CI/CD pipeline config
├── netpipelines.yml           # Network pipeline config
├── ETL.py                      # Main ETL module
├── ETL_Input.py               # Data input module
├── ETL2.pyth                  # Secondary ETL module
├── config.py                  # Configuration module
├── login.py                   # Authentication module
├── run_all.sh                 # Batch execution script
├── table_extractor.py         # Table extraction utility
├── select_columns.py          # Column selection utility
├── converter.py               # Data conversion utility
├── click_save.py              # Data persistence utility
├── click_watchdog.py          # File monitoring utility
└── common_methods.csv         # Shared utility functions
```

### Coding Standards

- **Python Style**: Follow PEP 8 guidelines
- **Documentation**: Comprehensive docstrings for all functions
- **Type Hints**: Use type annotations for better code clarity
- **Error Handling**: Implement robust error handling and logging
- **Testing**: Write unit tests for all components

### Adding New Features

1. **Create Feature Branch:**
```bash
git checkout -b feature/your-feature-name
```

2. **Implement Changes:**
   - Add new modules in appropriate directories
   - Update configuration files as needed
   - Add comprehensive tests

3. **Test Changes:**
```bash
# Run unit tests
python -m pytest tests/

# Run integration tests
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

4. **Update Documentation:**
   - Update this README
   - Add inline code documentation
   - Update API documentation

---

## Troubleshooting

### Common Issues

#### Docker Issues

**Problem**: Container fails to start
```bash
# Check container logs
docker-compose logs service-name

# Check container status
docker-compose ps

# Rebuild containers
docker-compose up --build --force-recreate
```

**Problem**: Port conflicts
```bash
# Check which process is using the port
sudo lsof -i :port-number

# Kill the process or change port in docker-compose.yml
```

#### Pipeline Issues

**Problem**: ETL pipeline fails
```bash
# Check logs for specific error
tail -f logs/etl_pipeline.log

# Run pipeline in debug mode
python ETL.py --debug

# Check data source connectivity
python -c "import config; config.test_connections()"
```

**Problem**: Data validation errors
- Check source data format and schema
- Verify transformation logic
- Review data quality rules

#### Performance Issues

**Problem**: Slow processing
- Increase container resources in docker-compose.yml
- Optimize SQL queries and transformations
- Implement data partitioning
- Add parallel processing

**Problem**: Memory issues
```bash
# Monitor container memory usage
docker stats

# Adjust memory limits
# In docker-compose.yml, add:
deploy:
  resources:
    limits:
      memory: 2G
```

### Debugging Commands

```bash
# Access running container
docker-compose exec service-name bash

# Check environment variables
docker-compose exec service-name env

# Monitor resource usage
docker stats

# View container processes
docker-compose exec service-name ps aux
```

### Log Analysis

```bash
# View recent logs
docker-compose logs --tail=100 service-name

# Follow logs in real-time
docker-compose logs -f service-name

# Search logs for errors
docker-compose logs service-name 2>&1 | grep -i error

# Export logs for analysis
docker-compose logs service-name > pipeline-logs.txt
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Third-Party Licenses

This project uses several open-source libraries. See `requirements.txt` for a full list of dependencies and their respective licenses.

---

## Changelog

### Version 2.0.0 (Latest)
- **Added**: Concourse CI/CD integration
- **Added**: Docker Compose orchestration
- **Added**: Advanced data transformation modules
- **Added**: Real-time file monitoring
- **Improved**: Error handling and recovery
- **Improved**: Configuration management
- **Fixed**: Memory optimization issues

### Version 1.5.0
- **Added**: Table extraction capabilities
- **Added**: Column selection utilities
- **Added**: Data format conversion
- **Improved**: Pipeline performance
- **Fixed**: Authentication issues

### Version 1.0.0
- **Initial Release**: Basic ETL functionality
- **Added**: Core extraction, transformation, and loading
- **Added**: Docker containerization
- **Added**: Basic monitoring and logging

---

## Support and Contact

### Getting Help

- **Documentation**: Check this README and inline code documentation
- **Issues**: Report bugs and feature requests via GitHub Issues
- **Discussions**: Join community discussions for questions and ideas

### Maintainer

- **Primary Maintainer**: kadar khan - kadar7715890925@gmail.com

---

**🚀 Happy Data Engineering!**

---

