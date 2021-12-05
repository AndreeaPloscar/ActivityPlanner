from repository.database_repository import PersonsDatabaseRepository, ActivitiesDatabaseRepository
from repository.repository import Repository
from repository.txt_file_repository import TxtPersonFileRepository
from repository.txt_file_repository import TxtActivityFileRepository
from repository.binary_file_repository import BinaryFileRepository
from repository.json_file_repository import JsonPersonFileRepository
from repository.json_file_repository import JsonActivityFileRepository
from console.gui import GUI
from console.ui import UI
from service.person_service import PersonService
from service.activity_service import ActivityService
from service.undo_service import UndoService
from entities.settings import Settings
from validators.validators import PersonValidator
from validators.validators import ActivityValidator


# import sqlite3
# #
# connection = sqlite3.connect('planner.db')
# cursor = connection.cursor()

# cursor.execute("""CREATE TABLE persons (
#             id text,
#             name text,
#             phone_number text
#             )""")
# persons = [('122','Ellie','0741274677'), ('120','Jules','0751274477'), ('123','Olaf','0781279470'),
#             ('124','Name','0987654321'), ('125','name','0987654321')]
# cursor.executemany("INSERT INTO persons(id,name,phone_number) VALUES(?,?,?)", persons)

# cursor.execute("""CREATE TABLE activities (
#             id text,
#             date text,
#             start_time text,
#             end_time text,
#             description text
#             )""")
# activities = [('2','01/12/2021','11:00','12:00','Test Activity2'),
#               ('3','12/12/2020','17:00','18:00','Test Activity3'),
#               ('4','10/06/2021','10:00','12:00','Test Activity4'),
#             ('5','09/07/2020','19:00','20:00','Test Activity5'),
#             ('1','12/12/2020','14:00','16:00','Test Activity1'),
#                 ]
#
#
# print(cursor.fetchall())
# cursor.executemany("INSERT INTO activities(id,date,start_time,end_time,description) VALUES(?,?,?,?,?)", activities)
#
# # cursor.execute("""CREATE TABLE enrolment(
# #             person_id text,
# #             activity_id text
# #             )""")
# enrolments = [('120', '1'), ('122', '1'), ('123', '2'), ('123', '3')]
# cursor.executemany("INSERT INTO enrolment(person_id, activity_id) VALUES(?,?)", enrolments)
# connection.commit()
#
# connection.close()

settings = Settings("", "", "", "")
property_index = 0
setting_index = 1
with open("settings.properties", "r") as settings_file:
    for line in settings_file:
        line = line.split("=")
        if line[property_index].strip() == "repository":
            settings.repository = line[setting_index].strip()
        if line[property_index].strip() == "persons":
            settings.persons = line[setting_index].strip()
        if line[property_index].strip() == "activities":
            settings.activities = line[setting_index].strip()
        if line[property_index].strip() == "ui":
            settings.ui = line[setting_index].strip()

if settings.repository == "txt":
    person_repository = TxtPersonFileRepository(settings.persons)
    activity_repository = TxtActivityFileRepository(settings.activities)
elif settings.repository == "binary":
    person_repository = BinaryFileRepository(settings.persons)
    activity_repository = BinaryFileRepository(settings.activities)
elif settings.repository == "json":
    person_repository = JsonPersonFileRepository(settings.persons)
    activity_repository = JsonActivityFileRepository(settings.activities)
elif settings.repository == "database":
    person_repository = PersonsDatabaseRepository()
    activity_repository = ActivitiesDatabaseRepository()
else:
    person_repository = Repository()
    activity_repository = Repository()

person_validator = PersonValidator()
activity_validator = ActivityValidator()
undo_service = UndoService()
activity_service = ActivityService(undo_service, activity_repository, activity_validator)
person_service = PersonService(undo_service, person_repository, person_validator, activity_service)
if settings.ui == "gui":
    console = GUI(activity_service, person_service, undo_service)
else:
    console = UI(activity_service, person_service, undo_service)

console.run()
