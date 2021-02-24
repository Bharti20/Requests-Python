import requests
import json
import os.path
from os import path
print()
print("------- Welcome to Saral page ----------")
print()
url = "https://saral.navgurukul.org/api/courses"
def online(fname, link):
    if path.exists(fname)==True:
        particular_course(fname)
    else:
        response = requests.get(link)
        data=response.text
        dump_data=json.dumps(response.json(), indent=4)    
        dictionary=json.loads(data)

        with open(fname, "w") as jsonFile:
            jsonFile.write(dump_data)
        return dictionary
def converting_to_py():
    if path.exists("courses.json")==True:
        with open("courses.json", "r") as convert_to_py:
            pyData=json.load(convert_to_py)
        return pyData
    else:
        res = requests.get(url)
        dumpData =json.dumps(res.json(), indent=4 )
        with open("courses.json", "w") as creat_json_file:
            creat_json_file.write(dumpData)

        with open("courses.json", "r") as convert_to_py:
            pyData=json.load(convert_to_py)
        return pyData 
def printCourses(data):
    print()
    print("**************** Available Courses ****************")
    print()
    id_list=[]
    i=0
    while i<len(data['availableCourses']):
        id_list.append(data['availableCourses'][i]["id"])
        print(i, data['availableCourses'][i]['name'])
        i=i+1
def ids_print():
    courses_ids_list=[]
    store = converting_to_py()
    x=0
    while x<len(store['availableCourses']):
        courses_ids_list.append(store['availableCourses'][x]["id"])
        x=x+1
    return courses_ids_list
def particular_course(name):
    with open(name, "r") as one_course_data:
        all_d =json.load(one_course_data)
        return all_d
def parentChild_exersise():
    store_id_list = ids_print()
    save=converting_to_py()
    printCourses(save)
    course_index=int(input("select a course---"))
    child_ids=[]
    slug_list=[]
    print()
    print("******************* parent exersise**************************")
    print()
    j=0
    while j<len(save["availableCourses"]):
        if course_index==j:
            url2="https://saral.navgurukul.org/api/courses/"+str(store_id_list[j])+"/exercises"
            file_name = "exercises"+str(store_id_list[j])+".json"
            online(file_name, url2)
            print(save["availableCourses"][j]["name"])
            data_store =particular_course(file_name)
            # print("uuuu", data_store)
            z=0
            length =data_store["data"]
            while z<len(length):
                child_ids.append(data_store["data"][z]["id"])
                slug_list.append(data_store["data"][z]["slug"])
                print("    ", z,(data_store["data"][z]["name"]))
                if len(data_store["data"][z]["childExercises"])==0:
                        print("       ", (data_store["data"][z]["childExercises"]))
                        print()
                else:
                    index=0
                    while index<len(data_store["data"][z]["childExercises"]):
                        print("       ", (data_store["data"][z]["childExercises"][index]["name"]))
                        slug_list.append(data_store["data"][z]["childExercises"][index]["slug"])
                        print()
                        index=index+1
                z=z+1
            print("*************** Slug ***************")
            print()
            print(slug_list)
            print()
            inputForSlug=int(input("select a slug:--"))
            y=0
            while y<len(length):
                if inputForSlug==y:
                    third_api=requests.get("https://merakilearn.org/api/courses/"+str(store_id_list[j])+"/exercise/getBySlug?slug="+str(slug_list[y]))
                    break
                y=y+1
            slug_data = json.dumps(third_api.json())

            slug_py_data = json.loads(slug_data)

            print(slug_py_data["content"])
        j=j+1
    print()
    print("******************** user choice ************************")
    print()
    while True:
        user_choice=input("what you want to do 1. up, 2. next. 3. p:----")
        if user_choice=="up": 
            print()
            save=converting_to_py()
            printCourses(save)
            parentChild_exersise()
        elif user_choice=="next":
            if inputForSlug==len(slug_list):
                print("there is no next slug ")
                break
            else:
                third_api=requests.get("https://merakilearn.org/api/courses/75/exercise/getBySlug?slug="+str(slug_list[y+1]))                 
                slug_data = json.dumps(third_api.json())
                slug_py_data = json.loads(slug_data)
                print(slug_py_data["content"])
                break
        elif user_choice=="p":
            if inputForSlug==0:
                print("there is no previous slug content")
                break
            else:
                third_api=requests.get("https://merakilearn.org/api/courses/75/exercise/getBySlug?slug="+str(slug_list[y-1]))                 
                slug_data = json.dumps(third_api.json())
                slug_py_data = json.loads(slug_data)
                print(slug_py_data["content"])
                break
    print()
    print("-----------------Thank you for visit!! ------------------------ ")
parentChild_exersise()