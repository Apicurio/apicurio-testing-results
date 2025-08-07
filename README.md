# Apicurio Registry QE Testing Results

This repository contains the results and summaries of Quality Assurance (QE) testing for Apicurio Registry. All test results from automated QE workflows are collected here and made available through interactive HTML dashboards.

## 🔗 View Test Results

**Browse the latest test results at: https://www.apicur.io/apicurio-testing-results/**

## What's Inside

This repository serves as the central location for:

- **Test Results**: Comprehensive QE test results from multiple configurations and environments
- **Interactive Dashboards**: HTML summaries providing easy navigation through test outcomes
- **Historical Data**: Archive of test runs over time to track quality trends
- **Multi-Configuration Coverage**: Results from various storage backends, OpenShift versions, and test scenarios

### Test Coverage

The QE testing workflow provides comprehensive quality assurance by testing:

1. **Multiple Storage Backends**: In-memory, PostgreSQL (12, 17), MySQL, and Kafka (Strimzi 0.43, 0.47)
2. **Integration Testing**: Maven-based integration tests covering core functionality
3. **UI Testing**: Playwright-based browser automation tests
4. **Security Testing**: DAST (Dynamic Application Security Testing) vulnerability scans
5. **Authentication Testing**: Tests with various authentication configurations

## Repository Structure

Each test run is organized in timestamped directories (e.g., `2025-08-06-16780041188/`) containing:

- **Job Results**: Individual subdirectories for each test configuration
- **Test Reports**: Detailed test results in standardized formats
- **Pod Logs**: Application logs from test environments
- **Security Scans**: DAST vulnerability assessment results
- **Summary Dashboard**: Generated `index.html` with interactive overview

### Browsing Results

- **Main Dashboard**: The root `index.html` lists all test runs with quick status indicators
- **Individual Summaries**: Each test run has its own detailed dashboard
- **Raw Data**: All original test files are preserved for detailed analysis

## Dashboard Features

### Main Dashboard

The main dashboard provides a comprehensive overview of all test runs:
- **Chronological Listing**: Test runs organized by date with unique identifiers
- **Quick Status**: At-a-glance indicators for test outcomes
- **Job Counts**: Summary of integration tests, UI tests, and security scans
- **Direct Navigation**: Links to detailed summaries and raw result files

### Individual Test Run Summaries

Each test run includes an interactive dashboard with:

#### Summary Statistics
- **Integration Test Jobs**: Count and status of Maven integration test executions
- **UI Test Jobs**: Count and status of Playwright UI test executions  
- **Security Scan Jobs**: Count and status of DAST security scan executions
- **Overall Results**: Aggregate pass/fail statistics across all test types

#### Detailed Breakdown

**Integration Tests**
- **Test Statistics**: Total, passed, failed, and skipped test counts per configuration
- **Test Suites**: Individual test suite results with execution times and failure details
- **Configuration Matrix**: Results across OpenShift versions, storage backends, and test scenarios

**UI Tests**
- **Test Status**: Overall pass/fail status for browser automation tests
- **Interactive Reports**: Links to detailed Playwright HTML reports with screenshots and traces
- **Cross-Browser Coverage**: Results from different browser configurations

**Security Scans (DAST)**
- **Vulnerability Assessment**: Total security issues categorized by severity
- **Scan Coverage**: Individual scan results across different API endpoints
- **SARIF Integration**: Industry-standard security findings format for tooling integration

## Test Configurations

Results are available for multiple test configurations and environments:

### OpenShift Versions
- `os419` → OpenShift 4.19

### Storage Backends
- `inmemory` → In-Memory storage
- `pg12`, `pg17` → PostgreSQL 12, 17
- `mysql` → MySQL
- `strimzi043`, `strimzi047` → Strimzi Kafka 0.43, 0.47

### Test Types
- `integrationtests` → Maven Surefire/Failsafe integration tests
- `uitests` → Playwright UI automation tests
- `dastscan` → RapiDAST security vulnerability scans

---

## Implementation Details

This section describes the technical implementation used to generate the dashboards and summaries.

### Summary Generation Scripts

The repository includes Python scripts that automatically process test results:

- **`generate-workflow-summary.py`**: Creates HTML summaries for individual test runs
- **`update-index.py`**: Generates the main dashboard listing all test runs

#### Usage

```bash
# Generate a summary for a specific test run
python generate-workflow-summary.py <workflow-directory>

# Update the main index
python update-index.py
```

#### Example

```bash
# Generate a workflow summary report for a specific workflow run
python generate-workflow-summary.py 2025-08-06-16780041188

# Update the main index with current workflow directories
python update-index.py
```

### File Structure Analysis

The scripts automatically parse and analyze various result formats:

#### Integration Test Results
- **Location**: `<job-dir>/test-results/failsafe-reports/`
- **Format**: Maven Surefire XML format
- **Key Files**: `failsafe-summary.xml`, `TEST-*.xml`

#### UI Test Results  
- **Location**: `<job-dir>/test-results/`
- **Format**: Playwright HTML reports and JSON data
- **Key Files**: `index.html`, `results.json`

#### DAST Security Scan Results
- **Location**: `<job-dir>/dast-results/<scan-name>/`
- **Format**: SARIF (Static Analysis Results Interchange Format)
- **Key Files**: `*.sarif`, `scan-status.txt`

### Requirements

- Python 3.6+
- Standard library only (no external dependencies)
- Automated execution via GitHub Actions workflow
