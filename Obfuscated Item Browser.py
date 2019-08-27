#!/usr/bin/env python
# coding: utf-8

import os
import psutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
import tkinter.ttk as ttk
import gc
from bokeh.palettes import Category20_20
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import Counter
from matplotlib.transforms import Bbox
from win32api import GetSystemMetrics


class ____Brower():
    """
    GUI ____ Browser application for browsing ____ population of output
    csv from ____ engine (evaluated _____ set after running through ____
    engine). Displays individual ____s, with either the number of _____s
    it evaluated or the total _____ score that it _____d, and the ___ it
    _____d to. GUI consists of a interactive plot of this information, a
    vertical line cursor used to scroll through the ____s in the plot,
    and buttons to control both the view of the plot, the plot type to view,
    and the cursor. GUI primarily can be used to find a specific ____ that
    can be changed  move some desired number of _____s or some amount
    of _____ score to another destination ___ (e.g. want to move 5 _____s
    from ___ _______ to _______)

    Attributes
    ---
    parent : tk.Tk
        Parent root window widget for all widgets. Can be called to run
        mainloop of application.
    font : tuple of (str, float)
        Tuple of font and fontsize for labels and text display
        (font, fontsize).
    padx : int
        X-direction padding for widgets for grid.
    pady : int
        Y-direction padding for widgets for grid.
    leftfive : ttk.Button
        Button to increment cursor left five ____s.
    leftone : ttk.Button
        Button to increment cursor left one ____s.
    rightone : ttk.Button
        Button to increment cursor right one ____s.
    rightfive : ttk.Button
        Button to increment cursor right five ____s.
    zoomin : ttk.Button
        Button to zoom in to y axis of plot.
    zoomout : ttk.Button
        Button to zoom out of y axis of plot.
    resetbutton : ttk.Button
        Button to reset plot view to original view.
    quit : ttk.Button
        Button to properly quit application.
    enlargebutton : ttk.Button
        Button to enlarge plot by ten percent.
    reducebutton : ttk.Button
        Button to reduce plot by ten percent.
    switchscorecount : ttk.Button
        Button to switch y axis from _____ count to _____ score or vice versa.
    textdisplay : ScrolledText
        Scrolled text widget for displaying the ____ that the cursor is
        currently placed on.
    fig : plt.Figure
        Figure for ____ plot.
    ax : plt.Axes()
        Axes for ____ plot.
    ax_ylim_orig :
        Upper limit of y for the original plotting of ____ plot, for
        reverting back to original view.
    xlim : tuple of float
        Lower and upper bounds for arbitary ____ index for ____s. Used
        to prevent cursor from overshooting ____s.
    ylim : int
        Current upper limit of y.
    ax_ylim_orig : float
        Original upper y limit for current plot.
    scalenumfory : float
        Amount to scale ax_ylim_orig by to get current ylim.
    blankcanvas : FigureCanvasTkAgg
        Blank canvas to prevent application from constricting upon canvas
        clearing/destroy.
    canvas : FigureCanvasTkAgg
        Canvas widget for ____ plot.
    legendcanvas : FigureCanvasTkAgg
        Canvas widget for legend for ____ plot.
    linex : int
        Current x position of vertical scrolling line.
    dpi : int
        Calculated dpi for screen.
    plotscale : float
        Percent of screen that pre stickied plot should take up.
    ____info____grouped : list of tuple of (str, str, str, str, str)
        List of tuples containing info for each ____, in form of
        (___ key, ___ _____d to, ___ ____ Category, N _____s _____d,
        Total _____ Score _____d). Grouped by ___, in the same order
        as enumeration of items in ________count____grouped.
    ________count____grouped : list of tuple of
                               (str, list of tuple of (int, int))
        List of tuples of ___ and enumerated counts of ____s that _____ to
        that ___. Data is in form of list of tuple of (___,
        list of tuple of (____ Index, N _____s _____d)). Used for
        plotting such that each associated ____ index and _____s _____d
        count, would correspond to the ____ of the same index in
        ____info____grouped, such that reference in the plot could point
        to the correct ____ info.
    ____info2____grouped : list of tuple of (str, str, str, str, str)
        List of tuples containing info for each ____, in form of
        (___ key, ___ _____d to, ___ ____ Category, N _____s _____d,
        Total _____ Score _____d). Grouped by ___, in the same order
        as enumeration of items in ________score____grouped.
    ________score____grouped : list of tuple of
                               (str, list of tuple of (int, int))
        List of tuples of ___ and enumerated total _____ score of ____
        that _____d to that ___. Data is in form of list of tuple of (___,
        list of tuple of (____ Index, Total _____ Score _____d)). Used for
        plotting such that each associated ____ index and _____s _____d
        count, would correspond to the ____ of the same index in
        ____info2____grouped, such that reference in the plot could point
        to the correct ____ info.
    ____line : matplotlib.lines.Line2D
        Vertical selection cursor line for plot.
    legendreference : list of tuple of (str, plt.Artist)
        List of labels and handles for plotting legend in seperate figure.
    active_plot : str
        Either _____count or _____score, states the current active plot in
        the GUI.
    user_warned : bool
        States whether user has been warned yet about high RAM consumption.
    initial_bg_canvas : FigureCanvasTkAgg
        Initial canvas for saving background.
    canvas_bg : matplotlib.BufferRegion
        Saved background for plot, for blit.
    ___colorreference : dict
        Lookup dictionary for consistency of ___ and color, so legend does
        not have to be redrawn.
    legend___namelookup : dict
        Lookup dictionary for assigning ___Keys proper names.

    """
    def __init__(self, parent, output_csv, plot_screen_percent=0.6):
        """
        Constructor for ____Browser Class, does following:
            - Loads in ____ engine output csv.
            - Builds widgets of application and specifies their functionality
              and style.
            - Performs counts of ____s' n _____s _____d, organizing by ___,
              and sorting by volume of _____s for ____ to increase plot
              readability
            - Performs sum of ____s' total _____ scores _____d, organizing
              by ___, and sorting by total _____ score _____df to increase
              plot readability.
            - Creates interactive plot and establishs cursor, specifying
              limitations, live updating of visuals, and updating of text
              based on cursor placement.

        Parameters
        ---
        parent : tk.Tk
            Parent root window widget for all widgets to be built upon.
        output_csv : str
            Path to ____ engine output CSV.
        plot_screen_percent : float, optional
            Size of plot, in percentage of screen.

        """
        # Initial parent set up
        self.parent = parent
        self.parent.title("Obfuscated Item Browser")

        # Set style for parent
        plt.style.use('seaborn')
        style = ttk.Style(self.parent)
        style.theme_use('clam')
        style.configure('TButton', font=('default', 10))
        self.font = ('default', 11)
        self.padx = 10
        self.pady = 5

        # Add instructions menu
        menu = tk.Menu(self.parent)
        menu.add_command(label='Help',
                         command=self.instructions_message)
        self.parent.config(menu=menu)

        # Fine tuning increment Buttons
        tk.Label(text='Fine Line Movement', font=self.font).grid(
            column=1, columnspan=4, row=0)

        self.leftfive = ttk.Button(
            text='<<', command=lambda: self.increment_line(-5))
        self.leftfive.configure(state='disabled')
        self.leftfive.grid(
            column=1, row=1, sticky="WE", padx=self.padx, pady=self.pady)

        self.leftone = ttk.Button(
            text='<', command=lambda: self.increment_line(-1))
        self.leftone.configure(state='disabled')
        self.leftone.grid(
            column=2, row=1, sticky="WE", padx=self.padx, pady=self.pady)

        self.rightone = ttk.Button(
            text='>', command=lambda: self.increment_line(1))
        self.rightone.configure(state='disabled')
        self.rightone.grid(
            column=3, row=1, sticky="WE", padx=self.padx, pady=self.pady)

        self.rightfive = ttk.Button(
            text='>>', command=lambda: self.increment_line(5))
        self.rightfive.configure(state='disabled')
        self.rightfive.grid(
            column=4, row=1, sticky="WE", padx=self.padx, pady=self.pady)

        # Zoom in zoom out on y axis Buttons
        self.zoomin = ttk.Button(
            text='Zoom In Y', command=lambda: self.scale_y('reduce'))
        self.zoomin.configure(state='disabled')
        self.zoomin.grid(
            column=1, row=2, sticky="WE", padx=self.padx, pady=self.pady)

        self.zoomout = ttk.Button(
            text='Zoom Out Y', command=lambda: self.scale_y('enlarge'))
        self.zoomout.configure(state='disabled')
        self.zoomout.grid(
            column=2, row=2, sticky="WE", padx=self.padx, pady=self.pady)

        # Enlarge/Reduce plot Buttons
        self.enlargebutton = ttk.Button(
            text='Expand Plot', command=lambda: self.resize_plot(0.1))
        self.enlargebutton.configure(state='disabled')
        self.enlargebutton.grid(
            column=4, row=2, sticky="WE", padx=self.padx, pady=self.pady)

        self.reducebutton = ttk.Button(
            text='Reduce Plot', command=lambda: self.resize_plot(-0.1))
        self.reducebutton.configure(state='disabled')
        self.reducebutton.grid(
            column=3, row=2, sticky="WE", padx=self.padx, pady=self.pady)

        # Switch y axis button
        self.switchscorecount = ttk.Button(
            text='Switch Item Value/Item Count',
            command=self.switch_plot)
        self.switchscorecount.configure(state='disabled')
        self.switchscorecount.grid(
            column=1, row=3, columnspan=2, sticky="WE",
            padx=self.padx, pady=self.pady)

        # Reset Button
        self.resetbutton = ttk.Button(
            text='Reset View', command=self.reset_plot,)
        self.resetbutton.configure(state='disabled')
        self.resetbutton.grid(
            column=3, row=3, sticky="WE", padx=self.padx, pady=self.pady)

        # Quit Button
        self.quit = ttk.Button(
            text='Quit', command=self.true_quit)
        self.quit.configure(state='disabled')
        self.quit.grid(
            column=4, row=3, sticky="WE", padx=self.padx, pady=self.pady)

        # Scrolling message box for current ____
        self.textdisplay = ScrolledText(
            self.parent, width=50, height=20, state=tk.DISABLED,
            font=self.font)
        self.textdisplay.grid(
            column=1, row=4, columnspan=4, padx=self.padx, pady=self.pady,
            sticky='WE')

        # Bind arrow keys to increment
        self.parent.bind(
            '<Left>',
            lambda event: self.sudo_press_button(self.leftone))
        self.parent.bind(
            '<Right>',
            lambda event: self.sudo_press_button(self.rightone))
        self.parent.bind(
            '<Up>',
            lambda event: self.sudo_press_button(self.rightfive))
        self.parent.bind(
            '<Down>',
            lambda event: self.sudo_press_button(self.leftfive))
        self.parent.bind(
            '<KeyRelease-Left>',
            lambda event: self.leftone.state(['!pressed']))
        self.parent.bind(
            '<KeyRelease-Right>',
            lambda event: self.rightone.state(['!pressed']))
        self.parent.bind(
            '<KeyRelease-Up>',
            lambda event: self.rightfive.state(['!pressed']))
        self.parent.bind(
            '<KeyRelease-Down>',
            lambda event: self.leftfive.state(['!pressed']))

        # Bind wasd keys to increment
        self.parent.bind(
            '<a>',
            lambda event: self.sudo_press_button(self.leftone))
        self.parent.bind(
            '<d>',
            lambda event: self.sudo_press_button(self.rightone))
        self.parent.bind(
            '<w>',
            lambda event: self.sudo_press_button(self.rightfive))
        self.parent.bind(
            '<s>',
            lambda event: self.sudo_press_button(self.leftfive))
        self.parent.bind(
            '<KeyRelease-a>',
            lambda event: self.leftone.state(['!pressed']))
        self.parent.bind(
            '<KeyRelease-d>',
            lambda event: self.rightone.state(['!pressed']))
        self.parent.bind(
            '<KeyRelease-w>',
            lambda event: self.rightfive.state(['!pressed']))
        self.parent.bind(
            '<KeyRelease-s>',
            lambda event: self.leftfive.state(['!pressed']))

        # Store dpi
        self.dpi = int(GetSystemMetrics(0) /
                       (self.parent.winfo_screenmmwidth()/25.4))

        # Set up blank canvas behind canvas, so canvas destroys do
        # not shrink window
        self.plotscale = plot_screen_percent
        self.plot_blankcanvas(self.plotscale)

        # Set initial parameters for vertical ____s line
        self.linex = 0

        # Set initial scaling for y axis
        self.scalenumfory = 1.

        # Load data for plotting
        chunked_csv = pd.read_csv(output_csv,
                                  delimiter=',',
                                  chunksize=10000,
                                  encoding='UTF-8')
        _______keys = []
        ___s = []
        ___names = []
        ________priorities = []
        _____s_scores = []
        for chunk in chunked_csv:

            # Since _______key must be unique to each ___, convert any nan entry to
            # No ___ ____ Key (___KEY)
            chunk_______key = chunk['_______ID'].astype(str).copy()
            chunk___s = chunk['___Key_1'].astype(str).copy()
            nanindices = chunk_______key == 'nan'
            nanindices___s = chunk___s[nanindices]
            nanstrings = nanindices___s.map(lambda s: 'No ____ ID ___ {}'.format(s))
            chunk_______key[nanindices] = nanstrings

            # Append listed chunks to larger list
            _______keys += list(chunk_______key)
            ___s += list(chunk___s)
            ___names += list(chunk['___Name_1'].astype(str))
            ________priorities += list(chunk['_______Hierarchy'].astype(str))
            _____s_scores += list(chunk['_____ScoreAtLatest________'])

        # Make up lookup for ___ name and ___ key for legend
        self.legend___namelookup = dict(list(set(list(zip(___s, ___names)))))

        # Count number of occurrences of each ____ in output
        ____count_obj = Counter(zip(_______keys, ___s, ___names, ________priorities))
        ____info_count = []
        for key in ____count_obj.keys():
            ____info_count.append((key, ____count_obj[key]))

        # Convert _______keys, ___s and ______scores into
        # arrays for ease in finding and summing scores
        _______keys_arr = np.array(_______keys)
        ___s_arr = np.array(___s)
        _____s_scores_arr = np.array(_____s_scores)

        # Sum total _____ score for each ____ in output
        ____info2_score = []
        for key in ____count_obj.keys():
            _______key_temp = key[0]
            relevant_indices = _______keys_arr == _______key_temp
            relevant_scores = _____s_scores_arr[relevant_indices]
            ____info2_score.append((key, round(np.sum(relevant_scores), 2)))

        # Convert both into a lookup dictionary of ____key
        # and either _____ count or _____ score
        count_lookup = dict([(____info[0], count)
                             for ____info, count in ____info_count])
        score_lookup = dict([(____info2[0], score)
                             for ____info2, score in ____info2_score])

        # For each of both ____info count/score lists, append the opposite
        # score or count for later text display
        ____info_count = [((____info[0],
                            ____info[1],
                            ____info[2],
                            ____info[3],
                            score_lookup[____info[0]]),
                           count) for ____info, count in ____info_count]
        ____info2_score = [((____info2[0],
                             ____info2[1],
                             ____info2[2],
                             ____info2[3],
                             count_lookup[____info2[0]]),
                            score) for ____info2, score in ____info2_score]

        # Get Unique ___s and count n _____s for each
        ___s = [____info[1] for ____info, count in ____info_count]
        ___count_obj = Counter(___s)
        unique____s = ___count_obj.keys()
        counts_for____s = [___count_obj[____temp] for ____temp in unique____s]

        # Using unique ___s, get total _____ score for each
        unique____s2 = list(unique____s).copy()
        ___totalscores = []
        for ____temp in unique____s2:
            relevant_indices = ___s_arr == ____temp
            relevant_scores = _____s_scores_arr[relevant_indices]
            ___totalscores.append(np.sum(relevant_scores))

        # Prememptively sort ___s by n _____s and total _____ scores
        # going to each so that higher _____ volumes are first,
        # and thus later are plotted first
        unique____s = list(np.array(list(unique____s))[
            np.flipud(np.argsort(counts_for____s))])
        unique____s2 = list(np.array(list(unique____s2))[
            np.flipud(np.argsort(___totalscores))])

        # Seperate into a list for plotting and a list for referencing
        # ____info from cursor placement
        ____info____grouped = []
        ________count____grouped = []
        last_enumerated_index = 0
        for ____temp in unique____s:

            relevant_____info_count = [(____info, count)
                                       for ____info, count in ____info_count
                                       if ____info[1] == ____temp]

            count_temp = np.array(
                [count for ____info, count in relevant_____info_count])

            # Remake ____info such that count is also included as info and
            # also such that score follows count
            ____info_temp = np.array(
                 [(____info[0], ____info[1], ____info[2], ____info[3],
                   count, ____info[4])
                  for ____info, count in relevant_____info_count])

            sorted_indices = np.flipud(np.argsort(count_temp))
            count_temp = list(count_temp[sorted_indices])
            ____info_temp = list(____info_temp[sorted_indices])

            # Enumerate count with consistent unique index with other ___
            # grouped lists, by updating last_enumerated_index, for
            # plotting and text reference in application
            ind_count = list(enumerate(count_temp, last_enumerated_index))
            last_enumerated_index += len(count_temp)

            ____info____grouped += ____info_temp
            ________count____grouped.append((____temp, ind_count))

        # Make another similar set of data for _____ score
        ____info2____grouped = []
        ________score____grouped = []
        last_enumerated_index = 0
        for ____temp in unique____s2:

            relevant_____info2_score = [(____info2, score)
                                        for ____info2, score in ____info2_score
                                        if ____info2[1] == ____temp]

            score_temp = np.array(
                [score for ____info2, score in relevant_____info2_score])

            # Remake ____info2 such that score is also included as info and
            # also such that score immediately follows count
            ____info2_temp = np.array(
                 [(____info2[0], ____info2[1], ____info2[2],
                   ____info2[3], ____info2[4], score)
                  for ____info2, score in relevant_____info2_score])

            sorted_indices = np.flipud(np.argsort(score_temp))
            score_temp = list(score_temp[sorted_indices])
            ____info2_temp = list(____info2_temp[sorted_indices])

            # Enumerate score with consistent unique index with other ___
            # grouped lists, by updating last_enumerated_index, for
            # plotting and text reference in application
            ind_count = list(enumerate(score_temp, last_enumerated_index))
            last_enumerated_index += len(score_temp)

            ____info2____grouped += ____info2_temp
            ________score____grouped.append((____temp, ind_count))

        # Define as object attributes for use in plots and text reference
        self.____info____grouped = ____info____grouped.copy()
        self.________count____grouped = ________count____grouped.copy()
        self.____info2____grouped = ____info2____grouped.copy()
        self.________score____grouped = ________score____grouped.copy()

        # Set attribute stating that current plot is the count plot
        self.active_plot = "_____count"

        # Track if user has been warned yet about memory consumption
        self.user_warned = False

        # Plot initial ____ plot as count plot, and legend
        self.plot_____countplot()
        self.plot_legend()

        # Blit affects blank canvas scaling so refresh and do plot again
        # so that plot is as big as possible (plot is based on blank
        # canvas scaling)
        self.refresh_____plot()
        self.reset_plot()

        self.parent.geometry(
            "+{}+{}".format(int(GetSystemMetrics(0)/2 -
                                self.parent.winfo_width()/2),
                            int(GetSystemMetrics(1)/2 -
                                self.parent.winfo_height()/2)))
        self.parent.lift()

    def check_memory(self):
        """ Check memory to see if is over 1 Gb, and notify user of
        potential instability after it hits it, once.

        """
        if not self.user_warned:
            process = psutil.Process(os.getpid())
            mem_in_gb = process.memory_info()[0]/2**30
            if mem_in_gb > 1.:
                messagebox.showinfo('Warning',
                                    ('Item browser is now occupying over 1'
                                     ' Gb of RAM and may be unstable. An'
                                     ' application reset is recommended.'
                                     ' If app is not reset, potential crash'
                                     ' may occur.'))
                self.user_warned = True
        else:
            pass

    def clear_memory(self):
        """ Clear memory of all previously existing figures, axes, and
        canvases if they exist, and call garbage collection to clear
        any unreferenced objects.

        """
        if hasattr(self, 'ax'):
            self.ax.cla()
        if hasattr(self, 'fig'):
            self.fig.clf()
        if hasattr(self, 'initial_bg_canvas'):
            self.initial_bg_canvas.get_tk_widget().destroy()
            self.initial_bg_canvas.figure.clf()
            del(self.initial_bg_canvas)
        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().destroy()
            self.canvas.figure.clf()
            del(self.canvas)
        if hasattr(self, 'canvas_bg'):
            del(self.canvas_bg)
        plt.close('all')
        gc.collect(0)
        gc.collect(1)
        gc.collect(2)

    def plot_blankcanvas(self, percentofscreen):
        """ Plots a blank canvas where ____ plot will be placed to prevent
        window shrinkage.

        """
        fig = plt.figure(
            figsize=(percentofscreen*GetSystemMetrics(0)/self.dpi,
                     percentofscreen*GetSystemMetrics(1)/self.dpi))
        self.blankcanvas = FigureCanvasTkAgg(fig, master=self.parent)
        self.blankcanvas.get_tk_widget().configure(relief='sunken', bd=1)
        self.blankcanvas.get_tk_widget().grid(
            column=0, row=0, rowspan=6, padx=self.padx, pady=self.pady,
            sticky='NSWE')

    def plot_____countplot(self):
        """ Plot ____ plot of _____ counts alongside vertical cursor line,
        based on data loaded from csv in constructor.

        """
        # Clear RAM of previous unecessary plots
        self.clear_memory()

        # Set figuresize as size of blank canvas post sticky
        self.parent.update_idletasks()  # Update size of blank canvas
        self.fig, self.ax = plt.subplots(
            figsize=((self.blankcanvas.get_tk_widget().winfo_width()-2) /
                     self.dpi,
                     (self.blankcanvas.get_tk_widget().winfo_height()-2) /
                     self.dpi))
        self.fig.set_dpi(self.dpi)
        self.fig.tight_layout(pad=4.)

        # Create legend reference and save to it if it does not exist yet
        if not hasattr(self, 'legendreference'):
            # Since legend creation is first plotting, also save
            # a color reference for score plotting so that ___ colors
            # match
            self.legendreference = []
            ___colorreference = []
            for index in range(len(self.________count____grouped)):
                ____temp, ind_count_temp = self.________count____grouped[index]
                arr_temp = np.array(ind_count_temp)
                bars = self.ax.bar(arr_temp[:, 0], arr_temp[:, 1],
                                   color=Category20_20[index], width=1.,
                                   label=____temp, align='center')
                last_used_index = arr_temp[:, 0][-1]
                self.legendreference.append((____temp, bars.patches[0]))
                ___colorreference.append((____temp, Category20_20[index]))
            self.___colorreference = dict(___colorreference)
        else:
            for index in range(len(self.________count____grouped)):
                ____temp, ind_count_temp = self.________count____grouped[index]
                arr_temp = np.array(ind_count_temp)
                self.ax.bar(arr_temp[:, 0], arr_temp[:, 1],
                            color=Category20_20[index], width=1.,
                            label=____temp, align='center')
                last_used_index = arr_temp[:, 0][-1]

        self.ax.margins(x=0.01)
        self.ax.locator_params(axis='both', nbins=20)
        self.ax.set_ylabel('Number of Items')
        self.ax.set_xlabel('Arbitrary Individual Item Index')

        # Check if set_ylim is set yet for replotting on zoom in/out
        if hasattr(self, 'ylim'):
            self.ax.set_ylim(0, self.ylim)
        # If not set, means first plotting of ____ plot, so save y limit of
        # original for future zooming
        else:
            self.ax_ylim_orig = self.ax.get_ylim()[1]
            self.ylim = self.ax_ylim_orig*self.scalenumfory

        # Set to 0 and last used index, which is final index for use in
        # limiting overshooting cursor
        self.xlim = (0, last_used_index)

        # Save background for blit without line
        self.initial_bg_canvas = FigureCanvasTkAgg(self.fig,
                                                   master=self.parent)
        self.initial_bg_canvas.draw()
        self.canvas_bg = self.initial_bg_canvas.copy_from_bbox(
            self.initial_bg_canvas.get_tk_widget().bbox('all'))

        # Clear the just generated canvas
        self.initial_bg_canvas.get_tk_widget().delete('all')
        self.initial_bg_canvas.get_tk_widget().destroy()

        # Draw ____ line (slightly smaller than ylim, to account for smear)
        self.____line = self.ax.axvline(
            self.linex, color='black', linestyle='--', ymin=0.005, ymax=0.995,
            lw=.8)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.parent)
        self.canvas.get_tk_widget().grid(
             column=0, row=0, rowspan=6, padx=self.padx, pady=self.pady)

        # Connect click to matplotlib
        self.canvas.mpl_connect('button_press_event', self.click_line)

        # Check if at high RAM
        self.check_memory()

    def plot_____scoreplot(self):
        """ Plot ____ plot of _____ scores alongside vertical cursor line,
        based on data loaded from csv in constructor.

        """
        # Clear RAM of previous unecessary plots
        self.clear_memory()

        # Set figuresize as size of blank canvas post sticky
        self.parent.update_idletasks()  # Update size of blank canvas
        self.fig, self.ax = plt.subplots(
            figsize=((self.blankcanvas.get_tk_widget().winfo_width()-2) /
                     self.dpi,
                     (self.blankcanvas.get_tk_widget().winfo_height()-2) /
                     self.dpi))
        self.fig.set_dpi(self.dpi)
        self.fig.tight_layout(pad=4.)

        for index in range(len(self.________score____grouped)):
            ____temp, ind_count_temp = self.________score____grouped[index]
            arr_temp = np.array(ind_count_temp)
            self.ax.bar(arr_temp[:, 0], arr_temp[:, 1],
                        color=self.___colorreference[____temp], width=1.,
                        label=____temp, align='center')
            last_used_index = arr_temp[:, 0][-1]

        self.ax.margins(x=0.01)
        self.ax.locator_params(axis='both', nbins=20)
        self.ax.set_ylabel('Total Item Value')
        self.ax.set_xlabel('Arbitrary Individual Item Index')

        # Check if set_ylim is set yet for replotting on zoom in/out
        if hasattr(self, 'ylim'):
            self.ax.set_ylim(0, self.ylim)
        # If not set, means first plotting of ____ plot, so save y limit of
        # original for future zooming
        else:
            self.ax_ylim_orig = self.ax.get_ylim()[1]
            self.ylim = self.ax_ylim_orig*self.scalenumfory

        # Set to 0 and last used index, which is final index for use in
        # limiting overshooting cursor
        self.xlim = (0, last_used_index)

        # Save background for blit without line
        self.initial_bg_canvas = FigureCanvasTkAgg(self.fig,
                                                   master=self.parent)
        self.initial_bg_canvas.draw()
        self.canvas_bg = self.initial_bg_canvas.copy_from_bbox(
            self.initial_bg_canvas.get_tk_widget().bbox('all'))

        # Clear the just generated canvas
        self.initial_bg_canvas.get_tk_widget().delete('all')
        self.initial_bg_canvas.get_tk_widget().destroy()

        # Draw ____ line (slightly smaller than ylim, to account for smear)
        self.____line = self.ax.axvline(
            self.linex, color='black', linestyle='--', ymin=0.005, ymax=0.995,
            lw=.8)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.parent)
        self.canvas.get_tk_widget().grid(
             column=0, row=0, rowspan=6, padx=self.padx, pady=self.pady)

        # Connect click to matplotlib
        self.canvas.mpl_connect('button_press_event', self.click_line)

        # Check if at high RAM
        self.check_memory()

    def plot_legend(self):
        """ Plot legend for ___s colors in a seperate smaller widget
        canvas.

        """
        fig, ax = plt.subplots(
            figsize=(0.2*GetSystemMetrics(0)/self.dpi,
                     0.2*GetSystemMetrics(1)/self.dpi))
        fig.tight_layout()
        fig.set_dpi(self.dpi)
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(b=False, which='both', axis='both')
        ax.set_facecolor('white')
        ax.tick_params(axis="both", left=False, bottom=False,
                       labelleft=False, labelbottom=False)
        # 3 cols if maximum lengthed label is less than 15 chars,
        # otherwise only 2
        max_length_labels = max(
            [len(str(label)) for label, handle in self.legendreference])
        if (max_length_labels <= 15):
            # If Labels less than 15, add spaces to end until all have 15
            new_labels = []
            for label, handle in self.legendreference:
                mutatable_label = str(self.legend___namelookup[label])
                while(len(mutatable_label) < 15):
                    mutatable_label += ' '
                new_labels.append(mutatable_label)
            ax.legend([handle for label, handle in self.legendreference],
                      new_labels,
                      ncol=3, framealpha=0., loc="center",
                      bbox_to_anchor=(.5, .5), fontsize=8,
                      title='Place Legend')
        else:
            ax.legend([handle for label, handle in self.legendreference],
                      [self.legend___namelookup[label] for label, handle in self.legendreference],
                      ncol=2, framealpha=0., loc="center",
                      bbox_to_anchor=(.5, .5), fontsize=8,
                      title='Place Legend')
        self.legendcanvas = FigureCanvasTkAgg(fig, master=self.parent)
        self.legendcanvas.get_tk_widget().configure(relief='sunken', bd=1)
        self.legendcanvas.get_tk_widget().grid(
            column=1, row=5, columnspan=4, padx=self.padx, pady=self.pady,
            sticky='NSEW')

    def disable_input_widgets(self):
        """ Disable all user input widgets.

        """
        self.leftfive.configure(state='disabled')
        self.leftone.configure(state='disabled')
        self.rightone.configure(state='disabled')
        self.rightfive.configure(state='disabled')
        self.zoomin.configure(state='disabled')
        self.zoomout.configure(state='disabled')
        self.enlargebutton.configure(state='disabled')
        self.reducebutton.configure(state='disabled')
        self.resetbutton.configure(state='disabled')
        self.quit.configure(state='disabled')
        self.switchscorecount.configure(state='disabled')

    def enable_input_widgets(self):
        """ Enable all user input widgets.

        """
        self.leftfive.configure(state='normal')
        self.leftone.configure(state='normal')
        self.rightone.configure(state='normal')
        self.rightfive.configure(state='normal')
        self.zoomin.configure(state='normal')
        self.zoomout.configure(state='normal')
        self.enlargebutton.configure(state='normal')
        self.reducebutton.configure(state='normal')
        self.resetbutton.configure(state='normal')
        self.quit.configure(state='normal')
        self.switchscorecount.configure(state='normal')

    def refresh_____plot(self):
        """ Update ____ line cursor with current linex attribute and perform
        blit refreshing of plot, drawing updated position of line. After
        plot is updated, calls update_text to update as well.

        """
        self.____line.set_xdata(self.linex)
        self.canvas.restore_region(self.canvas_bg)
        self.ax.draw_artist(self.____line)
        bbox = (self.canvas.get_tk_widget().bbox('all'))
        self.canvas.blit(Bbox(np.array([[bbox[0], bbox[1]],
                                        [bbox[2], bbox[3]]])))
        self.update_text()

    def reset_plot(self):
        """ Reset plot to initial plotting view.

        """
        self.disable_input_widgets()
        # Reset to initial values, and replot
        self.linex = 0
        self.scalenumfory = 1.
        self.ylim = self.ax_ylim_orig*self.scalenumfory
        plt.close('all')
        self.canvas.get_tk_widget().destroy()
        if self.active_plot == "_____count":
            self.plot_____countplot()
        elif self.active_plot == "_____score":
            self.plot_____scoreplot()
        self.enable_input_widgets()

    def resize_plot(self, increment):
        """ Increases/decreases blank canvas screen scaling by increment,
        and replots everything to fit the new value.

        """
        if (self.plotscale + increment) >= 0.1:
            self.disable_input_widgets()
            self.plotscale += increment
            self.blankcanvas.get_tk_widget().destroy()
            self.canvas.get_tk_widget().destroy()
            self.plot_blankcanvas(self.plotscale)
            plt.close('all')
            if self.active_plot == "_____count":
                self.plot_____countplot()
            elif self.active_plot == "_____score":
                self.plot_____scoreplot()
            self.refresh_____plot()
            self.enable_input_widgets()
        else:
            pass

    def scale_y(self, enlarge_or_reduce):
        """ Sudo zoom in to the plot, by reducing the y limit range, or
        increasing the y limit range of the plot. Can not zoomout
        more than original view.

        """
        self.disable_input_widgets()
        scale_amount = 0.7
        if enlarge_or_reduce == 'enlarge':
            if 0 < self.scalenumfory/scale_amount <= 1.0:
                self.scalenumfory /= scale_amount
                self.ylim = self.ax_ylim_orig*self.scalenumfory
                plt.close('all')
                self.canvas.get_tk_widget().destroy()
                if self.active_plot == "_____count":
                    self.plot_____countplot()
                elif self.active_plot == "_____score":
                    self.plot_____scoreplot()
            else:
                pass
        elif enlarge_or_reduce == 'reduce':
            if 0 < self.scalenumfory*scale_amount <= 1.0:
                self.scalenumfory *= scale_amount
                self.ylim = self.ax_ylim_orig*self.scalenumfory
                plt.close('all')
                self.canvas.get_tk_widget().destroy()
                if self.active_plot == "_____count":
                    self.plot_____countplot()
                elif self.active_plot == "_____score":
                    self.plot_____scoreplot()
            else:
                pass
        self.enable_input_widgets()

    def switch_plot(self):
        """ Switch plot from _____ count to _____ score, or from _____ score
        to _____ count, depending on which is currently active.

        """
        self.disable_input_widgets()
        self.scalenumfory = 1.
        delattr(self, 'ylim')
        plt.close('all')
        self.canvas.get_tk_widget().destroy()
        # If _____ count plot, plot score plot, and if score
        # plot, plot _____ count plot
        if self.active_plot == "_____count":
            self.active_plot = "_____score"
            self.plot_____scoreplot()
            self.update_text()
        elif self.active_plot == "_____score":
            self.active_plot = "_____count"
            self.plot_____countplot()
            self.update_text()
        self.enable_input_widgets()

    def sudo_press_button(self, button):
        """ Invokes button and makes button appear to be pressed, does not
        unpress it itself.

        """
        button.state(['pressed'])
        button.invoke()

    def click_line(self, event):
        """ Checks click of mouse cursor, and see if is within axes and within
        ____s. If outside of axes, does nothing, and if outside of ____s
        but still in axes, changes linex to the respective xlimit that
        cursor is on the side of.

        """
        # If mouse click is out of plot does nothing
        if event.inaxes is None:
            pass
        else:
            # Check x limitations
            if event.xdata <= self.xlim[0]:
                moveto = self.xlim[0]
            elif event.xdata >= self.xlim[1]:
                moveto = self.xlim[1]
            else:
                moveto = event.xdata
            self.linex = round(moveto)
            self.refresh_____plot()

    def increment_line(self, amount):
        """ Checks the value if the ____ line cursor is changed be the amount,
        and increments linex by the amount, if it will not overshoot the x
        limits of the graph (i.e. will not move cursor to area where there
        are no ____s). Then calls to refresh the plot to move the line, or
        not move it if overshot.

        """
        next_line_value = self.linex + amount
        if next_line_value <= self.xlim[0]:
            self.linex = self.xlim[0]
        elif next_line_value >= self.xlim[1]:
            self.linex = self.xlim[1]
        else:
            self.linex = next_line_value
        self.refresh_____plot()

    def update_text(self):
        """ Updates text in text display, based on which ____ the ____ line
        cursor is currently selecting.

        """
        # linex x value will match index referenced, as ____info is in the
        # same enumerated index as the plot, due to earlier similar ordered
        # enumeration and placement in constructor.
        index = int(self.linex)

        # Change text with reference to _____ score or _____ count
        # and corresponding ____info grouping depending on the current
        # active plot
        if self.active_plot == '_____count':
            ____info = self.____info____grouped[index]
        elif self.active_plot == '_____score':
            ____info = self.____info2____grouped[index]
        # Must enable text to change it, and must disable so user does not
        # accidentally change it
        self.textdisplay.configure(state=tk.NORMAL)
        self.textdisplay.delete('1.0', tk.END)
        self.textdisplay.insert(
            tk.END, '\n  N Occurences of Item:\n', 'boldtag')
        self.textdisplay.insert(
            tk.END, '  {}\n\n'.format(____info[4]))
        self.textdisplay.insert(
            tk.END, '  Total Value of Item:\n', 'boldtag')
        self.textdisplay.insert(
            tk.END, '  {}\n\n'.format(____info[5]))
        self.textdisplay.insert(
            tk.END, '  Average Value of Item:\n', 'boldtag')
        self.textdisplay.insert(
            tk.END, '  {}\n\n'.format(round(float(____info[5]) /
                                            float(____info[4]), 2)))
        self.textdisplay.insert(
            tk.END, '  Item Identification:\n', 'boldtag')
        self.textdisplay.insert(
            tk.END, '  {}\n\n'.format(____info[0]))
        self.textdisplay.insert(
            tk.END, '  Item Attribute:\n', 'boldtag')
        self.textdisplay.insert(
            tk.END, '  {}\n\n'.format(____info[3]))
        self.textdisplay.insert(
            tk.END, '  Place of Item:\n', 'boldtag')
        self.textdisplay.insert(
            tk.END, '  {}\n\n'.format(____info[1]))
        self.textdisplay.insert(
            tk.END, '  Name of Place of Item:\n', 'boldtag')
        self.textdisplay.insert(
            tk.END, '  {}\n\n'.format(____info[2]))
        self.textdisplay.insert(
            tk.END, '  Plot Index:\n', 'boldtag')
        self.textdisplay.insert(
            tk.END, '  {}\n'.format(index))
        self.textdisplay.tag_configure('boldtag', font='default 11 bold')
        self.textdisplay.configure(state=tk.DISABLED)

    def true_quit(self):
        """ Destroys window after explicitly closing plots and deleting
        picture in canvas, speeding up the close time of the application.

        """
        plt.close('all')
        self.canvas.get_tk_widget().delete('all')
        self.parent.destroy()

    def instructions_message(self):
        """ Instruction help popup.

        """
        localroot = tk.Tk()
        localroot.title('Instructions')
        message = ScrolledText(
            localroot, width=60, height=10, font=('default', 11),
            wrap=tk.WORD)
        message.insert(
            tk.END,
            ('Line Cursor Movement\n\n'), 'boldtag')
        message.insert(
            tk.END,
            ('( > / <Right Key> / <D Key> )  Move Line 1 Index Right.\n\n'
             '( >> / <Up Key> / <W Key> )  Move Line 5 Indices Right.\n\n'
             '( < / <Left Key> / <A Key> )  Move Line 1 Index Left.\n\n'
             '( << / <Down Key> / <S Key> )  Move Line 5 Indices Left.\n\n'
             'Can click on plot to move line to mouse cursor location.\n\n'))
        message.insert(
            tk.END,
            ('Plot View Manipulation\n\n'), 'boldtag')
        message.insert(
            tk.END,
            ('( Zoom in Y / Zoom out Y )  Zooms Y axis of plot to better see desired '
             'range of item values or item counts.\n\n'
             '( Reduce Plot / Enlarge Plot )  Expands or reduces size of plot for '
             'desired viewing.\n\n'
             '( Reset View )  Unzooms y axis and resets line cursor position while '
             'maintaining enlarged or reduced plot size.\n\n'
             '( Switch Item Value / Item Count )  If current plot is of '
             'item count, switches to item value. If current plot is of '
             'item value, switches to item count. Maintains line cursor '
             'placement and enlarged/reduced plot size.'))
        message.tag_configure('boldtag', font='default 11 bold')
        message.config(state='disabled')
        message.grid(column=0, row=0, padx=5, pady=5, sticky='NSWE')
        localroot.grid_columnconfigure(0, weight=1)
        localroot.grid_rowconfigure(0, weight=1, minsize=460)
        localroot.geometry(
            "+{}+{}".format(int(self.parent.winfo_rootx()-
                                localroot.winfo_width()/2),
                            int(self.parent.winfo_rooty()-
                                localroot.winfo_height()/2)))
        localroot.mainloop()


