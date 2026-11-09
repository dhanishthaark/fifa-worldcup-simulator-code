
from data_loader import load_teams_csv


def main():
    # loads and validates the team data from data/teams.cv
    try:
        teams = load_teams_csv("data/teams.csv")

        print(f"Successfully loaded {len(teams)} teams.")

        # display each team's info : team_name, team_id and rating
        for team in teams:
            print(
                f"{team['team_id']}: {team['team_name']} "
                f"(Rating: {team['rating']})"
            )

    # this is when functin gets correct type but invorrect value argument. saves error into variable error. prints error message and exact error from variable
    except ValueError as error:
        print(f"Data loading error:\n{error}")


# runs program when this file is executed directly
if __name__ == "__main__":
    main()
