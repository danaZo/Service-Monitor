import sys
from threading import Thread
from tkinter import *
from tkinter import font
from tkinter import ttk
import tkinter.messagebox
import tkinter as tk
import main

menu = "Welcome to our service monitoring tool\n\n" \
       "Here you will see the changes made between every two consecutive samples\n" \
       "To manually compare two samples, insert their time in the following format:,\n" \
       "YYYY-MM-DD-HH-MM-SS"


class StdoutRedirector(object):
    def __init__(self,text_widget):
        self.text_space = text_widget

    def write(self,string):
        self.text_space.insert('end', string)
        self.text_space.see('end')


class GUI:

    # GUI functions
    def __init__(self):
        self.Window = Tk()
        self.Window.withdraw()

        self.main_menu = Toplevel()
        self.main_menu.title("Main Menu")
        self.main_menu.resizable(width=False, height=False)
        self.main_menu.configure(width=400, height=300, background='grey3')

        self.pls = Label(self.main_menu, text="Select a time interval in seconds:", justify=CENTER, font="Helvetica 14 bold",
                         background='grey3', fg= 'white')
        self.pls.place(relheight=0.15, relx=0.25, rely=0.07)

        self.entryNum = Entry(self.main_menu, font="Helvetica 14")
        self.entryNum.place(relwidth=0.4, relheight=0.12, relx=0.35, rely=0.2)
        self.entryNum.focus()

        # Construct a Monitor Mode Button widget
        self.moni = Button(self.main_menu, text="Start Recording Servers Logs", font="Helvetica 14 bold",
                           command=lambda: self.monitor_mode(self.entryNum.get()), background='PaleTurquoise1')
        self.moni.place(relx=0.2, rely=0.55)

        # Call the mainloop of Tk.
        self.Window.mainloop()

    def monitor_mode(self, num):
        # Destroy this and all descendants widgets.
        self.main_menu.destroy()
        self.layout(num)
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END, menu + "\n\n")
        # self.textCons.config(state=DISABLED)
        self.textCons.see(END)
        sys.stdout = StdoutRedirector(self.textCons)
        Thread(target=main.monitor, daemon=True, args=num).start()

    # The main layout
    def layout(self, num):
        self.num = num
        # to show Monitor Mode window
        self.Window.deiconify()
        self.Window.title("Monitor Mode")
        self.Window.resizable(width=True, height=True)
        self.Window.configure(width=800, height=580, bg='white')

        self.labelHead = Label(self.Window, bg="floral white", pady=5)
        self.labelHead.place(relwidth=1)

        self.line = Label(self.Window, width=450, bg="cyan2")
        self.line.place(relwidth=1, rely=0.07, relheight=0.012)

        # the place where text appears
        self.textCons = Text(self.Window, width=20, height=2, bg="white", fg="black", font="Calibri 14", padx=5,
                             pady=5)
        self.textCons.place(relheight=0.745, relwidth=1, rely=0.08)



        self.labelBottom = Label(self.Window, bg="cyan2", height=80)
        self.labelBottom.place(relwidth=1, rely=0.925)

        # the text above the left box
        self.labelDown = Label(self.Window, bg="pink", fg="black",
                               text="First Date:",
                               font="Calibri 10 bold", pady=8.55)
        self.labelDown.place(relwidth=0.3, rely=0.83, relx=0.05)

        # the text above the right box
        self.labelMsg = Label(self.Window, bg="pink", fg="black",
                              text="Second Date:",
                              font="Calibri 10 bold", pady=8.55)
        self.labelMsg.place(relwidth=0.3, rely=0.83, relx=0.4)

        # the right box
        self.entryRight = Entry(self.labelBottom, bg="floral white", fg="black", font="Calibri 13")
        self.entryRight.place(relwidth=0.35, relheight=0.03, rely=0.0, relx=0.011)
        self.entryRight.focus()

        # the left box
        self.entryLeft = Entry(self.labelBottom, bg="floral white", fg="black", font="Calibri 13")
        self.entryLeft.place(relwidth=0.35, relheight=0.03, rely=0.0, relx=0.38)
        self.entryLeft.focus()

        # create a go Button
        self.buttonManual = Button(self.labelBottom, text="Go", font="Calibri 14 bold", width=20, bg="light blue",
                            fg="black", command=lambda: self.ManualButton(self.entryRight.get(), self.entryLeft.get()))
        self.buttonManual.place(relx=0.77, rely=0.0, relheight=0.03, relwidth=0.22)

        self.textCons.config(cursor="arrow")

        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)

        # place the scroll bar into the gui window
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.config(command=self.textCons.yview)
        self.textCons.config(state=DISABLED)

    def ManualButton(self, date1, date2):
        # self.textCons.config(state=DISABLED)
        self.date1 = date1
        self.date2 = date2
        self.entryRight.delete(0, END)
        self.entryLeft.delete(0, END)
        try:
            main.manualMonitor(date1, date2, self.num)
        except ValueError:
            print("Invalid date,please try again.\n")
            print("\nBack to automatic monitor mode")


if __name__ == '__main__':
    g = GUI()


