import pandas as pd
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog, Canvas, Scrollbar
import datetime


# Step 0: Create helper functions
# Function to create a tooltip
class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tip_window = None

    def show_tip(self, tip_text, event):
        if self.tip_window or not tip_text:
            return
        x = event.x_root + 20
        y = event.y_root + 20
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=tip_text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tip(self):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()

# Function to generate weekly dates
def generate_weekly_dates(start_year):
    start_date = datetime.date(start_year, 1, 1)
    return [start_date + datetime.timedelta(weeks=i) for i in range(52)]


# Step 1: Ask to Load CSV
load_csv = messagebox.askyesno("Load CSV", "Do you want to load data from a CSV file?")
if load_csv:
    filename = filedialog.askopenfilename(title="Select file", filetypes=[("CSV files", "*.csv")])
    if filename:
        df = pd.read_csv(filename, index_col=0)
        df = df.astype(object)  # Convert all columns to object type
        # Extract name and birth year from filename
        name, birth_year = filename.rstrip('.csv').split('/')[-1].split('-')
        birth_year = int(birth_year)
    else:
        load_csv = False

# Step 2: Conditional Name and Birth Year Input

if not load_csv:
    name = simpledialog.askstring("Name", "Enter your name:")
    birth_year = simpledialog.askinteger("Birth Year", "Enter your birth year:")
    life_length = simpledialog.askinteger("Life Length", "How many years do you want to live for?")
    cols = generate_weekly_dates(birth_year)
    rows = [f"{birth_year + i}" for i in range(life_length)]  # Rows for years of life starting from birth year
    df = pd.DataFrame(index=rows, columns=cols, dtype=object)

# Step 3: Set Up the GUI
class DataFrameGUI:
    def __init__(self, master, dataframe):
        self.master = master
        self.df = dataframe
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.create_grid()

    def create_grid(self):
        # Create a canvas and scrollbar
        self.canvas = Canvas(self.master)
        self.scrollbar = Scrollbar(self.master, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        for i, row in enumerate(self.df.index):
            tk.Label(self.scrollable_frame, text=row).grid(row=i, column=0)  # Year labels
            for j, col in enumerate(self.df.columns, start=1):
                # Check if cell has data
                data = self.df.at[row, col]
                canvas = tk.Canvas(self.scrollable_frame, width=30, height=30, bg='white')
                canvas.grid(row=i, column=j)
                fill_color = 'black' if pd.notna(data) else 'white'
                canvas.create_oval(5, 5, 25, 25, fill=fill_color)

                # Bind a click event
                canvas.bind("<Button-1>", lambda event, x=i, y=j-1: self.cell_clicked(x, y))

                # Create tooltip if there is data
                if pd.notna(data):
                    tooltip = ToolTip(canvas)
                    canvas.bind("<Enter>", lambda event, text=data, tooltip=tooltip: tooltip.show_tip(text, event))
                    canvas.bind("<Leave>", lambda event, tooltip=tooltip: tooltip.hide_tip())

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def cell_clicked(self, row, col):
        # Convert the string date to datetime.date object
        start_date_str = self.df.columns[col]
        start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()  # Adjust the format if necessary

        # Calculate the end date of the week
        end_date = start_date + datetime.timedelta(days=6)  # End date is 6 days after the start date

        # Format the prompt message with these dates
        prompt_message = f"What happened between {start_date.strftime('%b %d')} - {end_date.strftime('%b %d, %Y')} ?"

        # Open a dialog to enter data
        value = simpledialog.askstring("Input", prompt_message, parent=self.master)

        if value is not None:
            # Update the DataFrame
            self.df.at[self.df.index[row], self.df.columns[col]] = value

    def on_closing(self):
        # Save to CSV with name and birth year
        self.df.to_csv(f"{name}-{birth_year}.csv")
        self.master.destroy()

# Step 4: Initialize the GUI
root = tk.Tk()
root.title("💀💀💀")
app = DataFrameGUI(root, df)
root.mainloop()
