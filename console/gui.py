from tkinter import *
from tkinter import ttk
from validators.validators import PersonValidatorException
from validators.validators import RepositoryException
from validators.validators import ActivityValidatorException


class GUI:
    def __init__(self, activity_service, person_service, undo_service):
        self.__activity_service = activity_service
        self.__person_service = person_service
        self.__undo_service = undo_service
        self.root = Tk()
        self.frame_activities = LabelFrame(self.root, text="Activities", padx=5, pady=5)
        self.wrapper = LabelFrame(self.frame_activities, text="Activities List", padx=5, pady=5)
        self.canvas = Canvas(self.wrapper)
        self.frame_activities_list = Frame(self.canvas)
        self.activities_list = Label(self.frame_activities_list)
        self.frame_persons = LabelFrame(self.root, text="Persons", padx=5, pady=5)
        self.frame_persons_list = LabelFrame(self.frame_persons, text="Persons List", padx=5, pady=5)
        self.persons_list = Label(self.frame_persons_list)
        self.warning_label = Label(self.root)
        self.warning_label.pack(side=BOTTOM)
        self.input_frame = Frame(self.root).pack()
        self.entry = Entry(self.input_frame, width=50)
        self.entry.pack()
        self.entry.insert(0, "Input:")

    def run(self):
        self.__activity_service.add_test_data_activities()
        self.__person_service.add_test_data_persons()
        self.root.title('Planner')
        self.root.geometry("725x490")
        self.frame_activities.pack(side=LEFT)
        self.canvas.pack(side=LEFT)
        scrollbar = ttk.Scrollbar(self.wrapper, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side=RIGHT, fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.canvas.create_window((0, 0), window=self.frame_activities_list)
        self.wrapper.pack(fill="both", expand="yes", padx=10, pady=10)
        string_list_of_activities = self.get_activities()
        self.activities_list.config(text=string_list_of_activities)
        self.activities_list.pack()
        frame_activities_buttons = LabelFrame(self.frame_activities, text="Actions",  padx=5, pady=5)
        frame_activities_buttons.pack(side=BOTTOM)
        icon1 = PhotoImage(file='images/plus.png')
        add_activity = Button(frame_activities_buttons, image=icon1, command=self.gui_add_activity)
        add_activity.grid(row=0, column=0)
        icon2 = PhotoImage(file='images/remove.png')
        remove_activity = Button(frame_activities_buttons, image=icon2, command=self.gui_remove_activity)\
            .grid(row=0, column=1)
        icon3 = PhotoImage(file='images/add-anchor-point.png')
        update_activity = Button(frame_activities_buttons, image=icon3, command=self.gui_update_activity)\
            .grid(row=0, column=2)
        icon4 = PhotoImage(file='images/loupe-2.png')
        search_activity = Button(frame_activities_buttons, image=icon4, command=self.gui_search_activity)\
            .grid(row=1, column=0)
        icon5 = PhotoImage(file='images/calendar.png')
        date_activity = Button(frame_activities_buttons, image=icon5, command=self.gui_activity_for_date)\
            .grid(row=1, column=1)
        icon11 = PhotoImage(file='images/busy.png')
        busiest_days = Button(frame_activities_buttons, image=icon11, command=self.gui_busiest_days)\
            .grid(row=1, column=2)
        icon12 = PhotoImage(file='images/work-time.png')
        person_activity = Button(frame_activities_buttons, image=icon12, command=self.gui_activities_with_person)\
            .grid(row=2, column=1)
        icon13 = PhotoImage(file='images/refresh.png')
        update_activity_list = Button(frame_activities_buttons, image=icon13, command=self.refresh_activities)\
            .grid(row=2, column=0)
        string_list_of_persons = self.get_persons()
        self.frame_persons.pack(side=RIGHT)
        self.frame_persons_list.pack(side=TOP)
        self.persons_list.config(text=string_list_of_persons)
        self.persons_list.pack()
        frame_persons_buttons = LabelFrame(self.frame_persons, text="Actions",  padx=5, pady=5)
        frame_persons_buttons.pack(side=BOTTOM)
        icon6 = PhotoImage(file='images/contact.png')
        add_person = Button(frame_persons_buttons, image=icon6, command=self.gui_add_person).grid(row=0, column=0)
        icon9 = PhotoImage(file='images/refresh.png')
        update_list_person = Button(frame_persons_buttons, image=icon9, command=self.refresh_persons)\
            .grid(row=1, column=1)
        icon8 = PhotoImage(file='images/loupe-2.png')
        search_person = Button(frame_persons_buttons, image=icon8, command=self.gui_search_person).grid(row=1, column=0)
        icon7 = PhotoImage(file='images/remove-user.png')
        remove_person = Button(frame_persons_buttons, image=icon7, command=self.gui_remove_person).grid(row=0, column=1)
        icon10 = PhotoImage(file='images/add-anchor-point.png')
        update_person = Button(frame_persons_buttons, image=icon10, command=self.gui_update_person)\
            .grid(row=0, column=2)
        icon14 = PhotoImage(file='images/undo.png')
        icon15 = PhotoImage(file='images/redo.png')
        frame_undo_redo = LabelFrame(self.root, padx=5, pady=5)
        frame_undo_redo.place(x=500, y=380)
        undo_button = Button(frame_undo_redo, image=icon14, command=self.gui_undo).pack()
        redo_button = Button(frame_undo_redo, image=icon15, command=self.gui_redo).pack()
        self.root.mainloop()

    def get_activities(self):
        string_list_of_activities = ""
        try:
            all_activities = self.__activity_service.get_all_activities()
            for activity in all_activities:
                string_list_of_activities += str(activity)
                string_list_of_activities += "\n"
            return string_list_of_activities
        except RepositoryException as error:
            return "THERE ARE NO ACTIVITIES TO DISPLAY"

    def get_persons(self):
        string_list_of_persons = ""
        try:
            all_persons = self.__person_service.get_all_persons()
            for person in all_persons:
                string_list_of_persons += str(person)
                string_list_of_persons += "\n"
            return string_list_of_persons
        except RepositoryException as error:
            return "THERE ARE NO PERSONS TO DISPLAY"

    def refresh_persons(self):
        persons = self.get_persons()
        self.persons_list.config(text=persons)

    def refresh_activities(self):
        activities = self.get_activities()
        self.activities_list.config(text=activities)

    def gui_add_person(self):
        person_id, name, phone_number = self.parse_input_person()
        try:
            operation = self.__person_service.add_person(person_id, name, phone_number)
            self.__undo_service.record(operation)
            self.warning_label.config(text="Person added")
            self.refresh_persons()
            self.refresh_activities()
        except PersonValidatorException as error:
            self.warning_label.config(text=error)
        except RepositoryException as error:
            self.warning_label.config(text=error)

    def gui_remove_person(self):
        try:
            person_id = self.entry.get()
            if person_id == "":
                self.warning_label.config(text="Input should not be empty!")
            operation = self.__person_service.remove_person(person_id)
            self.__undo_service.record(operation)
            self.refresh_persons()
            self.refresh_activities()
            self.warning_label.config(text="Person deleted")
        except RepositoryException as error:
            self.warning_label.config(text=error)

    def gui_remove_activity(self):
        try:
            activity_id = self.entry.get()
            if activity_id == "":
                self.warning_label.config(text="Input should not be empty!")
            operation = self.__activity_service.remove_activity(activity_id)
            self.__undo_service.record(operation)
            self.warning_label.config(text="Activity deleted")
            self.refresh_activities()
        except RepositoryException as error:
            self.warning_label.config(text=error)

    def gui_search_person(self):
        string_to_search = self.entry.get()
        persons = ""
        for person in self.__person_service.search_person(string_to_search.lower()):
            persons += str(person)
        self.persons_list.config(text=persons)

    def gui_search_activity(self):
        string_to_search = self.entry.get()
        activities = ""
        for activity in self.__activity_service.search_activity(string_to_search.lower()):
            activities += str(activity)
        self.activities_list.config(text=activities)

    def gui_activity_for_date(self):
        date = self.entry.get()
        activities = ""
        for activity in self.__activity_service.activities_for_given_date(date):
            activities += str(activity)
        self.activities_list.config(text=activities)

    def gui_activities_with_person(self):
        person = self.entry.get()
        activities = ""
        for activity in self.__activity_service.activities_with_person(person):
            activities += str(activity)
        self.activities_list.config(text=activities)

    def gui_busiest_days(self):
        days = "Your busiest upcoming days are:\n"
        for date in self.__activity_service.busiest_days():
            days += date.strftime("%B %d, %Y")
            days += "\n"
        self.activities_list.config(text=days)

    def gui_update_person(self):
        update_id, new_name, new_phone_number = self.parse_input_person()
        try:
            operation = self.__person_service.update_person(update_id, new_name, new_phone_number)
            self.__undo_service.record(operation)
            self.warning_label.config(text="Person updated")
            self.refresh_persons()
        except RepositoryException as error:
            self.warning_label.config(text=error)

    def gui_update_activity(self):

        update_id, new_persons, new_date, new_start, new_end, new_description = self.parse_input_activity()
        try:
            operation = self.__activity_service.update_activity(update_id, new_persons, new_date, new_start, new_end,
                                                                new_description)
            self.__undo_service.record(operation)
            self.warning_label.config(text="Activity updated")
            self.refresh_activities()
        except RepositoryException as error:
            self.warning_label.config(text=error)

    def gui_add_activity(self):
        activity_id, persons, date, start, end, description = self.parse_input_activity()
        try:
            operation = self.__activity_service.add_activity(activity_id, persons, date, start, end, description)
            self.__undo_service.record(operation)
            self.warning_label.config(text="Activity added")
            self.refresh_activities()
        except ActivityValidatorException as error:
            self.warning_label.config(text=error)
        except RepositoryException as error:
            self.warning_label.config(text=error)

    def parse_input_person(self):
        string = self.entry.get()
        person_parameters = string.split(",")
        person_id = person_parameters[0].strip()
        name = person_parameters[1].strip()
        number = person_parameters[2].strip()
        return person_id, name, number

    def parse_input_activity(self):
        string = self.entry.get()
        activity_parameters = string.split(";")
        activity_id = activity_parameters[0].strip()
        persons = activity_parameters[1].strip()
        persons = persons.split(",")
        date = activity_parameters[2].strip()
        start = activity_parameters[3].strip()
        end = activity_parameters[4].strip()
        description = activity_parameters[5].strip()
        return activity_id, persons, date, start, end, description

    def gui_undo(self):
        self.__undo_service.undo()
        self.refresh_activities()
        self.refresh_persons()

    def gui_redo(self):
        self.__undo_service.redo()
        self.refresh_activities()
        self.refresh_persons()