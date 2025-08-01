import pytest
import xml.etree.ElementTree as ET
from unittest.mock import Mock, patch
from pubmed_pharma_papers.api_client import PubMedAPIClient, PubMedConfig, PubMedAPIError

class TestPubMedAPIClient:
    """Test cases for PubMedAPIClient"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.config = PubMedConfig(email="test@example.com")
        self.client = PubMedAPIClient(self.config)
    
    @patch('pubmed_pharma_papers.api_client.requests.Session.get')
    def test_search_papers_success(self, mock_get):
        """Test successful paper search"""
        # Mock response
        mock_response = Mock()
        mock_response.content = b'''<?xml version="1.0"?>
        <eSearchResult>
            <IdList>
                <Id>12345</Id>
                <Id>67890</Id>
            </IdList>
        </eSearchResult>'''
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Test search
        pmids = self.client.search_papers("cancer drug", max_results=10)
        
        assert pmids == ['12345', '67890']
        mock_get.assert_called_once()
    
    @patch('pubmed_pharma_papers.api_client.requests.Session.get')
    def test_search_papers_no_results(self, mock_get):
        """Test search with no results"""
        mock_response = Mock()
        mock_response.content = b'''<?xml version="1.0"?>
        <eSearchResult>
            <IdList/>
        </eSearchResult>'''
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        pmids = self.client.search_papers("nonexistent query")
        assert pmids == []
    
    @patch('pubmed_pharma_papers.api_client.requests.Session.get')
    def test_api_error_handling(self, mock_get):
        """Test API error handling"""
        mock_get.side_effect = Exception("Network error")
        
        with pytest.raises(PubMedAPIError):
            self.client.search_papers("test query")
