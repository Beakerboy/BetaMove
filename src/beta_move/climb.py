import re
from typing import TypeVar, Type


T = TypeVar('T', bound='Climb')


class Climb:

    # class default constructor
    def __init__(self: T) -> None:

        # Instance Attributes
        # The moonboard ID
        self._id = "0"

        # The problem name
        self._name = ""

        # The list of allowed holds with start and end
        self._holds: dict[tuple, tuple] = {}
        self._start_holds: list[tuple] = []
        self._mid_holds: list[tuple] = []
        self._end_holds: list[tuple] = []

        # The grade
        # The JSON object has three grades; grade, info[2] and UserGrade
        self._grade: str = ""

    # Setters and Getters
    def set_id(self: T, id: str) -> None:
        _rex = re.compile("[1-9][0-9]*")
        if not _rex.fullmatch(id):
            raise Exception("Incorrect id format")
        self._id = id

    def set_name(self: T, name: str) -> None:
        self._name = name

    def get_name(self: T) -> str:
        return self._name

    def add_hold(self: T, hold: tuple) -> None:
        if hold[1] and len(self._start_holds) == 2:
            raise Exception("Too many start holds")
        if hold[1] and int(hold[0][1:]) > 6:
            raise Exception("Start Hold must be in lower 6 rows")
        if hold[2] and len(self._end_holds) == 2:
            raise Exception("Too many finish holds")
        if hold[2] and int(hold[0][1:]) < 18:
            msg = "Finish hold must be on top row (18). Hold is on row "
            raise Exception(msg + hold[0][1:])
        if self.num_holds() == 14:
            raise Exception("Too many holds. id " + self._id)
        # Mini Moonboard will need different criteria
        _rex = re.compile("[A-K]([1-9]|(1[0-8]))")
        if not _rex.fullmatch(hold[0]):
            raise Exception("Incorrect location format. Value is " + hold[0])
        # Check if hold is already in list
        x_value = ord(hold[0][0]) - ord("A")
        y_value = int(hold[0][1:]) - 1
        if (x_value, y_value) in self._holds:
            raise Exception("A hold at list location already exists.")
        if (hold[1]):
            self._start_holds.append((x_value, y_value))
        elif (hold[2]):
            self._end_holds.append((x_value, y_value))
        else:
            self._mid_holds.append((x_value, y_value))
        self._holds[x_value, y_value] = hold

    def get_holds(self: T) -> list:
        self._start_holds.sort(key=lambda x: x[1])
        self._mid_holds.sort(key=lambda x: x[1])
        self._end_holds.sort(key=lambda x: x[1])
        return self._start_holds + self._mid_holds + self._end_holds

    def get_hold(self: T, location: tuple) -> tuple:
        return self._holds[location]

    def set_grade(self: T, grade: str) -> None:
        self._grade = grade
        # Validate acceptible values

    def url(self: T) -> str:
        url = "https://moonboard.com/Problems/View/"
        return url + self._id + "/" + self._name.lower()

    def num_holds(self: T) -> int:
        return (len(self._start_holds)
                + len(self._mid_holds)
                + len(self._end_holds))

    def num_starts(self: T) -> int:
        return len(self._start_holds)

    def num_finish(self: T) -> int:
        return len(self._end_holds)

    def is_valid(self: T) -> bool:
        """
        Verify that the climb meets the minimum expectations.
        Has at least one start, one end, and one other hold.
        """
        return (len(self._mid_holds) > 0
                and self.num_starts() > 0
                and self.num_finish() > 0)

    @classmethod
    def from_json(cls: Type[T], id: str, data: dict) -> T:
        # parse data and set attributes
        climb = cls()
        climb.set_id(id)
        climb.set_name(data["problem_name"])
        climb.set_grade(data["grade"])
        for hold in data["moves"]:
            climb.add_hold(
                (
                    hold["Description"],
                    hold["IsStart"],
                    hold["IsEnd"]
                )
            )
        return climb

    @classmethod
    def from_old_json(cls: Type[T], id: str, data: dict) -> T:
        # parse data and set attributes from the old json format
        climb = cls()
        climb.set_id(id)
        url = data["url"]
        index = url.rindex('/')
        climb.set_name(url[index + 1:])
        climb.set_grade(data["grade"])
        for hold in data["start"]:
            climb.add_hold(
                (
                    chr(int(hold[0]) + ord('A')) + str(hold[1] + 1),
                    True,
                    False
                )
            )
        for hold in data["mid"]:
            climb.add_hold(
                (
                    chr(int(hold[0]) + ord('A')) + str(hold[1] + 1),
                    False,
                    False
                )
            )
        for hold in data["end"]:
            climb.add_hold(
                (
                    chr(int(hold[0]) + ord('A')) + str(hold[1] + 1),
                    False,
                    True
                )
            )
        return climb
