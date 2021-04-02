from app.Controllers import Controller


def start():
    """
    It allows user to give short instructions.
    Look at the controller.py to look at these instructions.
    """
    commands = {"new tournament": Controller.new_tournament,
                "new round": Controller.new_round,
                "new player": Controller.new_player,

                "set round": Controller.set_round,
                "set player": Controller.set_player,

                "get players -all -alpha": Controller.get_all_players_alpha,
                "get players -all -rank": Controller.get_all_players_rank,
                "get players -alpha": Controller.get_players_alpha,
                "get players -rank": Controller.get_players_rank,

                "get tournament -all": Controller.get_all_tournaments,
                "get tournament": Controller.get_tournament,

                "get round -all": Controller.get_all_rounds,
                "get round": Controller.get_round,

                "get match -all": Controller.get_all_matches,
                "get match": Controller.get_match,

                "load": Controller.load,

                "get flake-report": Controller.get_flake_report,
                "commands": Controller.list_commands,
                "exit": Controller.close_app
                }

    # At the beginning of the program, load all data from a data_base.
    Controller.load()
    print("Need help? Type 'commands' to see all commands and there purposes.")

    while True:
        instruction = str(input("ChessManager >>> "))
        try:
            commands[instruction]()
        except KeyError:
            print("Wrong Command.")
