# import json
#
# questions = open('../scrapers/linked_in/easy_apply_question.json')
#
# data = json.loads(questions.read())
#
# if __name__ == '__main__':
#     print(data['Do you have experience working with AuthZero?'])

from models.company import Company


# my_company = Company.create(name='Last test',
#                             linked_in_url='www.linkedin.com')

my_company = Company.get_object(fields=('name', 'pk'), pk=1, linked_in_url='www.hanz_gallego.com')

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
