from tinydb import TinyDB
from .match import Match


class Round:
    """
    Rounds Objects are structured with Matches objects inside.
    With the data_base, those objects need to be serialized.
    There are the steps that manipulate an instance :

        1. Initialize
    Round instance is created
        2. Update
    Round instance is pasted in a dictionary, for save purpose. ( dictionary : *rounds*)
        3. Serialize
    Round instance is serialized in another dictionary, but this time, the objects inside the instance are also
    serialized.
        4. Ready to Work
    Round instance is ready to be manipulate. When the program is launch, the serials are called from the
    data_base and transformed into objects.
    """

    rounds = {}
    serialized_rounds = {}
    data_base = TinyDB("data_base.json")
    rounds_table = data_base.table("rounds")
    serialized_rounds = rounds_table.all()[0] if rounds_table else {}
    """
    Class parameters:
        * *rounds* (dict): Keep all rounds in a dictionary, allow them to be used away
        * *serialized_rounds* (dict): Serials from all rounds attributes, ready to be convert into objects.
        * *data_base* (list): TinyDB list where serials are saved.
        * *rounds_table* (list): Specific TinyDB data_base region where serialized rounds are saved.
    """

    def __init__(self,
                 id_round: str,
                 name_round: str,
                 begin_time: str,
                 end_time: str,
                 **kwargs):
        """
        Initialize a round.

        Args:
            * *id_round* (str): ID of the round, composed as "<ID_tournament>:<ID_round>". e.g: "1:1"
            * *name_round* (str): Name of round
            * *begin_time* (str): The time when the round started
            * *end_time* (str): The time when round must end

        Keyword Arg:
            * *matches* (list): List of matches objects.
        """
        self.id_round = id_round
        self.name_round = name_round
        self.begin_time = begin_time
        self.end_time = end_time

        self.matches = kwargs["matches"] if len(kwargs) > 0 else []

        self.update()

    def __str__(self):
        """
        Describe the match like this:
            >> print(round)
            ID : 1:1 - Name : Round 1
            Time : 13:10:05 until 13:30:05
            *Matches* -see Match __str__ for more information.
        """
        newline = "\n"
        return f"\033[1m{self.name_round} - ID : {self.id_round}\033[0m \n" \
               f"Time : {self.begin_time} until {self.end_time}\n" \
               f"{newline.join(map(str, self.matches))}"

    def update(self):
        """
        The update function save the attributes of an instance in the class attribute : *rounds*.

        Steps:
            1. Make a dictionary with all attributes of the instance.
            2. Add this dictionary to the *rounds* dictionary at the key: *self.id_round*.
        """
        round_dict = {key: value for key, value in vars(self).items()}
        if self.id_round in self.rounds.keys():
            self.rounds[self.id_round].update(round_dict)
        else:
            self.rounds[self.id_round] = round_dict

        self.serialize()

    def serialize(self):
        """
        Convert the serialized tournaments to objects.
        """
        serial_id_round = self.id_round
        serial_name_round = self.name_round
        serial_begin_time = self.begin_time
        serial_end_time = self.end_time

        serial_matches = Match.get_from_round(self.id_round)

        serial_round = {'id_round': serial_id_round,
                        'name_round': serial_name_round,
                        'begin_time': serial_begin_time,
                        'end_time': serial_end_time,
                        'matches': serial_matches
                        }
        self.serialized_rounds[self.id_round] = serial_round
        self.rounds_table.truncate()
        self.rounds_table.insert(self.serialized_rounds)

    def set_matches(self, matches):
        """
        Set the *matches* attribute with list of Match objects.

        Arg:
            * *matches* (list): List of matches objects.
        """
        self.matches = matches
        self.update()

    @classmethod
    def get(cls, id_round):
        """
        Get a specific Round giving its unique ID.

        Arg:
            * *id_round* (str): Unique ID of a round. i.e: "1:1"
        """
        db_round = cls.rounds.get(id_round)
        if db_round:
            single_round = Round(**db_round)
            return single_round
        return False

    @classmethod
    def get_serialized_from_tournament(cls, id_tournament):
        """
        Get all serialized rounds from a specific tournament.

        Arg:
            * *id_tournament* (str): ID of the tournament. i.e: "1"
        """
        list_round = []
        for id_round, db_round in cls.serialized_rounds.items():
            if id_tournament == db_round["id_round"].split(":")[0]:
                list_round.append(db_round)
        return list_round

    @classmethod
    def get_all_from_tournament(cls, id_tournament):
        """
        Get all rounds of a specific tournament.

        Arg:
            * *id_tournament* (str): ID of the tournament. i.e: "1"
        """
        list_rounds = []
        for id_round, db_round in cls.rounds.items():
            if id_tournament == id_round.split(":")[0]:
                single_round = Round(**db_round)
                list_rounds.append(single_round)
        return list_rounds

    @classmethod
    def deserialize_all(cls):
        """
        Deserialize all rounds.

        Steps :
            1. Get all matches from a round
            2. Compose round with its own attributes and matches
        """
        list_all_matches = Match.deserialize_all()
        list_rounds = []
        for id_round, db_round in cls.serialized_rounds.items():
            list_matches = []
            for match in list_all_matches:
                id_tournament_match = match.id_match.split(":")[0]
                id_round_match = match.id_match.split(":")[1]
                if id_round == f"{id_tournament_match}:{id_round_match}":
                    list_matches.append(match)
            kwargs = {"matches": list_matches}
            single_round = Round(db_round["id_round"],
                                 db_round["name_round"],
                                 db_round["begin_time"],
                                 db_round["end_time"],
                                 **kwargs)
            list_rounds.append(single_round)
        return list_rounds
