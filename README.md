PubMed Pharma Papers
A Python command-line tool to fetch research papers from PubMed that have at least one author affiliated with pharmaceutical or biotech companies, and export the results as CSV.
Table of Contents

Overview
Features
Installation
Usage
Output Format
Architecture
Development
Testing
Publishing
Tools and Resources Used
Examples
License

Overview
This tool addresses the need to identify research papers where pharmaceutical or biotech companies are involved as co-authors. It uses the PubMed E-utilities API to search for papers, identifies company-affiliated authors using intelligent heuristics, and exports the results in a structured CSV format.
Features

PubMed Integration: Full support for PubMed's query syntax and E-utilities API
Smart Company Detection: Identifies pharmaceutical/biotech company affiliations using multiple heuristics
Academic Filtering: Excludes university and academic institutions to focus on industry authors
CSV Export: Structured output with author details and company affiliations
Command-Line Interface: Easy-to-use CLI with comprehensive options
Type Safety: Fully typed Python code with mypy compliance
Robust Error Handling: Graceful handling of API failures and edge cases
Rate Limiting: Respects PubMed API limits with configurable delays

Installation
Prerequisites

Python 3.8 or higher
Poetry (for dependency management)

Setup Instructions

Clone the repository:
bashgit clone https://github.com/yourusername/pubmed-pharma-papers.git
cd pubmed-pharma-papers

Install Poetry (if not already installed):
bash# macOS/Linux
curl -sSL https://install.python-poetry.org | python3 -

# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -

Install dependencies:
bashpoetry install

Verify installation:
bashpoetry run get-papers-list --help


Usage
Basic Command Structure
bashget-papers-list "QUERY" [OPTIONS]
Command-Line Options
OptionDescriptionExamplequeryPubMed search query (required)"cancer drug discovery"-h, --helpDisplay usage instructions--help-d, --debugPrint debug information--debug-f, --file FILENAMESave results to CSV file--file results.csv--email EMAILEmail for PubMed API (recommended)--email user@example.com--api-key KEYAPI key for higher rate limits--api-key YOUR_KEY--max-results NMaximum results to fetch (default: 100)--max-results 50
Basic Examples
bash# Search and print to console
poetry run get-papers-list "immunotherapy"

# Save to CSV file
poetry run get-papers-list "COVID-19 therapeutics" --file covid_drugs.csv

# Use debug mode to see processing details
poetry run get-papers-list "diabetes treatment" --debug --max-results 20

# Advanced PubMed query with date range
poetry run get-papers-list "cancer[MeSH] AND drug AND 2022:2023[PDAT]" --file recent_cancer_drugs.csv
Advanced PubMed Query Examples
bash# Search specific journals
poetry run get-papers-list "Nature[Journal] AND pharmaceutical" --file nature_pharma.csv

# Search with MeSH terms
poetry run get-papers-list "Diabetes Mellitus[MeSH] AND Drug Therapy[MeSH]" --file diabetes_mesh.csv

# Search specific companies
poetry run get-papers-list "(pfizer[Affiliation] OR novartis[Affiliation])" --file company_specific.csv

# Clinical trials only
poetry run get-papers-list "clinical trial[Publication Type] AND pharmaceutical" --file clinical_trials.csv
Output Format
The tool generates CSV files with the following columns:
ColumnDescriptionExamplePubmedIDUnique PubMed identifier12345678TitleFull title of the research paper"Novel COVID-19 therapeutic approaches..."Publication DatePublication date (YYYY-MM-DD)2023-05-15Non-academic Author(s)Names of company-affiliated authors"John Doe; Jane Smith"Company Affiliation(s)Pharmaceutical/biotech companies"Pfizer Inc.; Novartis AG"Corresponding Author EmailEmail of corresponding authorjohn.doe@pfizer.com
Sample Output
csvPubmedID,Title,Publication Date,Non-academic Author(s),Company Affiliation(s),Corresponding Author Email
12345678,"Novel COVID-19 therapeutic approaches",2023-05-15,"John Doe; Jane Smith","Pfizer Inc.; Novartis AG",john.doe@pfizer.com
23456789,"Diabetes drug discovery and development",2023-03-22,"Alice Johnson","Roche Pharmaceuticals",alice.johnson@roche.com
Architecture
Project Structure
pubmed-pharma-papers/
├── pubmed_pharma_papers/          # Main package
│   ├── __init__.py               # Package initialization and exports
│   ├── api_client.py             # PubMed API interaction
│   ├── parser.py                 # XML parsing and data extraction
│   ├── filter.py                 # Company affiliation detection
│   ├── exporter.py               # CSV export functionality
│   └── cli.py                    # Command-line interface
├── tests/                        # Comprehensive test suite
│   ├── test_api_client.py        # API client tests
│   ├── test_parser.py            # Parser tests
│   ├── test_filter.py            # Filter logic tests
│   └── test_exporter.py          # Export functionality tests
├── pyproject.toml               # Poetry configuration
├── README.md                    # This documentation
└── .gitignore                   # Git ignore patterns
Component Overview

