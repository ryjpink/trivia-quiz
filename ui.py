from tkinter import *
from tkinter.colorchooser import askcolor
from quiz_brain import QuizBrain
from PIL import ImageTk, Image

THEME_COLOR = "#89caf5"
FONT_COLOR = "#8989f5"

class QuizInterface:
    def __init__(self, quizbrain: QuizBrain):
        self.quiz = quizbrain

        self.background_color = THEME_COLOR
        self.foreground_color = FONT_COLOR

        self.window = Tk()
        self.window.title("My Little Quiz")
        self.window.config(padx=20, pady=20,bg=self.background_color)

        self.menubar = Menu(self.window)
        self.settingsmenu = Menu(self.menubar)
        self.settingsmenu.add_command(label="Background color", command=self.change_background_color)
        self.settingsmenu.add_command(label="Quiz text color", command=self.change_foreground_color)
        self.menubar.add_cascade(label="Settings", menu=self.settingsmenu)
        self.window.config(menu=self.menubar)

        self.score = Label(text="Score:0",font=("Calibri", 14, "bold") ,fg="white",bg=self.background_color)
        self.score.grid(row=0,column=1)

        self.mycanvas = Canvas(width=300, height=250, bg="white")
        self.question_text = self.mycanvas.create_text(150, 125,width=280, text="Some Question text", fill=self.foreground_color, font=("Arial", 20, "italic"))
        self.mycanvas.grid(row=1, column=0, columnspan=2, pady=30)

        self.true_image = ImageTk.PhotoImage(Image.open("images/true.png"))
        self.true_button = Button(image=self.true_image, highlightthickness=0, command=self.true_pressed)
        self.true_button.grid(row=2, column=0)

        self.false_image = ImageTk.PhotoImage(Image.open("images/false.png"))
        self.false_button = Button(image=self.false_image, highlightthickness=0, command=self.false_pressed)
        self.false_button.grid(row=2, column=1)

        self.get_next_question()

    def change_background_color(self):
        selected_color = askcolor(color=self.background_color, title="Choose background color")
        if not selected_color[1] is None:
            self.background_color = selected_color[1]
            self.window.config(bg=self.background_color)
            self.score.config(bg=self.background_color)
            self.window.update()

    def change_foreground_color(self):
        selected_color = askcolor(color=self.foreground_color, title="Choose foreground color")
        if not selected_color[1] is None:
            self.foreground_color = selected_color[1]
            self.mycanvas.itemconfig(self.question_text, fill=self.foreground_color)
            self.window.update()

    def run(self):
        self.window.mainloop()

    def get_next_question(self):
        self.mycanvas.config(bg="white")
        self.score.config(text=f"Score: {self.quiz.score}")
        if self.quiz.still_has_questions():
            q_text = self.quiz.next_question()
            self.mycanvas.itemconfig(self.question_text, text=q_text)
        else:
            self.mycanvas.itemconfig(self.question_text, text=f"Sorry, we've run out of question.\nYour final score:{self.quiz.score}")
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")
        self.window.update()

    def true_pressed(self):
        self.give_feedback(self.quiz.check_answer("True"))



    def false_pressed(self):
        self.give_feedback(self.quiz.check_answer("False"))

    def give_feedback(self, is_right):
        if is_right:
            self.mycanvas.config(bg="green")
        else:
            self.mycanvas.config(bg="red")
        self.window.update()
        self.window.after(1000, self.get_next_question)




