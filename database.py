import sqlite3
import json

# Create database tables
def init_db(db_name="movies.db"):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    # IMDb keys table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS imdb_keys (
            imdb_id TEXT PRIMARY KEY
        );
    """)

    # Unique titles table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS movie_titles (
            title_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE
        );
    """)

    # TMDB table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tmdb_movies (
            tmdb_id INTEGER PRIMARY KEY,
            imdb_id TEXT,
            title_id INTEGER,
            budget INTEGER,
            FOREIGN KEY (imdb_id) REFERENCES imdb_keys(imdb_id),
            FOREIGN KEY (title_id) REFERENCES movie_titles(title_id)
        );
    """)

    # OMDB table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS omdb_movies (
            omdb_id INTEGER PRIMARY KEY AUTOINCREMENT,
            imdb_id TEXT,
            title_id INTEGER,
            genre TEXT,
            imdb_rating REAL,
            FOREIGN KEY (imdb_id) REFERENCES imdb_keys(imdb_id),
            FOREIGN KEY (title_id) REFERENCES movie_titles(title_id)
        );
    """)

    conn.commit()
    conn.close()


# Insert helpers

def insert_imdb_key(conn, imdb_id):
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO imdb_keys (imdb_id) VALUES (?);", (imdb_id,))
    conn.commit()


def insert_title(conn, title):
    cur = conn.cursor()
    if title:
        title = title.strip().lower()
    else:
        title = "unknown title"
    cur.execute("INSERT OR IGNORE INTO movie_titles (title) VALUES (?);", (title,))
    conn.commit()

    cur.execute("SELECT title_id FROM movie_titles WHERE title = ?;", (title,))
    return cur.fetchone()[0]


# Insert TMDB row

def insert_tmdb_row(conn, movie):
    imdb_id = movie["imdb_id"]
    title = movie["title"]

    insert_imdb_key(conn, imdb_id)
    title_id = insert_title(conn, title)

    cur = conn.cursor()
    cur.execute("""
        INSERT OR REPLACE INTO tmdb_movies (tmdb_id, imdb_id, title_id, budget)
        VALUES (?, ?, ?, ?);
    """, (
        movie["tmdb_id"],
        imdb_id,
        title_id,
        movie["budget"]
    ))
    conn.commit()


# Insert OMDB row

def insert_omdb_row(conn, movie):
    imdb_id = movie["imdb_id"]
    title = movie["title"]

    insert_imdb_key(conn, imdb_id)
    title_id = insert_title(conn, title)

    cur = conn.cursor()
    cur.execute("""
        INSERT INTO omdb_movies (imdb_id, title_id, genre, imdb_rating)
        VALUES (?, ?, ?, ?);
    """, (
        imdb_id,
        title_id,
        movie.get("genre"),
        movie.get("imdb_rating")
    ))
    conn.commit()


# MAIN function for database.py
# Reads JSON files and inserts them
def main():
    init_db()

    conn = sqlite3.connect("movies.db")

    # Load TMDB JSON
    with open("movie.json", "r") as f:
        tmdb_movies = json.load(f)

    # Load OMDB JSON
    with open("omdb_movies.json", "r") as f:
        omdb_movies = json.load(f)

    # # Limit to 25 items per execution
    # tmdb_movies = tmdb_movies[:25]
    # omdb_movies = omdb_movies[:25]

    # Insert TMDB data
    for movie in tmdb_movies:
        insert_tmdb_row(conn, movie)

    # Insert OMDB data
    for movie in omdb_movies:
        insert_omdb_row(conn, movie)

    conn.close()
    print("Database successfully populated.")


if __name__ == "__main__":
    main()

