import pytest
from pubmed_pharma_papers.filter import CompanyFilter
from pubmed_pharma_papers.parser import Author, Paper

class TestCompanyFilter:
    """Test cases for CompanyFilter"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.filter = CompanyFilter()
    
    def test_is_company_affiliation_pharma(self):
        """Test pharmaceutical company detection"""
        affiliations = [
            "Pfizer Inc., New York, NY",
            "Novartis Pharmaceuticals Corporation",
            "Roche Genentech, South San Francisco",
            "Bristol Myers Squibb Company"
        ]
        
        for affiliation in affiliations:
            assert self.filter.is_company_affiliation(affiliation), f"Failed for: {affiliation}"
    
    def test_is_company_affiliation_academic(self):
        """Test academic institution exclusion"""
        affiliations = [
            "University of California, San Francisco",
            "Harvard Medical School",
            "Massachusetts Institute of Technology", 
            "Johns Hopkins Hospital"
        ]
        
        for affiliation in affiliations:
            assert not self.filter.is_company_affiliation(affiliation), f"Failed for: {affiliation}"
    
    def test_is_corporate_email(self):
        """Test corporate email detection"""
        assert self.filter.is_corporate_email("john.doe@pfizer.com")
        assert self.filter.is_corporate_email("researcher@biotech.com")
        assert not self.filter.is_corporate_email("student@university.edu")
        assert not self.filter.is_corporate_email("invalid-email")
    
    def test_extract_company_name(self):
        """Test company name extraction"""
        affiliation = "Pfizer Inc., Global R&D, New York, NY"
        company = self.filter.extract_company_name(affiliation)
        assert company == "Pfizer"
        
        # Test non-company affiliation
        affiliation = "University of California, San Francisco"
        company = self.filter.extract_company_name(affiliation)
        assert company is None
    
    def test_filter_papers_with_company_authors(self):
        """Test paper filtering"""
        # Create test papers
        company_author = Author("John", "Doe", "Pfizer Inc., NY", "john@pfizer.com")
        academic_author = Author("Jane", "Smith", "University of California", "jane@ucsf.edu")
        
        paper_with_company = Paper("12345", "Test Paper 1", "2023-01-01", [company_author, academic_author])
        paper_academic_only = Paper("67890", "Test Paper 2", "2023-01-02", [academic_author])
        
        papers = [paper_with_company, paper_academic_only]
        filtered = self.filter.filter_papers_with_company_authors(papers)
        
        assert len(filtered) == 1
        assert filtered[0].pmid == "12345"
        assert hasattr(filtered[0], 'company_authors')
        assert len(filtered[0].company_authors) == 1
