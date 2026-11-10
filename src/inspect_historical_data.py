
import csv


def inspect_historical_data(filepath):
    """Check the structure and date coverage of the historical dataset."""

    total_rows = 0
    valid_rows = 0
    missing_scores = 0
    team_names = set()
    earliest_date = None
    latest_date = None

    with open(filepath, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        # Display the column headings found in the source file.
        print("CSV columns:", reader.fieldnames)

        for row in reader:
            total_rows += 1

            match_date = row["date"]
            home_team = row["home_team"].strip()
            away_team = row["away_team"].strip()

            # Record the date range covered by the dataset.
            if earliest_date is None or match_date < earliest_date:
                earliest_date = match_date

            if latest_date is None or match_date > latest_date:
                latest_date = match_date

            # Collect the names of all teams in the dataset.
            team_names.add(home_team)
            team_names.add(away_team)

            # Check whether both match scores are available.
            if row["home_score"] == "" or row["away_score"] == "":
                missing_scores += 1
            else:
                valid_rows += 1

    print("\nDataset inspection")
    print("------------------")
    print("Total records:", total_rows)
    print("Records with scores:", valid_rows)
    print("Records missing scores:", missing_scores)
    print("Unique teams:", len(team_names))
    print("Earliest match:", earliest_date)
    print("Latest match:", latest_date)


if __name__ == "__main__":
    inspect_historical_data("data/historical_results.csv")
