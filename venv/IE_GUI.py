"""university_course_inference_engine.py
    Created by Aaron at 20-Nov-20"""
import csv
import tkinter as tk
import tkinter.messagebox as messagebox

# window = tk.Tk()
# window.title("University Programme Expert System")
# for i in range(3):
#     window.rowconfigure(i, weight=1, minsize=25)
#     window.columnconfigure(i, weight=1, minsize=25)
#
#
# def button_pressed(event):
#     print(event.widget.cget("text"))
#     window.destroy()
#
#
# frame = tk.Frame(master=window)
# frame.grid(row=0, column=1)
#
# question = tk.Label(text="Lul", width=10, height=10, master=frame)
# question.pack()
#
# mainFrame = tk.Frame(master=window)
# mainFrame.grid(row=1, column=1)
#
# frame2 = tk.Frame(master=mainFrame, relief=tk.RAISED, borderwidth=2)
# frame2.pack(side=tk.LEFT, padx=20, pady=20)
#
# choice = tk.Button(text="Click here", width=8, height=2, master=frame2)
# choice.bind("<Button-1>", button_pressed)
# choice.pack()
#
# frame3 = tk.Frame(master=mainFrame, relief=tk.RAISED, borderwidth=2)
# frame3.pack(side=tk.LEFT, padx=20, pady=20)
#
# choice2 = tk.Button(text="Click There", width=8, height=2, master=frame3)
# choice2.bind("<Button-1>", button_pressed)
# choice2.pack()
# window.mainloop()

# open knowledge csv file
try:
    with open("university_course_knowledge.csv", "r") as knowledge:
        # data structure to store facts
        reader = csv.DictReader(knowledge)
        header = reader.fieldnames  # to store all header
        courses_dict = {}  # to store all courses' data
        # read and store facts
        for ind, row in enumerate(reader):
            collection_of_data = []  # to compile a course's facts
            # compilation facts process
            for each in row:
                collection_of_data.append(row[each])
            courses_dict[collection_of_data.pop(0)] = collection_of_data
        print(
            courses_dict)  ############################################################################################# to del
    # to store university course inference result
    result = False
    answer = ''
    current_question_ind = 1  # start from 1 because question is from 1 in variable header

    # inference process
    answer_pool = list(courses_dict.keys())  # possible course as the result of inference
    while not result:
        # GUI Main Window
        app = tk.Tk()
        app.title("University Programme Expert System")
        app.geometry("400x300")
        for i in range(3):
            app.rowconfigure(i, weight=1, minsize=25)
            app.columnconfigure(i, weight=1, minsize=25)

        questionFrame = tk.Frame(master=app)
        questionFrame.grid(row=0, column=1)

        buttonsFrame = tk.Frame(master=app)
        buttonsFrame.grid(row=1, column=1)


        def process_result(event):
            global result, answer, current_question_ind
            user = event.widget.cget("text")
            # if user answer is in the options, then find possible result
            for course in answer_pool[:]:
                # if the course's fact isn't same as user answer, then remove the course from answer_pool
                if courses_dict[course][current_question_ind - 1] != user:
                    answer_pool.remove(course)
                print("internal finding answer",
                      answer_pool)  ############################################################################################# to del

            # if the current_question_ind has reach the end, then display answer
            if len(answer_pool) == 1 or current_question_ind == len(header) - 1:
                result = True
                # if there is result
                if len(answer_pool) == 1:
                    answer = answer_pool.pop()
                # if there is no result
                else:
                    answer = "Not Found"
                # print("Result: {}".format(answer))
                messagebox.showinfo("Results", "The recommended university programme: {}".format(answer))

            # write inference into the textfile
            writer = open("inference.txt", "a")
            # if this is the first time
            if current_question_ind == 1:
                writer.write("\n_____New Inference_____\n")
            writer.write("\nQuestion: {}\n".format(question))
            writer.write("Answer: {}\n".format(user))
            writer.write("Possible Course: {}\n".format(answer_pool))
            # if inference process has successfully completed
            if result:
                writer.write("\nInference Result: {}\n".format(answer))
                writer.write("COMPLETED\n")

            current_question_ind += 1  # to proceed next question
            app.destroy()


        # choose question
        question, options = header[current_question_ind].split("(")
        options = list(options.replace(")", "").replace(" ", "").split(","))
        options_desc = "(Remarks: H: High, M: Medium, L: Low)"
        # validate options for CGPA situation
        if "CGPA" in question:
            options = ["H", "L"]
            options_desc = "(Remarks: H: >2.50, L: <2.50)"
        # print("What is your {}?".format(question))
        # print("Options: ", options)
        labelString = "What is your {}?".format(question)
        if "Major" not in question and "computer" not in question:
            labelString += "\n" + options_desc
        questionLabel = tk.Label(text=labelString, master=questionFrame)
        questionLabel.pack()
        # accept query
        # user = input()
        # # if user answer is not in the options, then continue ask the same question
        # if user not in options:
        #     print("Invalid Option")
        #     continue

        for opt in options:
            buttonFrame = tk.Frame(master=buttonsFrame, relief=tk.RAISED, borderwidth=2)
            buttonFrame.pack(side=tk.LEFT, padx=20, pady=20)
            button = tk.Button(text=opt, width=8, height=2, master=buttonFrame)
            button.bind("<Button-1>", process_result)
            button.pack()

        # if inference process hasn't completed
        app.mainloop()

# if knowledge csv file not found
except FileNotFoundError as e:
    print("university_course_knowledge.csv is not found!")
