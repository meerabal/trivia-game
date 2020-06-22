import urllib.request
import sys
import re
import json

# class holds all the attributes for an object of type Question
class Question:
    def __init__(self, category, ques_type, difficulty, ques, correct_ans, incorrect_ans):
        self.category = category
        self.ques_type = ques_type
        self.difficulty = difficulty
        self.ques = ques
        self.correct_ans = correct_ans
        self.incorrect_ans = incorrect_ans
        self.user_ans = ""

# returns the string contents of the page at url, or "" if there is an error
def readurl(url):
    try:
        fp = urllib.request.urlopen(url)
        mybytes = fp.read()
        mystr = mybytes.decode(sys.stdout.encoding)
        fp.close()
        return mystr
    except:
        return ""

# cleans input for inverted commas and quotation marks
def clean(given):
    if type(given) == str:
        return given.replace("&#039;", "'").replace('&quot;', '"')
    elif type(given) == list:
        newlist = []
        for elem in given:
            newlist.append(clean(elem))
        return newlist

# creates question objects and stores them in a ques_list
def obj_create(content):
    ques_dict = json.loads(content)["results"]      # could use eval(str) but eval is very powerful and should not be used if input is not completely trusted
    ques_list = []
    for q in ques_dict:
        print(q)
        ques_list.append(Question(q["category"], q["type"], q["difficulty"], clean(q["question"]), clean(q["correct_answer"]), clean(q["incorrect_answers"])))
        return ques_list
    '''# testing
    for q in ques_list:
        print(q.category, q.ques_type, q.difficulty, q.ques, q.correct_ans, str(q.incorrect_ans))'''

# sets type of question to be asked and difficulty
def init():
    return_str = ""

    print("Trivia game")
    print("The game will ask 10 questions from different categories and keep a track of your score.")
    difficulty = input("Choose difficulty level: Easy (1) or Medium (2) or Hard (3) or Mixed (4)? ")
    while True:
        if not(difficulty.isnumeric and 0 < int(difficulty) < 5):
            difficulty = input("Invalid input. Please enter \n1 for easy \n2 for medium \n3 for hard \n4 for mixed \n> ")
        else:
            if int(difficulty) == 1:
                return_str += "&difficulty=easy"
            elif int(difficulty) == 2:
                return_str += "&difficulty=medium"
            elif int(difficulty) == 3:
                return_str += "&difficulty=hard"
    
    ques_type = input("Choose type of questions: Multiple choice (1) or True / False (2) or Mixed (3)? ")
    while True:
        if not(ques_type.isnumeric and 0 < int(ques_type) < 4):
            ques_type = input("Invalid input. Please enter \n1 for multiple choice \n2 for true / false \n3 for mixed \n> ")
        else:
            if int(ques_type) == 1:
                return_str += "&type=multiple"
            elif int(ques_type) == 2:
                return_str += "&type=boolean"
    
    return return_str

# main method
def main():
    ques_type = init()
    content = readurl("https://opentdb.com/api.php?amount=10" + ques_type)
    ques_list = obj_create(content)

main()