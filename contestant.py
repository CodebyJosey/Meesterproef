import datetime
from databasemanagement import DatabaseManagement
import sqlite3


class Contestant:
    def __init__(self, *args) -> None:
        self.database: DatabaseManagement = DatabaseManagement()
        self.connection: sqlite3.Connection = self.database.connection
        self.cursor = sqlite3.Cursor = self.database.cursor

        self.id: str = args[0]
        self.first_name: str = args[1]
        self.last_name: str = args[2]
        self.classification: str = args[3]
        self.date_of_birth: datetime.datetime = args[4]

    def get_age(self, at_date: datetime.date = datetime.date.today()) -> int:
        age: datetime.timedelta = at_date.year - self.date_of_birth.year

        if (at_date.month, at_date.day) < (self.date_of_birth.month, self.date_of_birth.day):
            age -= 1
        return age

    def get_catches(self) -> tuple:
        from catch import Catch
        results: list[tuple] = self.cursor.execute('''SELECT * FROM Catches
                                                   WHERE contestant_id = ?''', (self.id,)).fetchall()
        return tuple(Catch(*result) for result in results)

    def __repr__(self) -> str:
        excluced_keys: list[str] = ['database', 'cursor', 'connection']
        return "{}({})".format(
            type(self).__name__,
            ", ".join([f"{key}={value!s}" for key, value in self.__dict__.items()
                       if not any(key == excluced_key for excluced_key in excluced_keys)]),
        )
