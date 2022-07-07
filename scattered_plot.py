"""
Project: Scattered Plot
Author: Alex Griffith
Date: July 07, 2022
Description: A small gui for making 2d and 3d graphs of book data, on variable axes.
"""
import urllib

import plotly.express as px
import pandas as pd
import tkinter as tk
import numpy as np


class Linear_Regression:
    def linear_regression(x, y):
        N = len(x)  # How many data points there are
        x_mean = x.mean()  # X mean
        y_mean = y.mean()  # Y mean

        # Calculate slope of reg line
        B1_num = ((x - x_mean) * (y - y_mean)).sum()
        B1_den = ((x - x_mean) ** 2).sum()
        B1 = B1_num / B1_den

        # Calculate intercept of reg line
        B0 = y_mean - (B1 * x_mean)

        # formatting reg line
        reg_line = 'y = {} + {}β'.format(round(B0, 3), round(B1, 3))

        return B0, B1, reg_line

    def corr_coef(x, y):
        """Calculate the co-efficient of determination, or how well the linear regression line fits the data"""
        N = len(x)

        num = (N * (x * y).sum()) - (x.sum() * y.sum())
        den = np.sqrt((N * (x ** 2).sum() - x.sum() ** 2) * (N * (y ** 2).sum() - y.sum() ** 2))
        R = num / den
        return R

    def start(data, x_name, y_name):
        x = data[x_name]
        y = data[y_name]

        annotation = str('Number of Data Points: ' + str(len(x)))
        try:
            B0, B1, reg_line = Linear_Regression.linear_regression(x, y)
            R = Linear_Regression.corr_coef(x, y)

            annotation += str('<br>Regression Line: ' + reg_line)
            annotation += str('<br>Correlation Coefficient: ' + str(round(R, 3)))
            annotation += str('<br>Goodness of Fit: ' + str(round(R ** 2, 3)))
        except (ZeroDivisionError, TypeError):
            annotation += "<br>Cannot Calculate Linear Regression Without Numerical Columns"

        return annotation


class Graphical_UI(tk.Frame):
    """
    Class that generates a GUI for easier use and entering of options.
    """

    df: pd.DataFrame = None

    def __init__(self, master=None):
        """
        Creates all the initial parameters for the listbox.
        Binds the 'Return' key to generating a new graph based on the current input parameters.
        :param master: the root of the window
        """
        super().__init__(master)
        self.frame = tk.Frame(root, padx=10, pady=10)
        self.top = None

        df = pd.read_csv('dataset/books.csv')
        AXES = list(df.columns)

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
        self.series_number = tk.IntVar(self.top)
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
        self.published = tk.IntVar(self.top)
        self.added_by = tk.StringVar(self.top)

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

        tk.Label(self.frame, text="X Axis Data: ", padx=5, pady=5).grid(row=0, column=0)
        tk.Label(self.frame, text="Y Axis Data: ", padx=5, pady=5).grid(row=1, column=0)
        tk.Label(self.frame, text="Graph Third Axis", padx=5, pady=5).grid(row=2, column=0)
        tk.Label(self.frame, text="Z Axis Data: ", padx=5, pady=5).grid(row=3, column=0)
        tk.Label(self.frame, text="Colour Gradient Data: ", padx=5, pady=5).grid(row=4, column=0)

        tk.Button(self.master, text="Generate graph", padx=5, pady=5,
                  command=lambda: generate_graph()).grid(row=5, column=1, columnspan=1)

        def generate_graph():
            df = get_book_data()
            if self.three_axis_graph.get() == 1:
                graph = px.scatter_3d(df, x=self.axis_one.get(), y=self.axis_two.get(), z=self.axis_three.get(),
                                      color=self.colour.get(), hover_name='Book',
                                      hover_data=['Author', 'Series', 'Series Number'], template="plotly_dark")

            else:
                graph = px.scatter(df, x=self.axis_one.get(), y=self.axis_two.get(), color=self.colour.get(),
                                   hover_name='Book', hover_data=['Author', 'Series', 'Series Number'],
                                   template="plotly_dark")

                # A two axis graph will also plot the linear regression
                annotation = Linear_Regression.start(df, self.axis_one.get(), self.axis_two.get())
                graph.add_annotation(showarrow=False, xanchor="left", yanchor="top", xref="paper", yref="paper", x=0.05,
                                     y=0.95, text=annotation, align="left")
            graph.show()

        def get_book_data():
            if self.df is not None:
                return self.df
            try:
                url = "https://docs.google.com/spreadsheets/d/18bKBAJkIEXZEw0K-nC2re8Zav2TOFV0rfPLW3j7OjHo/export?gid" \
                      "=280213473&format=csv"
                print('Connecting to: ', url)
                df = pd.read_csv(url)
                print('Data Received.')
                self.df = df
                write_book_data()
                print('Offline data has been updated.')
            except urllib.error.URLError:
                print('Cannot connect to live data, using most recent stored data.\n')
                df = pd.read_csv('dataset/books.csv', )

            return df

        def write_book_data():
            self.df.to_csv('dataset/books.csv', index=False)


root = tk.Tk()
gui = Graphical_UI(master=root)
root.geometry("350x220")
root.title("Scattered Plot")
root.iconbitmap('book_icon.ico')
gui.mainloop()
