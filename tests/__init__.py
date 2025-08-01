# Create a file called create_init.py
import os

# Content for main package __init__.py
main_init_content = '''"""
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
'''

# Content for tests __init__.py
tests_init_content = '"""Tests for pubmed_pharma_papers package"""'

# Create the files
with open('pubmed_pharma_papers/__init__.py', 'w') as f:
    f.write(main_init_content)

with open('tests/__init__.py', 'w') as f:
    f.write(tests_init_content)

print("✅ __init__.py files created successfully!")
