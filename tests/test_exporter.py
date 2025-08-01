import pytest
import io
import csv
from pubmed_pharma_papers.exporter import CSVExporter
from pubmed_pharma_papers.parser import Paper, Author

class TestCSVExporter:
    """Test cases for CSVExporter"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.exporter = CSVExporter()
    
    def test_format_authors_list(self):
        """Test author list formatting"""
        authors = [
            Author("John", "Doe", "Pfizer Inc."),
            Author("Jane", "Smith", "Novartis Corp.")
        ]
        formatted = self.exporter.format_authors_list(authors)
        assert formatted == "John Doe; Jane Smith"
        
        # Test empty list
        assert self.exporter.format_authors_list([]) == ""
    
    def test_format_affiliations_list(self):
        """Test affiliations list formatting"""
        affiliations = ["Pfizer", "Novartis", "Roche"]
        formatted = self.exporter.format_affiliations_list(affiliations)
        assert formatted == "Pfizer; Novartis; Roche"
    
    def test_export_papers_to_string(self):
        """Test CSV export functionality"""
        # Create test paper
        company_author = Author("John", "Doe", "Pfizer Inc.")
        paper = Paper("12345", "Test Paper", "2023-01-01", [company_author], "john@pfizer.com")
        
        # Add company metadata (normally done by filter)
        paper.company_authors = [company_author]
        paper.company_affiliations = ["Pfizer"]
        
        # Capture output to string buffer
        import sys
        from unittest.mock import patch
        
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.exporter.export_papers([paper])
            output = mock_stdout.getvalue()
        
        # Parse CSV output
        reader = csv.reader(io.StringIO(output))
        rows = list(reader)
        
        # Check headers
        assert rows[0] == self.exporter.HEADERS
        
        # Check data row
        assert rows[1][0] == "12345"  # PubmedID
        assert rows[1][1] == "Test Paper"  # Title
        assert rows[1][2] == "2023-01-01"  # Publication Date
        assert rows[1][3] == "John Doe"  # Non-academic Author(s)
        assert rows[1][4] == "Pfizer"  # Company Affiliation(s)
        assert rows[1][5] == "john@pfizer.com"  # Corresponding Author Email
