import sqlite3

# Find the movie with the highest budget AND the movie with the highest IMDb rating. 
def calculation_1_budget_vs_rating(conn):
    print("Calculation #1: Highest Budget and Highest IMDb Rating")

    cur = conn.cursor()

    # Join TMDB and OMDB tables together using imdb_id
    cur.execute("""
        SELECT tmdb_movies.title_id, tmdb_movies.budget, omdb_movies.imdb_rating
        FROM tmdb_movies
        JOIN omdb_movies
        ON tmdb_movies.imdb_id = omdb_movies.imdb_id;
    """)

    rows = cur.fetchall()

    # If the join returned nothing, we can't calculate anything
    if not rows:
        print("Not enough data to calculate.")
        return

    # We will save cleaned rows here after converting rating from string to float
    cleaned_rows = []

    # Loop through each row from the JOIN
    for row in rows:
        title_id = row[0]
        budget = row[1]
        rating_value = row[2]

        # IMDb ratings are stored as strings like "6.5" or "N/A"
        # If they cannot convert to float, skip them
        try:
            rating = float(rating_value)
        except:
            continue

        cleaned_rows.append((title_id, budget, rating))

    # If every rating was invalid, we cannot continue
    if not cleaned_rows:
        print("No valid rating data found.")
        return

    # Find the row with the highest budget 
    highest_budget_row = max(cleaned_rows, key=lambda r: r[1])

    # Find the row with the highest rating 
    highest_rating_row = max(cleaned_rows, key=lambda r: r[2])

    # Print results
    print("\nHighest Budget Movie:")
    print(f"  Title ID: {highest_budget_row[0]}")
    print(f"  Budget: ${highest_budget_row[1]:,}")

    print("\nHighest Rated Movie:")
    print(f"  Title ID: {highest_rating_row[0]}")
    print(f"  IMDb Rating: {highest_rating_row[2]}")

    print("\nDone with Calculation #1.\n")



# Calculate the average IMDb rating for each movie genre.
def calculation_2_avg_rating_by_genre(conn):
    print("Calculation #2: Average IMDb Rating by Genre")

    cur = conn.cursor()

    # Get all genres + ratings from OMDB table
    cur.execute("""
        SELECT omdb_movies.genre, omdb_movies.imdb_rating
        FROM omdb_movies;
    """)

    rows = cur.fetchall()

    # If no OMDB data exists, stop early
    if not rows:
        print("No OMDB data found.")
        return

    # genre_totals stores the SUM of ratings for each genre
    genre_totals = {}

    # genre_counts stores how many movies belong to each genre
    genre_counts = {}

    # Loop through all OMDB rows
    for row in rows:
        genre_string = row[0]
        rating_value = row[1]

        # Skip rows missing either genre or rating
        if not genre_string or not rating_value:
            continue

        # Convert rating to float
        # Skip invalid values like "N/A"
        try:
            rating = float(rating_value)
        except:
            continue

        # A movie can have multiple genres, separated by commas
        genres = [g.strip() for g in genre_string.split(",")]

        # Add rating to each genre individually
        for genre in genres:
            if genre not in genre_totals:
                genre_totals[genre] = 0.0
                genre_counts[genre] = 0

            genre_totals[genre] += rating
            genre_counts[genre] += 1

    # Print average rating for each genre
    print("\nAverage IMDb Rating by Genre:")
    for genre in genre_totals:
        avg = genre_totals[genre] / genre_counts[genre]
        print(f"  {genre}: {avg:.2f}")

    print("\nDone with Calculation #2.\n")



def main():
    conn = sqlite3.connect("movies.db")

    calculation_1_budget_vs_rating(conn)
    calculation_2_avg_rating_by_genre(conn)

    conn.close()


if __name__ == "__main__":
    main()