API Client (api_client.py): Handles PubMed E-utilities API interactions

Search for papers using ESearch
Fetch detailed paper information using EFetch
Rate limiting and error handling


Parser (parser.py): Processes PubMed XML responses

Extracts paper metadata (title, date, authors)
Parses author affiliations and emails
Handles missing or malformed data gracefully


Filter (filter.py): Identifies pharmaceutical/biotech company affiliations

Company keyword matching
Corporate email domain detection
Academic institution exclusion
Heuristic-based classification


Exporter (exporter.py): Generates CSV output

Formats data for CSV export
Handles file I/O and console output
Proper encoding and formatting


CLI (cli.py): Command-line interface

Argument parsing and validation
Workflow orchestration
User feedback and error reporting



Company Detection Algorithm
The tool uses multiple heuristics to identify pharmaceutical/biotech company affiliations:

Known Company Names: Matches against a comprehensive list of pharmaceutical companies

Major companies: Pfizer, Novartis, Roche, Merck, J&J, etc.
Biotech companies: Genentech, Biogen, Regeneron, etc.


Industry Keywords: Identifies industry-specific terms

"pharmaceuticals", "biotech", "therapeutic", "drug development"


Corporate Structure Indicators: Recognizes corporate entities

"Inc.", "Corp.", "Ltd.", "Limited", "Company", "LLC"


Email Domain Analysis: Analyzes email domains

Corporate domains vs. academic domains (.edu, .ac.uk)
Known pharmaceutical company domains


Academic Exclusion: Filters out academic institutions

Universities, medical schools, research institutes
Hospital and medical center affiliations



Development
Setting Up Development Environment

Clone and install:
bashgit clone https://github.com/yourusername/pubmed-pharma-papers.git
cd pubmed-pharma-papers
poetry install

Install development tools:
bashpoetry install --with dev

Run quality checks:
bash# Format code
poetry run black pubmed_pharma_papers tests
poetry run isort pubmed_pharma_papers tests

# Type checking
poetry run mypy pubmed_pharma_papers

# Linting
poetry run flake8 pubmed_pharma_papers tests


Code Quality Standards

Type Hints: All functions and methods have complete type annotations
Documentation: Comprehensive docstrings following Google style
Error Handling: Robust exception handling with informative messages
Testing: High test coverage with unit and integration tests
Code Style: Black formatting, isort import sorting, flake8 linting

Testing
Running Tests
bash# Run all tests
poetry run pytest -v

# Run tests with coverage
poetry run pytest -v --cov=pubmed_pharma_papers --cov-report=term-missing

# Run specific test modules
poetry run pytest tests/test_filter.py -v

# Run tests in debug mode
poetry run pytest tests/test_api_client.py -v -s
Test Coverage
The test suite includes:

Unit Tests: Individual component testing
Integration Tests: End-to-end workflow testing
Mock Testing: API interaction testing without external calls
Edge Case Testing: Error conditions and boundary cases

Manual Testing Commands
bash# Test basic functionality
poetry run get-papers-list "pfizer" --debug --max-results 5

# Test file output
poetry run get-papers-list "COVID-19 therapeutics" --file test_output.csv --max-results 10

# Test error handling
poetry run get-papers-list "nonexistent_query_12345" --debug
Publishing
TestPyPI Publication (Bonus Feature)

