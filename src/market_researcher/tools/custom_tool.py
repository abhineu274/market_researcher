from crewai.tools import BaseTool
import requests
import os
from bs4 import BeautifulSoup

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