import requests
from datetime import datetime
from bs4 import BeautifulSoup
from langchain.tools import BaseTool
from typing import Dict, List
class Fo4EventScraperTool(BaseTool):
    """Tool to scrape FIFA Online 4 events from the official website."""
    
    name = "Fo4EventScraper"
    description = "Scrapes the latest events from FIFA Online 4 website"
    return_direct = True
    
    def _run(self, *args, **kwargs) -> str:
        """Scrape the FIFA Online 4 website for the latest events."""
        url = "https://fconline.garena.vn/"
        
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract events from the website based on the actual HTML structure
            events_section = soup.find("div", class_="st-news__posts")
            if not events_section:
                return "Could not find events section on the website."
                
            event_items = events_section.find_all("a", class_="st-news__post")
            if not event_items:
                return "No events found on the website."
                
            events = []
            for item in event_items:
                # Extract title
                title_element = item.find("h3", class_="st-news__post--title")
                title = title_element.text.strip() if title_element else "No title"
                
                # Extract date
                date_element = item.find("p", class_="st-news__post--date")
                date = date_element.text.strip() if date_element else "No date"
                
                # Extract description
                desc_element = item.find("div", class_="st-news__post--description")
                description = desc_element.text.strip() if desc_element else "No description"
                
                # Extract link
                link = item.get("href", "#")
                if not link.startswith("http"):
                    link = url + link.lstrip("/")
                
                # Extract image URL
                img_element = item.find("img")
                img_url = img_element.get("src", "") if img_element else ""
                
                events.append({
                    "title": title,
                    "date": date,
                    "description": description,
                    "link": link,
                    "image_url": img_url
                })
                
            return self._format_events(events)
        
        except Exception as e:
            return f"Error scraping FIFA Online 4 website: {str(e)}"
    
    def _format_events(self, events: List[Dict]) -> str:
        """Format the list of events into a readable string."""
        if not events:
            return "No events found."
            
        result = "🎮 FIFA ONLINE 4 - LATEST EVENTS 🎮\n\n"
        for i, event in enumerate(events, 1):
            result += f"{i}. {event['title']}\n"
            result += f"   📅 Date: {event['date']}\n"
            result += f"   📝 Description: {event['description'][:100]}...\n" if len(event['description']) > 100 else f"   📝 Description: {event['description']}\n"
            result += f"   🔗 Link: {event['link']}\n\n"
            
        result += f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        return result
    
    async def _arun(self, *args, **kwargs) -> str:
        """Asynchronous version of _run."""
        return self._run(*args, **kwargs)