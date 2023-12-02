import tkinter as tk
import tkinter.filedialog
from tkinter import ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from nations import Nation


class GovernmentSimulator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AuroraGov")
        self.geometry("400x300")

        self.nation = None  # To store the current nation instance

        self.create_widgets()

    def create_widgets(self):
        saveButton = ttk.Button(self, text="Save Nation", command=self.SaveNation)
        saveButton.pack(pady=10)

        loadButton = ttk.Button(self, text="Load Nation", command=self.LoadNation)
        loadButton.pack(pady=10)

        # Label for displaying current nation info
        self.info_label = ttk.Label(self, text="")
        self.info_label.pack(pady=10)

        # Matplotlib canvas for embedding the plot
        self.canvas = None

    def DisplayNationInfo(self, nationInfo):
        infoText = f"Name: {nationInfo['name']}\nGovernment Type: {nationInfo['governmentType']}\n" \
                    f"Population: {nationInfo['population']}\nPublic Opinion: {nationInfo['publicOpinion']}"
        self.info_label.config(text=infoText)

    def PlotPartyData(self):
        # If a canvas already exists, destroy it before creating a new one
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        # Create a new Matplotlib canvas and embed it in the Tkinter window
        fig = self.nation.PlotPartyPie()
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def SaveNation(self):
        if self.nation is None:
            return  # No nation to save

        # Open a file dialog to choose the location to save the JSON file
        filename = tk.filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])

        if filename:
            self.nation.SaveState(filename)

    def LoadNation(self):
        # Open a file dialog to select a JSON file
        filename = tk.filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])

        if filename:
            # Load the nation from the selected file
            self.nation = Nation()
            self.nation.LoadState(filename)
            print("Nation loaded from:", filename)

            self.RefreshNationInfo()

    def RefreshNationInfo(self):
        currentState = self.nation.GetState()
        self.DisplayNationInfo(currentState)

        self.PlotPartyData()


if __name__ == "__main__":
    app = GovernmentSimulator()
    app.mainloop()
