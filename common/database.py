import sqlite3
import random
from string import ascii_letters, digits

class AbstractDatabaseTable():
    """ Abstract Class for SQLite3 Tables """
    def __init__(self):
        self._conn = sqlite3.connect("data/photowall.db", check_same_thread=False)

class PeopleTable(AbstractDatabaseTable):
    """
        SQLite3 Abstraction Layer for the People Table
    """
    TABLE_NAME = "people"
    CHARACTERS = ascii_letters + digits

    def __init__(self):
        super().__init__()
        self._ensure_table()

    def _ensure_table(self):
        """ Ensures that the People table exists """
        sql = """
            CREATE TABLE IF NOT EXISTS {table_name} (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                fun_fact TEXT,
                tribe TEXT NOT NULL
            )
        """.format(table_name=self.TABLE_NAME)
        cursor = self._conn.cursor()
        cursor.execute(sql)
        cursor.close()

    def add_person(self, name, fun_fact, tribe):
        """ Inserts a new Person into the db """
        person_id = self._generate_id()
        sql = """
            INSERT INTO {table_name} (id, name, fun_fact, tribe) VALUES (?, ?, ?, ?)
        """.format(table_name=self.TABLE_NAME)
        cursor = self._conn.cursor()
        cursor.execute(sql, (person_id, name, fun_fact, tribe,))
        was_successful = cursor.rowcount == 1
        cursor.close()
        self._conn.commit()
        return was_successful, person_id

    def get_person_by_id(self, person_id):
        """ Looks up a Person with an ID """
        sql = """
            SELECT id, name, fun_fact, tribe FROM {table_name} WHERE id = ?
        """.format(table_name=self.TABLE_NAME)
        cursor = self._conn.cursor()
        cursor.execute(sql, (person_id,))
        person = cursor.fetchone()
        cursor.close()
        return self._tupleToDict(person) if person else None

    def _generate_id(self):
        """ Generates a unique random ID """
        person_id = "".join(random.choice(self.CHARACTERS) for _ in range(10))
        exists = self.get_person_by_id(person_id)
        if exists:
            return self._generate_id()
        return person_id

    def get_people(self, limit=-1, tribe=None, name=None):
        """
            Returns a list of people from the database,
            matching against a list of criteria.
        """
        # Loose Match Name and Tribe
        tribe = "%{}%".format(tribe.replace(" ", "%")) if tribe else "%"
        name = "%{}%".format(name.replace(" ", "%")) if name else "%"

        sql = """
            SELECT * FROM {table_name} WHERE tribe LIKE ? AND name LIKE ? LIMIT ?
        """.format(table_name=self.TABLE_NAME)
        cursor = self._conn.cursor()
        cursor.execute(sql, (tribe, name, limit,))
        results = cursor.fetchall()
        return self._tupleToDict(results, array=True)

    def delete_person_by_id(self, person_id):
        """
        Deletes Person entry from DB
        """
        sql = """
            DELETE FROM {table_name} WHERE id = ?
        """.format(table_name=self.TABLE_NAME)
        cursor = self._conn.cursor()
        cursor.execute(sql, (person_id,))
        success = cursor.rowcount == 1
        cursor.close()
        self._conn.commit()
        return success

    @staticmethod
    def _tupleToDict(results, array=False):
        def process(result):
            id, name, fun_fact, tribe = result
            return {
                "id": id,
                "name": name,
                "fun_fact": fun_fact,
                "tribe": tribe
            }
        if array:
            dict_array = []
            for result in results:
                dict_array.append(process(result))
            return dict_array
        else:
            return process(results)
