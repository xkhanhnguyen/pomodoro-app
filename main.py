from tkinter import *
import math, os, random
from pygame import mixer


# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None
# ---------------------------- SOUND EFFECT ------------------------------- #
mixer.init()
notification = mixer.Sound(f"./audio/ding-sound-effect.mp3")
rain_sound_effect = mixer.Sound(f"./audio/soft-rain-sound-effect.mp3")


class Pomodoro: 
    def __init__(self):
        self.mp3_sound_effect = None

    # ---------------------------- TIMER RESET ------------------------------- # 
    def timer_reset(self):
        self.window.after_cancel(self.timer)
        self.canvas.itemconfig(self.timer_text, text="00:00")
        self.timer_label.config(text="Timer", foreground=GREEN)
        self.check_marks.config(text="")
        self.reps = 0  # Use self.reps to access the class attribute
    # ---------------------------- TIMER MECHANISM ------------------------------- # 
    def start_timer(self):
        global reps
        reps += 1
        work_sec = WORK_MIN * 60
        short_break_sec = SHORT_BREAK_MIN * 60
        long_break_sec = LONG_BREAK_MIN * 60
        # if it's the last rep
        if reps % 8 == 0:
            self.count_down(long_break_sec)
            self.timer_label.config(text="Break", foreground=RED)
        # if it's the 2nd, 4th, 6th rep:
        elif reps % 2 == 0:
            self.music_play()
            self.count_down(short_break_sec)
            self.timer_label.config(text="Break", foreground=PINK)
        # if it's the 1st, 3rd, 5th, 7th rep:
        else:
            self.music_play()
            self.count_down(work_sec)
            self.timer_label.config(text="Work", foreground=GREEN)
            
    def music_play(self):
        if self.mp3_sound_effect is not None:
            self.mp3_sound_effect.stop()  # Stop the previously playing sound effect
        mp3_file = random.choice(os.listdir('./audio/break_time_music'))
        self.mp3_sound_effect = mixer.Sound(f"./audio/break_time_music/{mp3_file}")
        if reps % 2 == 1:
            rain_sound_effect.play(-1)
        else:
            rain_sound_effect.stop()
            self.mp3_sound_effect.play(-1)  # Start the new sound effect
                  
    # ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
    def count_down(self, count):
        count_min = math.floor(count / 60)
        count_sec = math.floor(count % 60)
        if count_sec < 10:
            count_sec = f"0{count_sec}" #'%02d' % count_sec
        self.canvas.itemconfig(self.timer_text, text=f"{count_min}:{count_sec}")
        if count > 0:
            self.timer = self.window.after(10, self.count_down, count - 1)
        else:
            self.start_timer()
            notification.play()
            marks = ""
            work_session = math.floor(reps/2)
            for _ in range(work_session):
                marks += "✔"
                self.check_marks.config(text=marks)

    def main(self):
        # ---------------------------- UI SETUP ------------------------------- #
        self.window = Tk()
        self.window.title("Pomodoro")
        self.window.config(padx=100, pady=50, background=YELLOW)

        self.timer_label = Label(text="Timer", font=(FONT_NAME, 50, "bold"), foreground=GREEN, background=YELLOW)
        self.timer_label.grid(row=0, column=1)

        self.canvas = Canvas(width=200, height=224, background=YELLOW, highlightthickness=0)
        self.tomato_img = PhotoImage(file="tomato.png")
        self.canvas.create_image(100, 112, image=self.tomato_img)
        self.timer_text = self.canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
        self.canvas.grid(row=1, column=1)

        #Button
        self.start = Button(text="Start", highlightthickness=0, command=self.start_timer)
        self.start.grid(row=2, column=0)

        self.reset = Button(text="Reset", highlightthickness=0, command=self.timer_reset)
        self.reset.grid(row=2, column=2)

        self.check_marks = Label(foreground=GREEN, background=YELLOW)
        self.check_marks.grid(row=3, column=1)
        self.window.mainloop()

if __name__ == '__main__':
    pomo= Pomodoro()
    pomo.main()
    

