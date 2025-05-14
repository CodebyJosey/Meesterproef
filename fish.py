from databasemanagement import DatabaseManagement
import sqlite3


class Fish:
    def __init__(self, *args) -> None:
        self.database: DatabaseManagement = DatabaseManagement()
        self.connection: sqlite3.Connection = self.database.connection
        self.cursor = sqlite3.Cursor = self.database.cursor

        self.taxon_key: int = args[0]
        self.species: str = args[1]
        self.scientific_name: str = args[2]
        self.kingdom: str = args[3]

    def get_catches(self) -> tuple:
        from catch import Catch
        results: list[tuple] = self.cursor.execute('''SELECT * FROM Catches
                                                   WHERE Catches.fish_id = ?''', (self.taxon_key,))
        return tuple(Catch(*result) for result in results)

    def __repr__(self) -> str:
        excluced_keys: list[str] = ['database', 'cursor', 'connection']
        return "{}({})".format(
            type(self).__name__,
            ", ".join([f"{key}={value!s}" for key, value in self.__dict__.items()
                       if not any(key == excluced_key for excluced_key in excluced_keys)]),
        )
