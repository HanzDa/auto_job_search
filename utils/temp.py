import json

questions = open('../scrapers/linked_in/easy_apply_question.json')

data = json.loads(questions.read())

if __name__ == '__main__':
    print(data['Do you have experience working with AuthZero?'])

