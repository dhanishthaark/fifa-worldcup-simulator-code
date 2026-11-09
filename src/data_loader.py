
import csv


def load_teams_csv(filepath):
    """
    Load team data from a CSV file and validate each record.
    Returns a list of team dictionaries if the data is valid.
    """

    required_columns = {"team_id", "team_name", "rating"}

    teams = []
    team_ids = set()
    errors = []

    try:
        # Open the CSV file so that its contents can be read
        with open(filepath, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            # Check that the file contains column headings.
            if reader.fieldnames is None:
                raise ValueError("The CSV file is empty.")

            # Remove accidental spaces from the column headings
            reader.fieldnames = [
                column.strip() for column in reader.fieldnames
            ]

            # Check that all required columns are present
            missing_columns = required_columns - set(reader.fieldnames)

            if missing_columns:
                raise ValueError(
                    f"Missing required columns: {', '.join(sorted(missing_columns))}"
                )

            # Process each team record, starting at row 2
            for row_number, row in enumerate(reader, start=2):

                team_id = (row["team_id"] or "").strip()
                team_name = (row["team_name"] or "").strip()
                rating_text = (row["rating"] or "").strip()

                # Check that the team has an identifier and a name
                if not team_id:
                    errors.append(
                        f"Row {row_number}: team_id is missing."
                    )

                if not team_name:
                    errors.append(
                        f"Row {row_number}: team_name is missing."
                    )

                # Check that each team identifier is unique
                if team_id and team_id in team_ids:
                    errors.append(
                        f"Row {row_number}: duplicate team_id '{team_id}'."
                    )

                # Convert the rating into a number
                try:
                    rating = float(rating_text)
                except ValueError:
                    errors.append(
                        f"Row {row_number}: rating must be numeric."
                    )
                    continue

                # Remember the identifier to detect future duplicates
                if team_id:
                    team_ids.add(team_id)

                # Store the validated team's information
                teams.append({
                    "team_id": team_id,
                    "team_name": team_name,
                    "rating": rating
                })

    except OSError as error:
        raise ValueError(
            f"Could not read CSV file: {error}"
        ) from error

    # Check that the file contains at least one team
    if not teams:
        errors.append(
            "The CSV file contains no valid team records."
        )

    # Reject the file if any validation errors were found
    if errors:
        raise ValueError("\n".join(errors))

    return teams
