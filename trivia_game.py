import urllib.request
import sys
import re
import json

class Question:
    def __init__(self, category, ques_type, difficulty, ques, correct_ans, incorrect_ans):
        self.category = category
        self.ques_type = ques_type
        self.difficulty = difficulty
        self.ques = ques
        self.correct_ans = correct_ans
        self.incorrect_ans = incorrect_ans

#returns the string contents of the page at url, or "" if there is an error
def readurl(url):
    try:
        fp = urllib.request.urlopen(url)
        mybytes = fp.read()
        mystr = mybytes.decode(sys.stdout.encoding)
        fp.close()
        return mystr
    except:
        return ""

def clean(given):
    if type(given) == str:
        return given.replace("&#039;", "'").replace('&quot;', '"')
    elif type(given) == list:
        newlist = []
        for elem in given:
            newlist.append(clean(elem))
        return newlist


def obj_create(content):
    ques_dict = json.loads(content)["results"]      # could use eval(str) but eval is very powerful and should not be used if input is not completely trusted
    ques_list = []
    for q in ques_dict:
        print(q)
        ques_list.append(Question(q["category"], q["type"], q["difficulty"], clean(q["question"]), clean(q["correct_answer"]), clean(q["incorrect_answers"])))
    # testing
    for q in ques_list:
        print(q.category, q.ques_type, q.difficulty, q.ques, q.correct_ans, str(q.incorrect_ans))

def jsontolist(string): #string is actually a dictionary
    string = string.strip("{ }").replace('"', ' ').replace(',', ' ')
    #string = create_ques_object(string)
    stringlist = re.split("[{}]", string)
    ques_list = []
    '''try:
        stringlist.remove("")
    except:
        pass'''
    for s in stringlist:
        ques_list.append(create_ques_object(s))
        print(s, "###")

'''def create_ques_object(string):
    #new_str = string.replace(',', ' ').replace('"', ' ')
    stringlist = string.split(' ')

    category = ' '.join(map(str, stringlist[stringlist.index("category"+1) : stringlist.index("type"-1)])
    ques_type = ' '.join(map(str, stringlist[stringlist.index("type"+1) : stringlist.index("difficulty"-1)])
    difficulty = ' '.join(map(str, stringlist[stringlist.index("difficulty"+1) : stringlist.index("question"-1)])
    
    q = Question(category, ques_type, )
    #return new_str'''

def main():
    content = readurl("https://opentdb.com/api.php?amount=10")
    obj_create(content)

main()