from typing import List, Optional, Dict
from dataclasses import dataclass
import xml.etree.ElementTree as ET
import re
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@dataclass
class Author:
    """Represents a paper author"""
    first_name: str
    last_name: str
    affiliation: str
    email: Optional[str] = None
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

@dataclass
class Paper:
    """Represents a research paper"""
    pmid: str
    title: str
    publication_date: str
    authors: List[Author]
    corresponding_author_email: Optional[str] = None

class PubMedParser:
    """Parser for PubMed XML responses"""
    
    def safe_find_text(self, element: ET.Element, path: str, default: str = "") -> str:
        """Safely extract text from XML element"""
        found = element.find(path)
        return found.text if found is not None and found.text else default
    
    def extract_email_from_text(self, text: str) -> Optional[str]:
        """Extract email address from text using regex"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.findall(email_pattern, text)
        return matches[0] if matches else None
    
    def parse_publication_date(self, article_elem: ET.Element) -> str:
        """Parse publication date from article element"""
        # Try different date elements in order of preference
        date_elements = [
            './/ArticleDate',
            './/PubDate',
            './/DateCompleted',
            './/DateRevised'
        ]
        
        for date_path in date_elements:
            date_elem = article_elem.find(date_path)
            if date_elem is not None:
                year = self.safe_find_text(date_elem, 'Year', '1900')
                month = self.safe_find_text(date_elem, 'Month', '01')
                day = self.safe_find_text(date_elem, 'Day', '01')
                
                # Handle month names
                month_map = {
                    'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
                    'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
                    'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
                }
                
                if month in month_map:
                    month = month_map[month]
                
                try:
                    # Validate and format date
                    month = month.zfill(2)
                    day = day.zfill(2)
                    datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")
                    return f"{year}-{month}-{day}"
                except ValueError:
                    continue
        
        return "1900-01-01"  # Default date if none found
    
    def parse_authors(self, article_elem: ET.Element) -> List[Author]:
        """Parse authors from article element"""
        authors = []
        author_list = article_elem.find('.//AuthorList')
        
        if author_list is None:
            logger.warning("No author list found in article")
            return authors
        
        for author_elem in author_list.findall('Author'):
            # Extract name components
            first_name = self.safe_find_text(author_elem, 'ForeName')
            last_name = self.safe_find_text(author_elem, 'LastName')
            
            if not last_name:  # Skip if no last name
                continue
            
            # Extract affiliation
            affiliation_elem = author_elem.find('.//Affiliation')
            affiliation = affiliation_elem.text if affiliation_elem is not None and affiliation_elem.text else ""
            
            # Try to extract email from affiliation
            email = self.extract_email_from_text(affiliation) if affiliation else None
            
            authors.append(Author(
                first_name=first_name,
                last_name=last_name,
                affiliation=affiliation,
                email=email
            ))
        
        return authors
    
    def find_corresponding_author_email(self, paper: Paper) -> Optional[str]:
        """Find corresponding author email from authors list"""
        # First, look for any author with an email
        for author in paper.authors:
            if author.email:
                return author.email
        
        return None
    
    def parse_papers(self, xml_data: ET.Element) -> List[Paper]:
        """
        Parse XML response into Paper objects
        
        Args:
            xml_data: XML root element from PubMed API
            
        Returns:
            List of Paper objects
        """
        papers = []
        
        for article_elem in xml_data.findall('.//PubmedArticle'):
            try:
                # Extract basic information
                pmid_elem = article_elem.find('.//PMID')
                if pmid_elem is None or not pmid_elem.text:
                    logger.warning("Skipping article without PMID")
                    continue
                
                pmid = pmid_elem.text
                title = self.safe_find_text(article_elem, './/ArticleTitle')
                
                if not title:
                    logger.warning(f"Skipping article {pmid} without title")
                    continue
                
                # Parse publication date
                publication_date = self.parse_publication_date(article_elem)
                
                # Parse authors
                authors = self.parse_authors(article_elem)
                
                # Create paper object
                paper = Paper(
                    pmid=pmid,
                    title=title,
                    publication_date=publication_date,
                    authors=authors
                )
                
                # Find corresponding author email
                paper.corresponding_author_email = self.find_corresponding_author_email(paper)
                
                papers.append(paper)
                logger.debug(f"Parsed paper {pmid}: {title[:50]}...")
                
            except Exception as e:
                logger.error(f"Error parsing article: {e}")
                continue
        
        logger.info(f"Successfully parsed {len(papers)} papers")
        return papers
