"""
Project: Scattered Plot
Author: Alex Griffith
Date: Jan. 13th, 2022
Description: A small gui for making 3d graphs of book data, on variable axes.

TODO:   Add a window for inserting new books.
"""

import plotly.express as px
import pandas as pd
import tkinter as tk


class Graphical_UI(tk.Frame):
    """
    Class that generates a GUI for easier use and entering of options.
    """

    def __init__(self, master=None):
        """
        Creates all the initial parameters for the listbox.
        Binds the 'Return' key to generating a new set of NPC's based on the current input parameters.
        :param master: the root of the window
        """
        super().__init__(master)
        self.frame = tk.Frame(root, padx=10, pady=10)
        self.top = None

        AXES = [
            "Low Magic - High Magic",
            "Low Fantasy - High Fantasy",
            "Dark - Bright",
            "Grim - Noble",
            "Page Count",
            "Word Count",
            "Sad - Happy",
            "Calm - Passionate",
            "Goodreads",
            "Series"
        ]

        self.axis_one = tk.StringVar(master)
        self.axis_one.set(AXES[0])
        self.axis_two = tk.StringVar(master)
        self.axis_two.set(AXES[1])
        self.axis_three = tk.StringVar(master)
        self.axis_three.set(AXES[2])
        self.colour = tk.StringVar(master)
        self.colour.set(AXES[8])
        self.three_axis_graph = tk.IntVar()

        self.book = tk.StringVar(self.top)
        self.series = tk.StringVar(self.top)
        self.author = tk.StringVar(self.top)
        self.magic = tk.DoubleVar(self.top)
        self.fantasy = tk.DoubleVar(self.top)
        self.grim_noble = tk.DoubleVar(self.top)
        self.dark_bright = tk.DoubleVar(self.top)
        self.sad_happy = tk.DoubleVar(self.top)
        self.calm_passionate = tk.DoubleVar(self.top)
        self.word_count = tk.IntVar(self.top)
        self.page_count = tk.IntVar(self.top)
        self.goodreads = tk.DoubleVar(self.top)

        self.create_widgets(AXES)

    def create_widgets(self, AXES):
        """
        creates all the widgets and buttons in the window.
        """
        self.frame.grid(row=0, column=0, columnspan=2, rowspan=4)

        tk.OptionMenu(self.frame, self.axis_one, *AXES).grid(row=0, column=1)
        tk.OptionMenu(self.frame, self.axis_two, *AXES).grid(row=1, column=1)
        tk.Checkbutton(self.frame, variable=self.three_axis_graph).grid(row=2, column=1)
        tk.OptionMenu(self.frame, self.axis_three, *AXES).grid(row=3, column=1)
        tk.OptionMenu(self.frame, self.colour, *AXES).grid(row=4, column=1)

        tk.Label(self.frame, text="Axis One Data: ", padx=5, pady=5).grid(row=0, column=0)
        tk.Label(self.frame, text="Axis Two Data: ", padx=5, pady=5).grid(row=1, column=0)
        tk.Label(self.frame, text="Graph Third Axis", padx=5, pady=5).grid(row=2, column=0)
        tk.Label(self.frame, text="Axis Three Data: ", padx=5, pady=5).grid(row=3, column=0)
        tk.Label(self.frame, text="Colour Gradient Data: ", padx=5, pady=5).grid(row=4, column=0)

        tk.Button(self.master, text="Generate graph", padx=5, pady=5,
                  command=lambda: generate_graph()).grid(row=5, column=0, columnspan=1)
        tk.Button(self.master, text="Add New Book", padx=5, pady=5,
                  command=lambda: insert_new_book()).grid(row=5, column=1, columnspan=1)

        def generate_graph():
            df = get_book_data()

            if self.three_axis_graph.get() == 1:
                graph = px.scatter_3d(df, x=self.axis_one.get(), y=self.axis_two.get(), z=self.axis_three.get(),
                                      color=self.colour.get(), hover_name='Book', hover_data=['Author', 'Series'], template="plotly_dark")
            else:
                graph = px.scatter(df, x=self.axis_one.get(), y=self.axis_two.get(), color=self.colour.get(),
                                   hover_name='Book', hover_data=['Author', 'Series'], template="plotly_dark")

            graph.show()

        def get_book_data():
            df = pd.read_csv('dataset/books.csv')
            return df

        def write_book_data():
            df = get_book_data()
            df.loc[len(df.index)] = [self.book.get(), self.series.get(), self.author.get(), self.magic.get(),
                                     self.fantasy.get(), self.grim_noble.get(), self.dark_bright.get(),
                                     self.sad_happy.get(), self.calm_passionate.get(), self.word_count.get(),
                                     self.page_count.get(), self.goodreads.get()]
            df.to_csv('dataset/books.csv', index=False)

        def submit_new_book():
            write_book_data()
            self.top.destroy()

        def insert_new_book():
            self.top = tk.Toplevel(root)
            self.top.title("Add A New Book")
            self.top.geometry("355x390")

            tk.Label(self.top, text="Book Name: ", padx=5, pady=5).grid(row=0, column=0)
            tk.Label(self.top, text="Series: ", padx=5, pady=5).grid(row=1, column=0)
            tk.Label(self.top, text="Author: ", padx=5, pady=5).grid(row=2, column=0)
            tk.Label(self.top, text="Low Magic - High Magic [0-10]: ", padx=5, pady=5).grid(row=3, column=0)
            tk.Label(self.top, text="Low Fantasy - High Fantasy [0-10]: ", padx=5, pady=5).grid(row=4, column=0)
            tk.Label(self.top, text="Characters are... Grim - Noble [0-10]: ", padx=5, pady=5).grid(row=5, column=0)
            tk.Label(self.top, text="World is... Dark - Bright [0-10]: ", padx=5, pady=5).grid(row=6, column=0)
            tk.Label(self.top, text="It made me feel... Sad - Happy [0-10]: ", padx=5, pady=5).grid(row=7, column=0)
            tk.Label(self.top, text="It made me... Calm - Passionate [0-10]: ", padx=5, pady=5).grid(row=8, column=0)
            tk.Label(self.top, text="Word Count: ", padx=5, pady=5).grid(row=9, column=0)
            tk.Label(self.top, text="Page Count: ", padx=5, pady=5).grid(row=10, column=0)
            tk.Label(self.top, text="Goodreads [0-5]: ", padx=5, pady=5).grid(row=11, column=0)

            tk.Entry(self.top, textvariable=self.book).grid(row=0, column=1)
            tk.Entry(self.top, textvariable=self.series).grid(row=1, column=1)
            tk.Entry(self.top, textvariable=self.author).grid(row=2, column=1)
            tk.Entry(self.top, textvariable=self.magic).grid(row=3, column=1)
            tk.Entry(self.top, textvariable=self.fantasy).grid(row=4, column=1)
            tk.Entry(self.top, textvariable=self.grim_noble).grid(row=5, column=1)
            tk.Entry(self.top, textvariable=self.dark_bright).grid(row=6, column=1)
            tk.Entry(self.top, textvariable=self.sad_happy).grid(row=7, column=1)
            tk.Entry(self.top, textvariable=self.calm_passionate).grid(row=8, column=1)
            tk.Entry(self.top, textvariable=self.word_count).grid(row=9, column=1)
            tk.Entry(self.top, textvariable=self.page_count).grid(row=10, column=1)
            tk.Entry(self.top, textvariable=self.goodreads).grid(row=11, column=1)

            tk.Button(self.top, text="Submit", padx=5, pady=5,
                      command=lambda: submit_new_book()).grid(row=12, column=0, columnspan=2)


root = tk.Tk()
gui = Graphical_UI(master=root)
root.geometry("350x220")
root.title("Scattered Plot")
root.iconbitmap('book_icon.ico')
gui.mainloop()
