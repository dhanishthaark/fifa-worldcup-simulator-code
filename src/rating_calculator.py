import csv
from pathlib import Path


# Find the project's data folder.
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

TEAM_FILE = DATA_DIR / "32Round_WC2026.csv"
RESULTS_FILE = DATA_DIR / "historicalmatchresults.csv"
OUTPUT_FILE = DATA_DIR / "32Round_WC2026_rated.csv"

INITIAL_RATING = 1500
K_FACTOR = 20

START_DATE = "2022-01-01"
END_DATE = "2026-06-10"


def calculate_expected_score(rating_a, rating_b):
    """Calculate the probability of team A winning using Elo."""
    return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))


def calculate_ratings():
    ratings = {}
    matches_played = {}

    # Handle differences between names in the two CSV files.
    aliases = {
        "Bosnia Herzegovina": "Bosnia and Herzegovina",
        "Cabo Verde": "Cape Verde"
    }

    # Load the 32 selected teams.
    with open(TEAM_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        reader.fieldnames = [
            column.strip() for column in reader.fieldnames
        ]

        teams = []

        for row in reader:
            row = {
                key.strip(): value.strip()
                for key, value in row.items()
                if key is not None
            }

            team_id = row["team_id"]
            team_name = row["team_name"]

            dataset_name = aliases.get(team_name, team_name)

            teams.append({
                "team_id": team_id,
                "team_name": team_name,
                "dataset_name": dataset_name
            })

    # Read the historical match results.
    with open(RESULTS_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        matches = []

        for match in reader:
            date = match["date"]

            if START_DATE <= date <= END_DATE:
                if not match["home_score"] or not match["away_score"]:
                    continue

                matches.append(match)

    # Ensure matches are processed chronologically.
    matches.sort(key=lambda match: match["date"])

    # Process every historical match.
    for match in matches:
        home_team = match["home_team"]
        away_team = match["away_team"]

        home_score = int(match["home_score"])
        away_score = int(match["away_score"])

        # Initialise ratings when a team first appears.
        ratings.setdefault(home_team, INITIAL_RATING)
        ratings.setdefault(away_team, INITIAL_RATING)

        matches_played.setdefault(home_team, 0)
        matches_played.setdefault(away_team, 0)

        home_rating = ratings[home_team]
        away_rating = ratings[away_team]

        # Calculate the expected result.
        expected_home = calculate_expected_score(
            home_rating, away_rating
        )

        # Determine the actual result.
        if home_score > away_score:
            actual_home = 1
        elif home_score < away_score:
            actual_home = 0
        else:
            actual_home = 0.5

        # Calculate the rating change.
        rating_change = K_FACTOR * (
            actual_home - expected_home
        )

        # Update both ratings using the original values.
        ratings[home_team] = home_rating + rating_change
        ratings[away_team] = away_rating - rating_change

        matches_played[home_team] += 1
        matches_played[away_team] += 1

    # Export the ratings for the selected 32 teams.
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        fieldnames = ["team_id", "team_name", "rating"]

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for team in teams:
            name = team["dataset_name"]

            final_rating = ratings.get(name, INITIAL_RATING)

            writer.writerow({
                "team_id": team["team_id"],
                "team_name": team["team_name"],
                "rating": round(final_rating)
            })

            if matches_played.get(name, 0) == 0:
                print(f"Warning: no historical matches found for {name}")

    print(f"Processed {len(matches)} historical matches.")
    print(f"Calculated ratings for {len(teams)} selected teams.")
    print(f"Ratings saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    calculate_ratings()
