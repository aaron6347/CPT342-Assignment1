"""university_course_inference_engine.py
    Created by Aaron at 23-Nov-20"""
import csv
import tkinter as tk
import tkinter.messagebox as messagebox

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
        windowWidth = app.winfo_reqwidth()
        windowHeight = app.winfo_reqheight()
        positionRight = int(app.winfo_screenwidth() / 2 - windowWidth / 2)
        positionDown = int(app.winfo_screenheight() / 3 - windowHeight / 2)
        app.geometry("600x450+{}+{}".format(positionRight, positionDown))
        app.configure(bg="#444444")

        for i in range(3):
            app.rowconfigure(i, weight=1, minsize=25)
            app.columnconfigure(i, weight=1, minsize=25)

        questionFrame = tk.Frame(master=app)
        questionFrame.grid(row=0, column=1, padx=20, pady=20)

        buttonsFrame = tk.Frame(master=app, bg="#444444")
        buttonsFrame.grid(row=1, column=1)

        def process_result(event):
            global result, answer, current_question_ind
            user = event.widget.cget("text")
            # if user answer is in the options, then find possible result
            for course in answer_pool[:]:
                # if the course's fact isn't same as user answer, then remove the course from answer_pool
                if courses_dict[course][current_question_ind - 1] != user:
                    answer_pool.remove(course)

            # if the answer pool only has one answer, then display answer
            if len(answer_pool) == 1:
                result = True
                answer = answer_pool[0]
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

        def on_enter(event):
            event.widget.config(background="#d7d7d7")

        def on_leave(event):
            event.widget.config(background="SystemButtonFace")

        # choose question
        question, options = header[current_question_ind].split("(")
        options = list(options.replace(")", "").replace(" ", "").split(","))
        options_desc = "(Remarks: H: High, M: Medium, L: Low)"
        # validate options for CGPA situation
        if "CGPA" in question:
            options = ["H", "L"]
            options_desc = "(Remarks: H: >2.50, L: <2.50)"

        labelString = "What is your {}?".format(question)
        if "Major" not in question and "computer" not in question:
            labelString += "\n" + options_desc
        questionLabel = tk.Label(text=labelString, master=questionFrame, font=("Times New Roman", 16, "bold"),
                                 bg="#444444", fg="#FFFFFF")
        questionLabel.pack()

        # accept query
        for opt in options:
            buttonFrame = tk.Frame(master=buttonsFrame, relief=tk.RAISED, borderwidth=2)
            buttonFrame.pack(side=tk.LEFT, padx=40, pady=40)
            button = tk.Button(text=opt, width=12, height=2, master=buttonFrame, font=("Times New Roman", 10))
            button.bind("<Button-1>", process_result)
            button.bind("<Enter>", on_enter)
            button.bind("<Leave>", on_leave)
            button.pack()

        app.mainloop()

# if knowledge csv file not found
except FileNotFoundError as e:
    print("university_course_knowledge.csv is not found!")
