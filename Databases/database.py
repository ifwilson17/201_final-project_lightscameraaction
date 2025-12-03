import sqlite3
import matplotlib.pyplot as plt

def create_tmdb_table():
    # Connect to the SQLite database (creates the file if it doesn't exist)
    conn = sqlite3.connect("movies.db")
    cur = conn.cursor()

    # Create the TMDB table if it does not already exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tmdb_movies (
            tmdb_id INTEGER PRIMARY KEY,
            title TEXT,
            imdb_id TEXT,
            budget INTEGER
        );
    """)

    # Save changes and close connection
    conn.commit()
    conn.close()



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

def main():
    create_tmdb_table()
if __name__ == "__main__":
    main()
    plot_mentions_vs_budget(".db")