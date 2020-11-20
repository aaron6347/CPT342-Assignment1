"""university_course_inference_engine.py
    Created by Aaron at 20-Nov-20"""
import csv

# open knowledge csv file
try:
    with open("university_course_knowledge.csv", "r") as knowledge:
            reader = csv.DictReader(knowledge)
            # TODO data stucture to store facts
            # data =

            # read facts
            for each in reader:
                # TODO store facts as data
                print(each)

    # to store university course inference result
    result = False
    answer = ''

    # inference process
    while(not result):
        # TODO choose question

        # accept query
        user = input()

        # TODO inference process


        # TODO if query doesn't match in facts
        # if somethinghere:
        #     result = True
        #     answer = "Not found"
        result=True #testing purpose

        # TODO write inference into the textfile
        writer = open("inference.txt", "a")
        writer.write("something here\n")
        # if inference process has successfully completed
        if result == True:
            writer.write("Inference Result: {}\n".format(answer))
            writer.write("COMPLETED\n")

# if knowledge csv file not found
except FileNotFoundError as e:
    print("university_course_knowledge.csv is not found!")