class FileBrowser():
    """
    GUI File Browser application for finding ____ engine output CSV to
    activate ____ browser from. Simply contains an entry box for manual
    entry, a button to browse for the file using tkinter's filedialog,
    a submit button for activating with the entered path, a spinbox for
    entering initial plot upscaling/downscaling and a message to notify
    user of errors. Checks that path is a .txt or .csv, and if the
    file exists before attempting to load in ____browser.

    Attributes
    ---

    parent : tk.Tk
        Parent root window widget for all widgets. Can be called to run
        mainloop of application.
    font : tuple of (str, float)
        Tuple of font and fontsize for labels and text display
        (font, fontsize).
    padx : int
        X-direction padding for widgets for grid.
    pady : int
        Y-direction padding for widgets for grid.
    filenameentry : tk.Entry
        Entry box for entering and displaying current candidate entry for
        filename.
    valid_filename : str
        Valid filename to use, which is a .csv or a .txt, and is findable by
        python
    plotsize : str
        Text float number to use as percentage of screen that plot should be
        initially.
    localroot : tk.Tk, optional
        Instructions message window.

    """
    def __init__(self, parent):
        """
        Constructor for FileBrowser Class, does following:
            - Builds widgets of application and specifies their functionality
              and style.
            - Allows user to browse for or manually enter a path to desired
              output csv.
            - Checks given path for simple errors, and notifies user if there
              are, without closing application.

        Parameters
        ---
        parent : tk.Tk
            Parent root window widget for all widgets to be built upon.

        """
        self.parent = parent
        self.parent.title("Open CSV in Item Browser")

        menu = tk.Menu(self.parent)
        menu.add_command(label='Help',
                         command=self.instructions_message)
        self.parent.config(menu=menu)

        style = ttk.Style(self.parent)
        style.theme_use('clam')
        style.configure('TButton', font=('default', 10))
        self.font = ('default', 11)
        self.padx = 10
        self.pady = 5

        tk.Label(self.parent, text='Item History Input csv or txt',
                 font=self.font).grid(
            column=0, row=1, padx=self.padx, pady=self.pady, sticky='W')
        self.filenameentry = tk.Entry(
            self.parent, width=40, font=self.font)
        self.filenameentry.grid(
            column=0, row=2, padx=self.padx, pady=self.pady, sticky='W')

        browsebutton = ttk.Button(
            self.parent, text='Browse', command=self.facilitate_filedialog)
        browsebutton.grid(
            column=1, row=2, padx=self.padx, pady=self.pady)

        tk.Label(self.parent,
                 text='Initial Plot Size (Size as Fraction of Screen)',
                 font=self.font).grid(
            column=0, row=3, padx=self.padx, pady=self.pady, sticky='W')
        self.scalingentry = tk.Spinbox(
            self.parent,
            values=(0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.),
            font=self.font, width=39)
        self.scalingentry.grid(
            column=0, row=4, padx=self.padx, pady=self.pady, sticky='W')
        self.scalingentry.delete(0, tk.END)
        self.scalingentry.insert(tk.END, '0.6')
        self.scalingentry.configure(state='readonly')

        openbrowserbutton = ttk.Button(
            self.parent, text='Open CSV in Item Browser',
            command=self.check_valid_before_destroy)
        openbrowserbutton.grid(
            column=0, row=5, columnspan=2, padx=self.padx, pady=15,
            sticky='WE')

        # Creates widgets so that widget widths to be calculated
        self.parent.update_idletasks()

        self.parent.geometry(
            "+{}+{}".format(int(GetSystemMetrics(0)/2 -
                                self.parent.winfo_width()/2),
                            int(GetSystemMetrics(1)/2 -
                                self.parent.winfo_height()/2)))
        self.parent.lift()

    def instructions_message(self):
        """ Instruction help popup.

        """
        # Try and destroy localroot if exist already
        if hasattr(self, 'localroot'):
            try:
                self.localroot.destroy()
            except tk.TclError:
                pass
        localroot = tk.Tk()
        localroot.title('Instructions')
        message = ScrolledText(
            localroot, width=60, height=10, font=('default', 11),
            wrap=tk.WORD)
        message.insert(
            tk.END,
            ('How To Open a Item History csv in the Obfuscated Item '
             'Browser\n\n'),
            'boldtag')
        message.insert(
            tk.END,
            ('1. In the first entry box, enter the path to the item '
             'history csv that is to be viewed.\n\n'))
        message.insert(
            tk.END,
            ('1.1 Optionally, choose a larger or smaller initial plot size '
             'in a fraction of screen size, with the default being 0.6. '
             'This can be changed later in the application.\n\n'))
        message.insert(
            tk.END,
            ('2. Press the "Open CSV in Item Browser" button to open'
             ' the obfuscated item browser.'))
        message.tag_configure('boldtag', font='default 11 bold')
        message.config(state='disabled')
        message.grid(column=0, row=0, padx=5, pady=5, sticky='NSWE')
        localroot.grid_columnconfigure(0, weight=1)
        localroot.grid_rowconfigure(0, weight=1, minsize=200)
        localroot.geometry(
            "+{}+{}".format(int(self.parent.winfo_rootx()-
                                localroot.winfo_width()/2),
                            int(self.parent.winfo_rooty()-
                                localroot.winfo_height()/2)))

        # Set to object space so can be destroyed if generate csv is hit
        self.localroot = localroot
        self.localroot.mainloop()

    def is_number_greater_than(self, string, min_value):
        """ Checks if string is convertable to float number and is greater
        than given min_value number.

        """
        try:
            float(string)
            if min_value < float(string):
                return(True)
            else:
                return(False)
        except ValueError:
            return(False)

    def facilitate_filedialog(self):
        """ Activates the filedialog and replaces the entry in
        filenameentry if one is entered.

        """
        filename = filedialog.askopenfilename(
            title='Select Item History Extract')
        # If a filename is specified, delete and replace current entry
        if filename != "":
            self.filenameentry.delete(0, 'end')
            self.filenameentry.insert('end', filename)
        else:
            pass

    def check_valid_before_destroy(self):
        """ Checks if given file name is a csv or a .txt, if the file
        is able to be found by python. Activates pop up error if either
        condition is not met, and defines a attribute for reference if
        is a valid filename.

        """
        error_string = ""
        candidate_filename = self.filenameentry.get()
        candidate_plotsize = self.scalingentry.get()
        if (not ('.csv' in candidate_filename[-4:] or
                 '.txt' in candidate_filename[-4:]) and
                not os.path.isfile(candidate_filename)):
            error_string += ('____ engine output must be '
                             'existing csv or txt file.\n')
        if error_string == "":
            self.valid_filename = candidate_filename
            self.plotsize = candidate_plotsize
            # Try and destroy localroot
            if hasattr(self, 'localroot'):
                try:
                    self.localroot.destroy()
                except tk.TclError:
                    pass
            self.parent.destroy()
        else:
            messagebox.showerror('Error', error_string)


if __name__ == '__main__':

    # Start filebrowser to load csv
    mini_root = tk.Tk()
    mini_app = FileBrowser(mini_root)
    mini_app.parent.mainloop()

    # Use specified path to start main application if specifying one
    if hasattr(mini_app, 'valid_filename'):
        root = tk.Tk()
        app = ____Brower(root, mini_app.valid_filename,
                         float(mini_app.plotsize))
        app.parent.mainloop()
    else:
        pass
