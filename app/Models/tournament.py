from tinydb import TinyDB
from .player import Player
from .match import Match
from .round import Round


class Tournament:
    """
    Tournaments Objects are structured with many objects inside.
    With the data_base, those objects need to be serialized.
    There are the steps that manipulate an instance :

        1. Initialize
    Tournament instance is created
        2. Update
    Tournament instance is pasted in a dictionary, for save purpose. ( dictionary : *tournaments*)
        3. Serialize
    Tournament instance is serialized in another dictionary, but this time, the objects inside the instance are also
    serialized.
        4. Ready to Work
    Tournament instance is ready to be manipulate. When the program is launch, the serials are called from the
    data_base and transformed into objects.
    """

    tournaments = {}
    serialized_tournaments = {}
    data_base = TinyDB("data_base.json")
    tournaments_table = data_base.table("tournaments")
    serialized_tournaments = tournaments_table.all()[0] if tournaments_table else {}
    """
    Class parameters:
        * *tournaments* (dict): Keep all tournaments in a dictionary, allow them to be used away
        * *serialized_tournaments* (dict): Serials from all tournaments attributes, ready to be convert into objects.
        * *data_base* (list): TinyDB list where serials are saved.
        * *tournaments_table* (list): Specific TinyDB data_base region where serialized tournaments are saved.
    """

    def __init__(self,
                 id_tournament: str,
                 name_tournament: str,
                 place: str,
                 date: str,
                 number_players: int,
                 number_rounds: int,
                 time_control: int,
                 description: str,
                 **kwargs):
        """
        Initialize a tournament object then save it to the class attribute : *tournaments*.

        Args:
            * *id_tournament* (str): ID of tournament.
            * *name_tournament* (str): Name of tournament.
            * *place* (str): Where the tournament is played.
            * *date* (str): Date(s) when tournament is played.
            * *number_players* (int): Number of players for this tournament.
            * *number_rounds* (int): Number of round for this tournament.
            * *time_control* (int): Duration of rounds for this tournament.
            * *description* (str): Description of tournament.

        Keyword Args:
            * *players* (list): List of Player OBJECTS.
            * *rounds* (list): List of Round OBJECTS.
            * *tournament_open* (bool): Current state of tournament.
        """
        # Arguments:
        self.id_tournament = str(id_tournament)
        self.name_tournament = str(name_tournament)
        self.place = str(place)
        self.date = str(date)
        self.number_players = int(number_players)
        self.number_rounds = int(number_rounds)
        self.time_control = int(time_control)
        self.description = str(description)

        # Keyword Arguments:
        self.players = kwargs["players"] if len(kwargs) > 0 else False
        self.rounds = kwargs["rounds"] if len(kwargs) > 1 else []
        self.tournament_open = kwargs["tournament_open"] if len(kwargs) > 2 else True

        # Update:
        self.update()

    def __str__(self):
        """
        The printable representation of the object will be like :
            >> print(tournament)
            ID : 15 , Name : Tournament 15
            Place : Stanford
            Date(s) : 15/03/2021 - 16/03/2021
            nb. players : 8
            nb. rounds : 4
            Duration of matches : 20 minutes
            Description :
                Description of the tournament.
            *list of players*
            *list of rounds*
            Tournament open : True
        """
        newline = "\n"
        return f"\033[1m{self.name_tournament}\033[0m - " \
               f"\033[1mID :\033[0m {self.id_tournament} \n" \
               f"\00[1mPlace :\033[0m {self.place}\n" \
               f"\033[1mDate(s) :\033[0m {self.date}\n" \
               f"\033[1mnb. players :\033[0m {self.number_players}\n" \
               f"\033[1mnb. rounds :\033[0m {self.number_rounds}\n" \
               f"\033[1mDuration of matches :\033[0m {self.time_control} minutes\n" \
               f"\033[1mDescription :\033[0m \n\t{self.description}\n" \
               f"\033[1mPlayers :\033[0m\n" \
               f"{newline.join(map(str, self.players))}\n" \
               f"\033[1mRounds :\033[0m\n" \
               f"{newline.join(map(str, self.rounds))}" \
               f"\033[1mTournament open :\033[0m {self.tournament_open}"

    def update(self):
        """
        The update function save the attributes of an instance in the class attribute : *tournaments*.

        Process:
            1. Make a dictionary with all attributes of the instance.
            2. Add this dictionary to the *tournaments* dictionary at the key: *self.id_tournament*.
        """
        tournament_dict = {key: value for key, value in vars(self).items()}
        if self.id_tournament in self.tournaments:
            self.tournaments[self.id_tournament].update(tournament_dict)
        else:
            self.tournaments[self.id_tournament] = tournament_dict
        self.serialize()

    @staticmethod
    def load_from_db():
        """
        Load every serialized tournament from the *data_base.json* database to *tournaments* dictionary.
        Required at the start of the program.
        """
        # 1. Deserialize all players
        Player.get_all()
        # 2. Deserialize all tournaments
        #   2.1 Deserialize Matches
        Match.deserialize_all()
        #   2.2 Deserialize Rounds
        Round.deserialize_all()
        #   2.3 Deserialize Tournaments
        Tournament.deserialize_all()

    def serialize(self):
        """
        Convert the objects to serialized tournaments.
        """
        serial_id_tournament = self.id_tournament
        serial_name_tournament = self.name_tournament
        serial_place = self.place
        serial_date = self.date
        serial_number_players = self.number_players
        serial_number_rounds = self.number_rounds
        serial_time_control = self.time_control
        serial_description = self.description

        serialized_players = Player.get_serialized_from_tournament(self.id_tournament)
        serialized_rounds = Round.get_serialized_from_tournament(self.id_tournament)
        serial_open = self.tournament_open

        serial_tournament = {'id_tournament': serial_id_tournament,
                             'name_tournament': serial_name_tournament,
                             'place': serial_place,
                             'date': serial_date,
                             'number_players': serial_number_players,
                             'number_rounds': serial_number_rounds,
                             'time_control': serial_time_control,
                             'description': serial_description,
                             'players': serialized_players,
                             'rounds': serialized_rounds,
                             'tournament_open': serial_open
                             }
        self.serialized_tournaments[self.id_tournament] = serial_tournament
        self.tournaments_table.truncate()
        self.tournaments_table.insert(self.serialized_tournaments)

    def set_players(self, players):
        """
        Set the players participate to the tournament.

        Arg:
            * *players* (list): List of Player's (objects)
        """
        self.players = players
        self.update()

    def add_round(self, single_round):
        """
        Add a round to the tournament.

        Arg:
            * *single_round* (object): Round object.
        """
        self.rounds.append(single_round)
        self.update()

    def set_tournament_finished(self):
        """
        Set the state of the tournament finished.
        """
        self.tournament_open = False
        self.update()

    @classmethod
    def get(cls, id_got: str):
        """
        Get a specific tournament regarding its <id_tournament>.

        Arg:
            * *id_got* (str): ID of the tournament we want to get.

        Returns:
            If the tournament exists, return the tournament object.
            Else, return False.
        """
        db_tournament = cls.tournaments.get(id_got)
        if db_tournament:
            tournament = Tournament(**db_tournament)
            return tournament
        return False

    @classmethod
    def get_all(cls):
        """
        Get all tournaments created.

        Return:
            Return list of all tournaments
        """
        list_tournament = []
        for id_got, db_tournament in cls.tournaments.items():
            tournament = Tournament(**db_tournament)
            list_tournament.append(tournament)
        return list_tournament

    @classmethod
    def deserialize_all(cls):
        """
        Deserialize all tournaments.

        Steps:
            1. Get all players from a tournament
            2. Get all rounds from a tournament
            3. Compose a tournament with his own attributes, players and rounds.
        """
        for id_tournament, db_tournament in cls.serialized_tournaments.items():
            list_rounds = []
            players_tournament = []
            for player in Player.get_all():
                if id_tournament in player.tournaments_played:
                    players_tournament.append(player)

            for single_round in Round.deserialize_all():
                if id_tournament == single_round.id_round.split(":")[0]:
                    list_rounds.append(single_round)

            kwargs = {"players": players_tournament,
                      "rounds": list_rounds,
                      "tournament_open": db_tournament["tournament_open"]
                      }

            Tournament(db_tournament["id_tournament"],
                       db_tournament["name_tournament"],
                       db_tournament["place"],
                       db_tournament["date"],
                       db_tournament["number_players"],
                       db_tournament["number_rounds"],
                       db_tournament["time_control"],
                       db_tournament["description"],
                       **kwargs)
