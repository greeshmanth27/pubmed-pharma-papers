from typing import List, Set, Optional, Tuple
import re
from .parser import Paper, Author
import logging

logger = logging.getLogger(__name__)

class CompanyFilter:
    """Filter for identifying pharmaceutical and biotech company affiliations"""
    
    def __init__(self) -> None:
        # Major pharmaceutical companies (extend this list as needed)
        self.pharma_keywords = {
            'pfizer', 'novartis', 'roche', 'merck', 'johnson & johnson', 'j&j',
            'bristol myers squibb', 'bms', 'abbvie', 'amgen', 'gilead',
            'biogen', 'regeneron', 'vertex', 'moderna', 'biontech',
            'gsk', 'glaxosmithkline', 'sanofi', 'takeda', 'astrazeneca',
            'eli lilly', 'lilly', 'boehringer ingelheim', 'celgene',
            'alexion', 'incyte', 'illumina', 'genentech', 'immunogen',
            'seagen', 'seattle genetics', 'gilead sciences', 'biogen idec',
            'pharmaceuticals', 'pharma', 'biotech', 'biotechnology',
            'therapeutic', 'therapeutics', 'drug development', 'clinical research',
            'inc.', 'corp.', 'corporation', 'ltd.', 'limited', 'company', 'co.'
        }
        
        # Academic institution indicators (to exclude)
        self.academic_keywords = {
            'university', 'college', 'institute', 'hospital', 'medical center',
            'research center', 'centre', 'laboratory', 'school of medicine',
            'medical school', 'department', 'faculty', 'academic', 'clinic',
            'health system', 'healthcare', 'medical institute', 'research institute'
        }
        
        # Corporate email domains (common patterns)
        self.corporate_domains = {
            'pfizer.com', 'novartis.com', 'roche.com', 'merck.com',
            'jnj.com', 'bms.com', 'abbvie.com', 'amgen.com',
            'gilead.com', 'biogen.com', 'regeneron.com', 'vrtx.com',
            'modernatx.com', 'biontech.de', 'gsk.com', 'sanofi.com'
        }
    
    def extract_domain_from_email(self, email: str) -> Optional[str]:
        """Extract domain from email address"""
        if '@' in email:
            return email.split('@')[1].lower()
        return None
    
    def is_corporate_email(self, email: str) -> bool:
        """Check if email domain suggests corporate affiliation"""
        domain = self.extract_domain_from_email(email)
        if not domain:
            return False
            
        # Check against known corporate domains
        if domain in self.corporate_domains:
            return True
            
        # Check for corporate patterns (.com but not .edu, .org, .gov)
        if (domain.endswith('.com') and 
            not any(academic in domain for academic in ['edu', 'ac.', 'univ'])):
            return True
            
        return False
    
    def is_academic_affiliation(self, affiliation: str) -> bool:
        """Check if affiliation suggests academic institution"""
        affiliation_lower = affiliation.lower()
        
        # Strong indicators of academic affiliation
        academic_indicators = [
            '.edu', 'university', 'college', 'school of', 'medical school',
            'institute of', 'department of', 'faculty of', 'academic'
        ]
        
        return any(indicator in affiliation_lower for indicator in academic_indicators)
    
    def is_company_affiliation(self, affiliation: str) -> bool:
        """
        Determine if affiliation is a pharmaceutical/biotech company
        
        Args:
            affiliation: Author affiliation string
            
        Returns:
            True if affiliation appears to be a pharmaceutical/biotech company
        """
        if not affiliation:
            return False
            
        affiliation_lower = affiliation.lower()
        
        # First, exclude academic institutions
        if self.is_academic_affiliation(affiliation):
            return False
        
        # Check for pharmaceutical company keywords
        for keyword in self.pharma_keywords:
            if keyword in affiliation_lower:
                logger.debug(f"Found pharma keyword '{keyword}' in: {affiliation}")
                return True
                
        # Check for corporate structure indicators
        corporate_indicators = ['inc.', 'corp.', 'ltd.', 'limited', 'llc', 'gmbh']
        if any(indicator in affiliation_lower for indicator in corporate_indicators):
            # Additional check to ensure it's not just any corporation
            business_keywords = ['pharmaceutical', 'biotech', 'therapeutic', 'drug', 'clinical']
            if any(keyword in affiliation_lower for keyword in business_keywords):
                return True
        
        return False
    
    def extract_company_name(self, affiliation: str) -> Optional[str]:
        """
        Extract company name from affiliation string
        
        Args:
            affiliation: Author affiliation string
            
        Returns:
            Extracted company name or None
        """
        if not self.is_company_affiliation(affiliation):
            return None
        
        # Simple extraction - take the first part before comma or period
        # This is a heuristic and may need refinement
        company_name = affiliation.split(',')[0].strip()
        company_name = company_name.split('.')[0].strip()
        
        # Clean up common suffixes
        suffixes = [' Inc', ' Corp', ' Ltd', ' Limited', ' LLC', ' GmbH']
        for suffix in suffixes:
            if company_name.endswith(suffix):
                company_name = company_name[:-len(suffix)].strip()
        
        return company_name if company_name else None
    
    def filter_papers_with_company_authors(self, papers: List[Paper]) -> List[Paper]:
        """
        Filter papers to include only those with at least one company-affiliated author
        
        Args:
            papers: List of Paper objects
            
        Returns:
            Filtered list of papers with company-affiliated authors
        """
        filtered_papers = []
        
        for paper in papers:
            company_authors = []
            company_affiliations = []
            
            for author in paper.authors:
                if self.is_company_affiliation(author.affiliation):
                    company_authors.append(author)
                    company_name = self.extract_company_name(author.affiliation)
                    if company_name and company_name not in company_affiliations:
                        company_affiliations.append(company_name)
                
                # Also check email domain if available
                if author.email and self.is_corporate_email(author.email):
                    if author not in company_authors:
                        company_authors.append(author)
            
            if company_authors:
                # Add metadata for company authors and affiliations
                paper.company_authors = company_authors
                paper.company_affiliations = company_affiliations
                filtered_papers.append(paper)
                logger.debug(f"Paper {paper.pmid} has {len(company_authors)} company authors")
        
        logger.info(f"Filtered {len(filtered_papers)} papers with company authors from {len(papers)} total papers")
        return filtered_papers