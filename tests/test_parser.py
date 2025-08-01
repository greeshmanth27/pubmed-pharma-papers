import pytest
import xml.etree.ElementTree as ET
from pubmed_pharma_papers.parser import PubMedParser, Paper, Author

class TestPubMedParser:
    """Test cases for PubMedParser"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.parser = PubMedParser()
    
    def test_extract_email_from_text(self):
        """Test email extraction from text"""
        text = "Department of Medicine, University Hospital, email: test@example.com"
        email = self.parser.extract_email_from_text(text)
        assert email == "test@example.com"
        
        # Test no email
        text_no_email = "Department of Medicine, University Hospital"
        email = self.parser.extract_email_from_text(text_no_email)
        assert email is None
    
    def test_parse_publication_date(self):
        """Test publication date parsing"""
        xml_str = '''
        <PubmedArticle>
            <ArticleDate>
                <Year>2023</Year>
                <Month>05</Month>
                <Day>15</Day>
            </ArticleDate>
        </PubmedArticle>
        '''
        article_elem = ET.fromstring(xml_str)
        date = self.parser.parse_publication_date(article_elem)
        assert date == "2023-05-15"
    
    def test_parse_authors(self):
        """Test author parsing"""
        xml_str = '''
        <PubmedArticle>
            <AuthorList>
                <Author>
                    <ForeName>John</ForeName>
                    <LastName>Doe</LastName>
                    <Affiliation>Pfizer Inc., New York, NY</Affiliation>
                </Author>
                <Author>
                    <ForeName>Jane</ForeName>
                    <LastName>Smith</LastName>
                    <Affiliation>University of California, email: jane@example.com</Affiliation>
                </Author>
            </AuthorList>
        </PubmedArticle>
        '''
        article_elem = ET.fromstring(xml_str)
        authors = self.parser.parse_authors(article_elem)
        
        assert len(authors) == 2
        assert authors[0].first_name == "John"
        assert authors[0].last_name == "Doe"
        assert "Pfizer" in authors[0].affiliation
        assert authors[1].email == "jane@example.com"
