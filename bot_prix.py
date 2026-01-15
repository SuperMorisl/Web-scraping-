import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

def scrape_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() 
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        items = soup.find_all(class_="country")

        for item in items:
            name = item.find(class_="country-name")
            capital = item.find(class_="country-capital")
            
            results.append({
                "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Name": name.get_text(strip=True) if name else "N/A",
                "Capital": capital.get_text(strip=True) if capital else "N/A"
            })
        
        return results

    except Exception as e:
        print(f"Error during scraping: {e}")
        return []

if __name__ == "__main__":
    url = "https://www.scrapethissite.com/pages/simple/"
    data = scrape_data(url)
    
    if data:
        df = pd.DataFrame(data)
        df.to_excel("market_research_report.xlsx", index=False)
        print(f"Successfully exported {len(data)} rows to Excel.")