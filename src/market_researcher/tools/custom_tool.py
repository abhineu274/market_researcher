from crewai.tools import BaseTool
import requests
import os
from bs4 import BeautifulSoup
import PyPDF2

# Define a minimal WebScraperTool if not available from an import
class WebScraperTool(BaseTool):
    def scrape(self, url: str):
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        return response.text

class BSEWebTool(WebScraperTool):
    name: str = "BSE Data Fetcher"
    description: str = "Fetches latest stock data and news from the Bombay Stock Exchange website."
    
    def _run(self, query: str = ""):
            url = "https://www.bseindia.com/markets/equity"
            try:
                response = requests.get(url, timeout=20)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                # Try to find the date string (update selector as needed)
                date_elem = soup.find("span", {"id": "ContentPlaceHolder1_lblDate"})
                date_str = date_elem.get_text(strip=True) if date_elem else "Date not found"
                return f"Latest BSE data date: {date_str}"
            except Exception as e:
                return f"Error fetching BSE data: {e}"

class MoneycontrolWebTool(WebScraperTool):
    name: str = "Moneycontrol Data Fetcher"
    description: str = "Fetches latest stock data and news from the Moneycontrol website."

    def _run(self, query: str = ""):
        url = "https://www.moneycontrol.com/stocks/marketstats/nsegainer/index.php"
        try:
            response = requests.get(url, timeout=20)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            # Example: Find the date string (update selector as needed)
            date_elem = soup.find("span", class_="gD_12")  # This class may change, inspect the page for the latest
            date_str = date_elem.get_text(strip=True) if date_elem else "Date not found"
            return f"Latest Moneycontrol data date: {date_str}"
        except Exception as e:
            return f"Error fetching Moneycontrol data: {e}"

class SerperSearchTool(BaseTool):
    name: str = "Serper.dev Search"
    description: str = "Performs Google-like search using the Serper.dev API for latest news and info."

    def _run(self, query: str):
        api_key = os.getenv("SERPER_API_KEY")
        if not api_key:
            return "Serper.dev API key not set. Please set SERPER_API_KEY in your environment."
        url = "https://google.serper.dev/search"
        headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
        data = {"q": query}
        try:
            resp = requests.post(url, headers=headers, json=data, timeout=20)
            resp.raise_for_status()
            results = resp.json()
            if "organic" in results:
                summary = "\n".join([
                    f"{item['title']}: {item['link']}" for item in results["organic"][:3]
                ])
                return f"Top Serper.dev results for '{query}':\n{summary}"
            return f"No results found for '{query}'."
        except Exception as e:
            return f"Error using Serper.dev: {e}"
    name:str = "Serper.dev Search"
    description:str = "Performs Google-like search using the Serper.dev API for latest news and info."

    def run(self, query: str):
        api_key = os.getenv("SERPER_API_KEY")
        if not api_key:
            return "Serper.dev API key not set. Please set SERPER_API_KEY in your environment."
        url = "https://google.serper.dev/search"
        headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
        data = {"q": query}
        try:
            resp = requests.post(url, headers=headers, json=data, timeout=20)
            resp.raise_for_status()
            results = resp.json()
            # Return top 3 results summary
            if "organic" in results:
                summary = "\n".join([
                    f"{item['title']}: {item['link']}" for item in results["organic"][:3]
                ])
                return f"Top Serper.dev results for '{query}':\n{summary}"
            return f"No results found for '{query}'."
        except Exception as e:
            return f"Error using Serper.dev: {e}"

class HinduNewsTool(BaseTool):
    name: str = "The Hindu News Scraper"
    description: str = "Fetches and summarizes news articles from The Hindu for a given date."

    def _run(self, query: str = ""):
        import datetime
        from bs4 import BeautifulSoup

        # Get yesterday's date in YYYY/MM/DD format
        yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y/%m/%d")
        url = f"https://www.thehindu.com/archive/web/{yesterday}/"
        try:
            response = requests.get(url, timeout=20)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            # Find all news headlines/links (update selector as needed)
            articles = soup.find_all("a", class_="archive-list-link")
            headlines = [a.get_text(strip=True) for a in articles][:10]  # Top 10
            return "The Hindu headlines for yesterday:\n" + "\n".join(headlines)
        except Exception as e:
            return f"Error fetching The Hindu news: {e}"
        
class PDFTextExtractorTool(BaseTool):
    name: str = "PDF Text Extractor"
    description: str = "Extracts text from a provided PDF file path."

    def _run(self, pdf_path: str):
        print(f"[DEBUG] PDFTextExtractorTool received pdf_path: {pdf_path}")
        try:
            if not os.path.exists(pdf_path):
                print(f"[DEBUG] File does not exist at: {pdf_path}")
            with open(r"knowledge\PolityNotes.pdf", "rb") as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""
            # Split text into chunks of 4000 characters
            chunk_size = 4000
            chunks = [text[i:i+chunk_size] for i in range(0, 10000, chunk_size)]
            return chunks
        except Exception as e:
            print(f"[DEBUG] Exception: {e}")
            return [f"Error extracting text from PDF: {e}"]