Build the package:
bashpoetry build

Configure TestPyPI:
bashpoetry config repositories.testpypi https://test.pypi.org/legacy/
poetry config pypi-token.testpypi your-token-here

Publish to TestPyPI:
bashpoetry publish -r testpypi

Install from TestPyPI:
bashpip install --index-url https://test.pypi.org/simple/ pubmed-pharma-papers


Module Usage
The package can be used both as a CLI tool and as a Python module:
pythonfrom pubmed_pharma_papers import (
    PubMedAPIClient, 
    PubMedConfig, 
    PubMedParser, 
    CompanyFilter, 
    CSVExporter
)

# Initialize components
config = PubMedConfig(email="your.email@example.com")
client = PubMedAPIClient(config)
parser = PubMedParser()
filter_obj = CompanyFilter()
exporter = CSVExporter()

# Use programmatically
pmids = client.search_papers("COVID-19 therapeutics", max_results=50)
xml_data = client.fetch_paper_details(pmids)
papers = parser.parse_papers(xml_data)
filtered_papers = filter_obj.filter_papers_with_company_authors(papers)
exporter.export_papers(filtered_papers, "results.csv")
Tools and Resources Used
Core Dependencies

requests: HTTP client for PubMed API calls
click: Command-line interface framework
python-dateutil: Date parsing utilities

Development Tools

Poetry: Dependency management and packaging
pytest: Testing framework
pytest-cov: Test coverage reporting
black: Code formatting
isort: Import sorting
flake8: Code linting
mypy: Static type checking

External APIs

PubMed E-utilities API: Research paper data source
NCBI Entrez: Search and retrieval system

AI Assistance

Claude (Anthropic): Used for code generation, documentation, and architecture guidance
GitHub Copilot: Code completion and suggestions (if applicable)

Examples
Real-World Use Cases

COVID-19 Therapeutic Research:
bashpoetry run get-papers-list "COVID-19 AND (therapeutic OR treatment OR drug)" --file covid_therapeutics.csv --max-results 200

Cancer Drug Discovery:
bashpoetry run get-papers-list "(cancer OR oncology) AND drug discovery AND 2022:2023[PDAT]" --file cancer_drugs_recent.csv

Diabetes Treatment Research:
bashpoetry run get-papers-list "diabetes[MeSH] AND therapeutic[MeSH] AND pharmaceutical" --file diabetes_pharma.csv

Specific Company Research:
bashpoetry run get-papers-list "(pfizer[Affiliation] OR novartis[Affiliation] OR roche[Affiliation])" --file big_pharma_research.csv

Recent Biotech Publications:
bashpoetry run get-papers-list "biotechnology AND 2023[PDAT]" --file biotech_2023.csv --max-results 150


Expected Output Analysis
For a query like "COVID-19 therapeutics", you might expect:

Total papers found: ~1000-2000 papers
Papers with company authors: ~100-300 papers (10-30%)
Common companies: Pfizer, Moderna, Gilead, Roche, etc.
Research areas: Antiviral drugs, vaccines, monoclonal antibodies

Performance Considerations

Rate Limiting: Respects PubMed's 3 requests/second limit
Batch Processing: Efficiently fetches multiple paper details in single requests
Memory Usage: Processes papers in batches to manage memory consumption
Error Recovery: Implements retry logic for transient failures

Limitations

Metadata Only: Downloads paper metadata, not full-text PDFs
Affiliation Quality: Depends on quality of author affiliation data in PubMed
Company Detection: Heuristic-based, may miss some companies or include false positives
Rate Limits: Subject to PubMed API rate limiting (mitigated with email/API key)
Historical Data: Company affiliations may not reflect current company structures due to mergers/acquisitions

Future Enhancements

Enhanced company detection using machine learning
Support for additional databases (Scopus, Web of Science)
Full-text PDF downloading for open-access papers
Interactive web interface
Database storage for large-scale analysis
Company relationship mapping (subsidiaries, acquisitions)

License
This project is licensed under the MIT License - see the LICENSE file for details.
Acknowledgments

NCBI/PubMed for providing the E-utilities API
Pharmaceutical research community for open access publications
Poetry team for excellent dependency management
Python community for the robust ecosystem of libraries