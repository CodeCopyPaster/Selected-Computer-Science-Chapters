import pickle
import csv


class SerializationMixin:
    @staticmethod
    def csv_serialize(students, filename='students.csv'):
        '''Serialize list of Human() into *.csv'''
        data_to_save = [human.data for human in students]
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['surname', 'dormitory', 'work_years','education','language'])
            writer.writeheader()
            writer.writerows(data_to_save)

    @staticmethod
    def pickle_serialize(students, filename='students.pkl'):
        '''Serialize list of Human() into *.pkl'''
        with open(filename, 'wb') as file:
            pickle.dump(students, file)

    @staticmethod
    def csv_read(filename='students.csv'):
        '''Read from CSV and return list of Human objects'''
        students = []
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                students.append(Student(row['surname'], row['dormitory'], row['work_years'], row['education'],row['language']))
        return students

    @staticmethod
    def pickle_read(filename='students.pkl'):
        '''Read from pickle file'''
        with open(filename, 'rb') as file:
            return pickle.load(file)


class Student(SerializationMixin):
    def __init__(self, surname, dormitory, work_years, education, language):
        self.data = {
            'surname': surname,
            'dormitory': dormitory,
            'work_years': work_years,
            'education': education,
            'language': language
        }

    def __str__(self):
        return f'Фамилия:{self.get_surname()} Общага?:{self.get_dormitory()} Стаж работы:{self.get_work_years()} Образование:{self.get_education()} Язык:{self.get_language()}'

    def get_surname(self):
        return self.data['surname']

    def get_dormitory(self):
        return self.data['dormitory']

    def get_work_years(self):
        return self.data['work_years']

    def get_education(self):
        return self.data['education']

    def get_language(self):
        return self.data['language']

    def printInfo(self):
        '''Outputs all the info'''
        print(f'Фамилия:{self.get_surname()} Общага?:{self.get_dormitory()} Стаж работы:{self.get_work_years()} Образование:{self.get_education()} Язык:{self.get_language()}')

    @staticmethod
    def howManyNeededForDormitory(students):
        '''Counts how many people are need for a dormitory'''
        numOfNeeders = 0
        for person in students:
            if person.get_dormitory() == '1':
                numOfNeeders += 1
        return numOfNeeders

    @staticmethod
    def findPeopleWithHugeWorkExp(students):
        '''Returns list of people with work experience > 2 years'''
        listOfProfis = []
        for person in students:
            if int(person.get_work_years()) >= 2:
                listOfProfis.append(person.get_surname())
        return listOfProfis

    @staticmethod
    def findPeoplefromTech(students):
        '''Returns lsit of people from technicum '''
        listOfTechPeople = []
        for person in students:
            if person.get_education() == 'technicum':
                listOfTechPeople.append(person.get_surname())
        return listOfTechPeople

    @staticmethod
    def getLanguageGroups(students):
        '''Returns list of lang groups'''
        listOfLangGroups = []
        for person in students:
            if person.get_language() not in listOfLangGroups:
                listOfLangGroups.append(person.get_language())
        return listOfLangGroups



def task1():
    people = Student.csv_read('students.csv')

    print('Исходный список людей:')
    for person in people:
        person.printInfo()

    print('кол-во людей которые нуждаются в общежитии:', Student.howManyNeededForDormitory(people))
    print('кол-во людей со стажем >= 2:', Student.findPeopleWithHugeWorkExp(people))
    print('список людей после техникума:',Student.findPeoplefromTech(people))
    print('список языковых групп:', Student.getLanguageGroups(people))

    if input('Чтобы добавить студента введите 1, 0 чтобы продолжить ')==1:
        new_person = Student(
            input('Введите фамилию: '),
            input('Введите нуждается ли в общаге (1/0): '),
            input('Введите стаж работы: '),
            input('Введите образование:'),
            input('Введите язык студента:')
        )
        people.append(new_person)

        print('Обновленный список людей:')
        for person in people:
            person.printInfo()
    Student.csv_serialize(people)
    Student.pickle_serialize(people)
    print("\nДесериализованные данные из pickle:")
    loaded_people = Student.pickle_read('students.pkl')
    for person in loaded_people:
        print(person)
    print("\nДесериализованные данные из csv:")
    loaded_people = Student.csv_read('students.csv')
    for person in loaded_people:
        print(person)


