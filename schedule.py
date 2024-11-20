from tkinter import Tk, StringVar
from tkinter import ttk

class MyApp:
    def __init__(self, parent):
        self.selected_year = StringVar(value="Select Year")

        # Create a Combobox
        self.year_dropdown = ttk.Combobox(
            parent,
            textvariable=self.selected_year,
            values=[str(year) for year in range(2020, 2031)],
            state="readonly"  # Makes it a dropdown (not editable)
        )

        # Place the Combobox in the window
        self.year_dropdown.pack(pady=10)
        self.year_dropdown.bind("<<ComboboxSelected>>", self.change_year)

    def change_year(self, event):
        print(f"Year selected: {self.selected_year.get()}")

# Create the main window
root = Tk()
app = MyApp(root)
root.geometry("300x100")  # Set window size
root.mainloop()