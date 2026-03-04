import requests
from bs4 import BeautifulSoup
from app.core.config import settings
from typing import List, Dict, Any, Optional

class NewsTool:
    def __init__(self):
        self.api_key = settings.GNEWS_API_KEY
        self.base_url = "https://gnews.io/api/v4/search"

    def get_company_news(self, company_name: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Fetch recent news for a specific company using GNews API."""
        if not self.api_key:
            return self._scrape_google_news(company_name, limit)

        params = {
            "q": company_name,
            "token": self.api_key,
            "lang": "en",
            "country": "in",
            "max": limit
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            return data.get("articles", [])
        except Exception as e:
            return [{"error": f"GNews API failed: {str(e)}"}]

    def _scrape_google_news(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Fallback web scraper for news from Google News (Finance category)."""
        # Improved search query for better relevance to Indian markets
        search_url = f"https://www.google.com/search?q={query}+stock+latest+news+india&tbm=nws"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        try:
            response = requests.get(search_url, headers=headers, timeout=5)
            soup = BeautifulSoup(response.text, "html.parser")
            news_items = []
            
            # Find all news result blocks
            for item in soup.select("div.SoR63b", limit=limit) or soup.select("div.g", limit=limit):
                title_tag = item.find("h3")
                link_tag = item.find("a")
                source_tag = item.find("div", string=True) # Usually the source name is in a div
                
                if title_tag:
                    news_items.append({
                        "title": title_tag.get_text(),
                        "link": link_tag["href"] if link_tag else None,
                        "source": source_tag.get_text() if source_tag else "Google News",
                        "content": "Full content requires API key or direct parsing of source link."
                    })
            
            # Additional fallback if the above selectors fail (Google changes them often)
            if not news_items:
                for item in soup.find_all("h3", limit=limit):
                    news_items.append({
                        "title": item.get_text(),
                        "source": "Google Search",
                        "content": "Title only available in limited scrape."
                    })
                    
            return news_items
        except Exception:
            return []
