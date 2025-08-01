import csv
import sys
from typing import List, Optional, TextIO
from .parser import Paper
import logging

logger = logging.getLogger(__name__)

class CSVExporter:
    """Exporter for converting papers to CSV format"""
    
    HEADERS = [
        'PubmedID',
        'Title', 
        'Publication Date',
        'Non-academic Author(s)',
        'Company Affiliation(s)',
        'Corresponding Author Email'
    ]
    
    def format_authors_list(self, authors: List) -> str:
        """Format list of authors into a string"""
        if not authors:
            return ""
        return "; ".join(author.full_name for author in authors)
    
    def format_affiliations_list(self, affiliations: List[str]) -> str:
        """Format list of company affiliations into a string"""
        if not affiliations:
            return ""
        return "; ".join(affiliations)
    
    def export_papers(self, papers: List[Paper], filename: Optional[str] = None) -> None:
        """
        Export papers to CSV file or stdout
        
        Args:
            papers: List of Paper objects to export
            filename: Output filename, if None outputs to stdout
        """
        if not papers:
            logger.warning("No papers to export")
            return
        
        output: TextIO
        if filename:
            output = open(filename, 'w', newline='', encoding='utf-8')
            logger.info(f"Exporting {len(papers)} papers to {filename}")
        else:
            output = sys.stdout
            logger.info(f"Exporting {len(papers)} papers to stdout")
        
        try:
            writer = csv.writer(output)
            writer.writerow(self.HEADERS)
            
            for paper in papers:
                # Get company authors and affiliations (these should be set by the filter)
                company_authors = getattr(paper, 'company_authors', [])
                company_affiliations = getattr(paper, 'company_affiliations', [])
                
                row = [
                    paper.pmid,
                    paper.title,
                    paper.publication_date,
                    self.format_authors_list(company_authors),
                    self.format_affiliations_list(company_affiliations),
                    paper.corresponding_author_email or ""
                ]
                writer.writerow(row)
                
        finally:
            if filename:
                output.close()
                
        logger.info("Export completed successfully")

