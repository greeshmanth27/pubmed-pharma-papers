from typing import Optional, List, Dict, Any
import requests
import xml.etree.ElementTree as ET
import time
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class PubMedConfig:
    """Configuration for PubMed API client"""
    base_url: str = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    email: Optional[str] = None
    api_key: Optional[str] = None
    rate_limit_delay: float = 0.34  # ~3 requests per second

class PubMedAPIError(Exception):
    """Custom exception for PubMed API errors"""
    pass

class PubMedAPIClient:
    """Client for interacting with PubMed E-utilities API"""
    
    def __init__(self, config: PubMedConfig) -> None:
        self.config = config
        self.session = requests.Session()
        
    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> requests.Response:
        """Make a request to PubMed API with rate limiting"""
        url = f"{self.config.base_url}{endpoint}"
        
        # Add common parameters
        if self.config.email:
            params['email'] = self.config.email
        if self.config.api_key:
            params['api_key'] = self.config.api_key
            
        logger.debug(f"Making request to {url} with params: {params}")
        
        # Rate limiting
        time.sleep(self.config.rate_limit_delay)
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            raise PubMedAPIError(f"API request failed: {e}")
    
    def search_papers(self, query: str, max_results: int = 100) -> List[str]:
        """
        Search for papers and return list of PubMed IDs
        
        Args:
            query: Search query in PubMed format
            max_results: Maximum number of results to return
            
        Returns:
            List of PubMed IDs
        """
        params = {
            'db': 'pubmed',
            'term': query,
            'retmax': max_results,
            'retmode': 'xml'
        }
        
        response = self._make_request('esearch.fcgi', params)
        
        try:
            root = ET.fromstring(response.content)
            id_list = root.find('.//IdList')
            if id_list is None:
                return []
            
            pmids = [id_elem.text for id_elem in id_list.findall('Id') if id_elem.text]
            logger.info(f"Found {len(pmids)} papers for query: {query}")
            return pmids
            
        except ET.ParseError as e:
            raise PubMedAPIError(f"Failed to parse search results: {e}")
    
    def fetch_paper_details(self, pmids: List[str]) -> ET.Element:
        """
        Fetch detailed paper information for given PMIDs
        
        Args:
            pmids: List of PubMed IDs
            
        Returns:
            XML Element containing paper details
        """
        if not pmids:
            raise ValueError("No PMIDs provided")
            
        # Join PMIDs with commas
        id_list = ','.join(pmids)
        
        params = {
            'db': 'pubmed',
            'id': id_list,
            'retmode': 'xml',
            'rettype': 'abstract'
        }
        
        response = self._make_request('efetch.fcgi', params)
        
        try:
            root = ET.fromstring(response.content)
            logger.info(f"Fetched details for {len(pmids)} papers")
            return root
        except ET.ParseError as e:
            raise PubMedAPIError(f"Failed to parse paper details: {e}")
