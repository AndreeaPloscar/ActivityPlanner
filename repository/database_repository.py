from repository.repository import Repository
import sqlite3
from entities.person import Person
from entities.activity import Activity
import datetime


class PersonsDatabaseRepository(Repository):

    def __init__(self):
        super().__init__()
        self.connection = sqlite3.connect('planner.db')
        self.cursor = self.connection.cursor()
        self.__load_data_from_database()

    def __load_data_from_database(self):
        """
        Loads data from the database into the program
        """
        self.cursor.execute("SELECT * FROM persons")
        persons = self.cursor.fetchall()
        id_index = 0
        name_index = 1
        number_index = 2
        for person in persons:
            person_to_add = Person(person[id_index], person[name_index], person[number_index])
            super().save(person_to_add)

    def save(self, entity):
        """
        Saves an entity into self._entities and into the database
        """
        super().save(entity)
        person_id = entity.id
        person_name = entity.name
        person_number = entity.phone_number
        persons = [(person_id, person_name, person_number)]
        self.cursor.executemany("INSERT INTO persons(id,name,phone_number) VALUES(?,?,?)", persons)
        self.connection.commit()

    def delete_by_id(self, entity_id):
        """
        Deletes entity having entity_id as id from self._entities and from the database
        """
        entity = super().delete_by_id(entity_id)
        sql = 'DELETE FROM persons WHERE id = ?'
        self.cursor.execute(sql, (entity_id,))
        sql = 'DELETE FROM enrolment WHERE person_id = ?'
        self.cursor.execute(sql, (entity_id,))
        self.connection.commit()
        return entity

    def update(self, entity_id, entity):
        """
        Updates the entity having entity_id as id with the new entity
        """
        old_entity = super().update(entity_id, entity)
        person_name = entity.name
        person_number = entity.phone_number
        sql_command = "UPDATE persons SET name = ?, phone_number=? WHERE id = ?"
        person = (person_name, person_number, entity_id)
        self.cursor.execute(sql_command, person)
        self.connection.commit()
        return old_entity


class ActivitiesDatabaseRepository(Repository):

    def __init__(self):
        super().__init__()
        self.connection = sqlite3.connect('planner.db')
        self.cursor = self.connection.cursor()
        self.__load_data_from_database()

    def __load_data_from_database(self):
        """
        Loads data from the database into the program
        """
        self.cursor.execute("SELECT * FROM activities")
        activities = self.cursor.fetchall()
        id_index = 0
        date_index = 1
        start_index = 2
        end_index = 3
        description_index = 4
        for activity in activities:
            activity_to_add = Activity(activity[id_index], [], datetime.datetime.strptime(activity[date_index],
                                                                                          "%d/%m/%Y"),
                                       datetime.datetime.strptime(activity[start_index], "%H:%M"),
                                       datetime.datetime.strptime(activity[end_index], "%H:%M"),
                                       activity[description_index])
            super().save(activity_to_add)
        self.cursor.execute("SELECT * FROM enrolment")
        enrolments = self.cursor.fetchall()
        person_index = 0
        activity_index = 1
        for enrolment in enrolments:
            for activity in self._entities:
                if activity.id == enrolment[activity_index]:
                    activity.person_id.append(enrolment[person_index])

    def save(self, entity):
        """
        Saves an entity into self._entities and into the database
        """
        super().save(entity)
        activity_id = entity.id
        activities = [(entity.id, datetime.datetime.strftime(entity.date, "%d/%m/%Y"),
                       datetime.datetime.strftime(entity.start_time, "%H:%M"),
                       datetime.datetime.strftime(entity.end_time, "%H:%M"), entity.description)]
        self.cursor.executemany("INSERT INTO activities(id,date, start_time, end_time, description ) VALUES(?,?,?,?,?)",
                                activities)
        self.connection.commit()
        enrolments = []
        for person in entity.person_id:
            enrolments.append((person, entity.id))
        self.cursor.executemany("INSERT INTO enrolment(person_id, activity_id) VALUES (?,?)", enrolments)
        self.connection.commit()

    def delete_by_id(self, entity_id):
        """
        Deletes entity having entity_id as id from self._entities and from the database
        """
        entity = super().delete_by_id(entity_id)
        sql_command = 'DELETE FROM activities WHERE id = ?'
        self.cursor.execute(sql_command, (entity_id,))
        self.connection.commit()
        sql_command = 'DELETE FROM enrolment WHERE activity_id = ?'
        self.cursor.execute(sql_command, (entity_id,))
        self.connection.commit()
        return entity

    def update(self, entity_id, entity):
        """
        Updates the entity having entity_id as id with the new entity
        """
        old_entity = super().update(entity_id, entity)
        sql_command = "UPDATE activities SET date=?, start_time = ?, end_time=?, description = ? WHERE id = ?"
        activity = (datetime.datetime.strftime(entity.date, "%d/%m/%Y"), datetime.datetime.strftime(entity.start_time,
                                                                                                    "%H:%M"),
                    datetime.datetime.strftime(entity.end_time, "%H:%M"), entity.description, entity_id)
        self.cursor.execute(sql_command, activity)
        sql_command = 'DELETE FROM enrolment WHERE activity_id = ?'
        self.cursor.execute(sql_command, (entity_id,))
        self.connection.commit()
        enrolments = []
        for person in entity.person_id:
            enrolments.append((person, entity.id))
        self.cursor.executemany("INSERT INTO enrolment(person_id, activity_id) VALUES (?,?)", enrolments)
        self.connection.commit()
        return old_entity
