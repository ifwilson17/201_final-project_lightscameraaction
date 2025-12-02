import requests
import json
import my_key

def get_nyt_movie_articles(movie_title):
    url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    
    params = {
        "q": movie_title, 
        "api-key": my_key.API_KEY,

    }

    headers = {
        "User-Agent": "SI201-finalproject", 
        "Accept": "application/json"
    }

    response = requests.get(url, params=params, headers=headers)
    print("STATUS", response.status_code)

    if response.status_code != 200: 
        print("Request failed")
        return []
    
    data = response.json()
    docs = data.get("response", {}).get("docs", [])

    if not docs:
        print("No articles found for:", movie_title)
        return []

    results = []

    for d in docs[:1]: 
        article = {
            "movie_title": movie_title, 
            "headline": d.get("headline", {}).get("main", "No headline"),
            "summary": d.get("abstract", "No summary"), 
            "section": d.get("section_name"), 
            "byline": d.get("byline", {}).get("original"),
            "date": d.get("pub_date")
        }

        results.append(article)


    with open("articles.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
    print(f"Saved {len(article)} articles to articles.json")

    return results 


# if __name__ == "__main__":
#     print(get_nyt_movie_articles("Shrek"))
#     print(get_nyt_movie_articles("Barbie"))