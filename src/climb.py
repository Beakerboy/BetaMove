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
        self._holds = []

        # The grade
        # The JSON object has three grades; grade, info[2] and UserGrade
        self._grade = ""

        self._start_holds = 0
        self._finish_holds = 0

    # Setters and Getters
    def set_id(self: T, id: str) -> None:
        if re.match("[1-9][0-9]*", id) != id:
            raise Exception("Incorrect id format")
        self._id = id

    def set_name(self: T, name: str) -> None:
        self._name = name

    def add_hold(self: T, hold: list) -> None:
        if hold[1] and self._start_holds == 2:
            raise Exception("Too many start holds")
        if hold[1] and int(hold[0][1:]) > 6:
            raise Exception("Start Hold must be in lower 6 rows") 
        if hold[2] and self._finish_holds == 2:
            raise Exception("Too many finish holds")
        if hold[2] and int(hold[0][1:]) < 18:
            raise Exception("Finish hold must be on top row (18). Hold is on row " + hold[0][1:]) 
        if len(self._holds) > 14:
            raise Exception("Too many holds")
        # Mini Moonboard will need different criteria
        if re.match("[A-K]([1-9]|([1][0-8]))", hold[0]) != hold[0]:
            raise Exception("Incorrect location format. Value is " + hold[0])
        self._holds.append(hold)
        if (hold[1]):
            self._start_holds += 1
        if (hold[2]):
            self._finish_holds += 1

    def set_grade(self: T, grade: str) -> None:
        self._grade = grade
        # Validate acceptible values

    def url(self: T) -> str:
        url = "https://moonboard.com/Problems/View/"
        return url + self._id + "/" + self._name.lower()
        
    @classmethod
    def from_json(cls: Type[T], id: int, data: dict) -> T:
        # parse data and set attributes
        climb = cls()
        climb._id = id
        climb._name = data["problem_name"]
        climb._grade = data["grade"]
        for hold in data["moves"]:
            climb.add_hold(
                [
                    hold["Description"],
                    hold["IsStart"],
                    hold["IsEnd"]
                ]
            )
        return climb
