"""university_course_inference_engine.py
    Created by Aaron at 20-Nov-20"""
import csv

# open knowledge csv file
try:
    with open("university_course_knowledge.csv", "r") as knowledge:
        # data structure to store facts
        reader = csv.DictReader(knowledge)
        header = reader.fieldnames  # to store all header
        courses_dict = {}           # to store all courses' data
        # read and store facts
        for ind, row in enumerate(reader):
            collection_of_data = [] # to compile a course's facts
            # compilation facts process
            for each in row:
                collection_of_data.append(row[each])
            courses_dict[collection_of_data.pop(0)] = collection_of_data
        print(courses_dict) ############################################################################################# to del
    # to store university course inference result
    result = False
    answer = ''
    current_question_ind = 1    # start from 1 because question is from 1 in variable header

    # inference process
    answer_pool = list(courses_dict.keys())     # possible course as the result of inference
    while(not result):
        # choose question
        question, options = header[current_question_ind].split("(")
        options = list(options.replace(")", "").replace(" ", "").split(","))
        # validate options for CGPA situation
        if "CGPA" in question:
            options = ["H", "L"]
        print("What is your {}?".format(question))
        print("Options: ", options)
        # accept query
        user = input()
        # if user answer is not in the options, then continue ask the same question
        if user not in options:
            print("Invalid Option")
            continue
        # if user answer is in the options, then find possible result
        for course in answer_pool[:]:
            # if the course's fact isn't same as user answer, then remove the course from answer_pool
            if courses_dict[course][current_question_ind-1] != user:
                answer_pool.remove(course)
            print("internal finding answer", answer_pool) ############################################################################################# to del

        # if there is one or no more course in answer_pool or the current_question_ind has reach the end, then display answer
        if len(answer_pool) <= 1 or current_question_ind == len(header)-1:
            result = True
            # if there is result
            if len(answer_pool) == 1:
                answer = answer_pool.pop()
            # if there is no result
            else:
                answer = "Not Found"
            print("Result: {}".format(answer))

        # write inference into the textfile
        writer = open("inference.txt", "a")
        # if this is the first time
        if current_question_ind == 1:
            writer.write("\n_____New Inference_____\n")
        writer.write("\nQuestion: {}\n".format(question))
        writer.write("Answer: {}\n".format(user))
        writer.write("Possible Course: {}\n".format(answer_pool))
        # if inference process has successfully completed
        if result == True:
            writer.write("\nInference Result: {}\n".format(answer))
            writer.write("COMPLETED\n")
        # if inference process hasn't completed
        current_question_ind += 1   # to proceed next question

# if knowledge csv file not found
except FileNotFoundError as e:
    print("university_course_knowledge.csv is not found!")


