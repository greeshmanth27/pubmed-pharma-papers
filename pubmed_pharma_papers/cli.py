import click
import logging
import sys
from typing import Optional

from .api_client import PubMedAPIClient, PubMedConfig, PubMedAPIError
from .parser import PubMedParser
from .filter import CompanyFilter
from .exporter import CSVExporter

def setup_logging(debug: bool) -> None:
    """Setup logging configuration"""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        stream=sys.stderr
    )

@click.command()
@click.argument('query', required=True)
@click.option('-d', '--debug', is_flag=True, help='Print debug information during execution')
@click.option('-f', '--file', 'filename', help='Specify the filename to save the results')
@click.option('--email', help='Email address for PubMed API (recommended for higher rate limits)')
@click.option('--api-key', help='API key for PubMed API (for higher rate limits)')
@click.option('--max-results', default=100, help='Maximum number of results to fetch')
def main(query: str, debug: bool, filename: Optional[str], email: Optional[str], 
         api_key: Optional[str], max_results: int) -> None:
    """
    Fetch research papers from PubMed with pharmaceutical company-affiliated authors.
    
    QUERY: PubMed search query (supports full PubMed syntax)
    
    Examples:
        get-papers-list "cancer drug discovery"
        get-papers-list "diabetes[MeSH] AND 2023[PDAT]" --file results.csv
        get-papers-list "COVID-19 therapeutics" --debug --max-results 50
    """
    setup_logging(debug)
    logger = logging.getLogger(__name__)
    
    try:
        # Initialize components
        config = PubMedConfig(email=email, api_key=api_key)
        api_client = PubMedAPIClient(config)
        parser = PubMedParser()
        company_filter = CompanyFilter()
        exporter = CSVExporter()
        
        logger.info(f"Starting search for query: {query}")
        
        # Step 1: Search for papers
        pmids = api_client.search_papers(query, max_results)
        if not pmids:
            logger.warning("No papers found for the given query")
            sys.exit(0)
        
        # Step 2: Fetch paper details
        xml_data = api_client.fetch_paper_details(pmids)
        
        # Step 3: Parse papers
        papers = parser.parse_papers(xml_data)
        if not papers:
            logger.warning("No papers could be parsed from the response")
            sys.exit(0)
        
        # Step 4: Filter papers with company authors
        filtered_papers = company_filter.filter_papers_with_company_authors(papers)
        if not filtered_papers:
            logger.warning("No papers found with pharmaceutical/biotech company authors")
            sys.exit(0)
        
        # Step 5: Export results
        exporter.export_papers(filtered_papers, filename)
        
        logger.info(f"Successfully processed {len(filtered_papers)} papers with company authors")
        
    except PubMedAPIError as e:
        logger.error(f"PubMed API error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        if debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
