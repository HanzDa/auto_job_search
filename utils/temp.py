# import json
#
# questions = open('../scrapers/linked_in/easy_apply_question.json')
#
# data = json.loads(questions.read())
#
# if __name__ == '__main__':
#     print(data['Do you have experience working with AuthZero?'])
from lxml.html._diffcommand import description

from models.company import Company
from models.job import Job

my_company = Job.create(title='Un titulo bonito',
                        description="I'm a wizard")

# my_company = Job.get_object(fields=('name', 'pk'), pk=1, linked_in_url='www.hanz_gallego.com')

print(my_company.name, my_company.linked_in_url)



# class Parent:
#     def __init__(self):
#         pass
#
#     @classmethod
#     def create_child(cls, name):
#         return cls(name)
#
#
# class Child(Parent):
#     def __init__(self, name):
#         self.name = name
#         super().__init__()
#
#
# child = Child.create_child(name='Oswal')
