import csv


def load_teams_csv(filepath):
    """Load and validate team data from a CSV file."""

    required_columns = {"team_id", "team_name", "rating"}
    teams = []
    team_ids = set()
    errors = []

    try:
        with open(filepath, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            # Check that all required columns exist.
            if reader.fieldnames is None:
                raise ValueError("The CSV file is empty.")

            missing_columns = required_columns - set(reader.fieldnames)

            if missing_columns:
                raise ValueError(
                    f"Missing required columns: {', '.join(sorted(missing_columns))}"
                )

            for row_number, row in enumerate(reader, start=2):
                team_id = (row["team_id"] or "").strip()
                team_name = (row["team_name"] or "").strip()
                rating_text = (row["rating"] or "").strip()

                # Validate the team's identifier and name.
                if not team_id:
                    errors.append(f"Row {row_number}: team_id is missing.")

                if not team_name:
                    errors.append(f"Row {row_number}: team_name is missing.")

                if team_id and team_id in team_ids:
                    errors.append(
                        f"Row {row_number}: duplicate team_id '{team_id}'."
                    )

                # Validate the rating.
                try:
                    rating = float(rating_text)
                except ValueError:
                    errors.append(
                        f"Row {row_number}: rating must be numeric."
                    )
                    continue

                if team_id:
                    team_ids.add(team_id)

                teams.append({
                    "team_id": team_id,
                    "team_name": team_name,
                    "rating": rating
                })

    except OSError as error:
        raise ValueError(f"Could not read CSV file: {error}") from error

    if not teams:
        errors.append("The CSV file contains no valid team records.")

    if errors:
        raise ValueError("\n".join(errors))

    return teams
