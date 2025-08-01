"""
PubMed Pharma Papers - Fetch research papers with pharmaceutical company authors
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .api_client import PubMedAPIClient, PubMedConfig
from .parser import PubMedParser, Paper, Author
from .filter import CompanyFilter
from .exporter import CSVExporter

__all__ = [
    'PubMedAPIClient',
    'PubMedConfig', 
    'PubMedParser',
    'Paper',
    'Author',
    'CompanyFilter',
    'CSVExporter'
]