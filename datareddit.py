#GNEWS

#from GoogleNews import GoogleNews
import pandas as pd
from GoogleNews import GoogleNews
#Initialize GoogleNews
googlenews = GoogleNews(lang='en', region='IN', period='365d')  # last 7 days
ipo_list = ["Rubicon Research", "Canara Robeco Asset Management", 
            
            "LG Electronics India", "Mittal Sections", "Tata Capital", 
            "NSB BPO Solutions", "WeWork India Management", "DSM Fresh Foods", 
            "Greenleaf Envirotech", "Infinity Infoway", "Valplast Technologies", 
            "Sunsky Logistics", "Sheel Biotech", "Amanta Healthcare", "Vigor Plast India", 
            "Urban Company", "Shringar House of Mangalsutra", "Galaxy Medicare", "TechD Cybersecurity", 
            "Euro Pratik Sales", "JSW Cement", "All Time Plastics", "Bluestone Jewellery & Lifestyle", 
            "Regaal Resources", "Vikram Solar", "Patel Retail", "Gem Aromatics", "Shreeji Shipping Global", 
            "Mangal Electrical Industries", "Current Infraprojects", "Sattva Engineering Construction", 
            "Vikran Engineering", "Anlon Healthcare", "Snehaa Organics"]

all_news = []

for ipo in ipo_list:
    googlenews.clear()
    googlenews.search(ipo)
    results = googlenews.result()

    for r in results:
        all_news.append({
            'source': 'GoogleNews',
            'ipo_name': ipo,
            'title': r.get('title'),
            'media': r.get('media'),
            'date': r.get('date'),
            'desc': r.get('desc'),
            'link': r.get('link')
        })

#Save to CSV
df = pd.DataFrame(all_news)
df.to_csv('data/news1_data.csv', index=False)
print("✅ Collected", len(df), "news articles.")
df.head()