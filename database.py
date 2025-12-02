import sqlite3
import matplotlib.pyplot as plt

def plot_mentions_vs_budget(db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    rows = cur.execute("""
        SELECT tmdb.budget 
        FROM tmdb 
        JOIN nyt
            ON LOWER(tmdb.title) = LOWER(nyt.movie_title); 
    """).fetchall()

    conn.close()

    low = 0 
    medium = 0 
    high = 0 

    for (budget,) in rows: 
        if budget is None: 
            continue 
        if budget < 20_000_000: 
            low += 1 
        elif 20_000_000 <= budget <= 80_000_000: 
            medium += 1
        else: 
            high += 1 

    categories = ["Low", "Medium", "High"]
    counts = [low, medium, high]

    plt.figure(figsize=(8, 5))
    plt.bar(categories, counts)
    plt.title("NYT Article Mentions by Movie Budget Category")
    plt.xlabel("Budget Category")
    plt.ylabel("Number of NYT Mentions")
    plt.tight_layout()
    plt.savefig("NYT_Mention_vs_Budget.png")
    plt.show()

if __name__ == "__main__":
    plot_mentions_vs_budget(".db")