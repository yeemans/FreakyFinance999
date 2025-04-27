from datetime import datetime
import tkinter as tk
from tkinter import simpledialog
import tkcalendar
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Sheet

engine = create_engine('sqlite:///database.db')  # or your DB of choice
Session = sessionmaker(bind=engine)
session = Session()

class ScrollableFrame:
    def __init__(self, root):
        # Create a container frame for the self.canvas and scrollbars
        self.container = tk.Frame(root)
        self.container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.container)
        self.canvas.pack(side="top", fill="both", expand=True)


        self.horizontal_scrollbar = tk.Scrollbar(self.container, orient="horizontal", command=self.canvas.xview)
        self.horizontal_scrollbar.pack(side="bottom", fill="x")
        self.vertical_scrollbar = tk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.vertical_scrollbar.pack(side="right", fill="y")

        # Create a frame that will be placed inside the self.canvas
        self.frame = tk.Frame(self.canvas)

        # Create a window inside the self.canvas that will hold the frame
        self.window_id = self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        # Configure the self.canvas to update its view when the frame changes
        self.frame.bind("<Configure>", lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Link the scrollbars to the self.canvas
        self.canvas.configure(xscrollcommand=self.horizontal_scrollbar.set, yscrollcommand=self.vertical_scrollbar.set)


class App(tk.Frame):
    def get_start_date(self):
        if self.start_calendar_widget: self.start_calendar_widget.destroy()
        self.start_calendar_widget = tkcalendar.Calendar(self.root)
        self.start_calendar_widget.pack()
        
        # replace the show start calendar button with a button to save the date
        self.start_date_button.destroy()
        self.start_date_button = tk.Button(self.frame, text=f"Save date", command=self.save_start_date)
        self.start_date_button.grid(row=1, column=1, columnspan=1, pady=10)

    def save_start_date(self):
        self.start_date = self.start_calendar_widget.get_date()
        # hide calendar and change save button back to button that shows the date

        self.start_date_button = tk.Button(self.frame, text=f"Start Date: {self.start_date}", command=self.get_start_date)
        self.start_date_button.grid(row=1, column=1, columnspan=1, pady=10)
        self.start_calendar_widget.destroy()
        self.start_calendar_widget = None

    def get_end_date(self):
        if self.end_calendar_widget: self.end_calendar_widget.destroy()
        self.end_calendar_widget = tkcalendar.Calendar(self.root)
        self.end_calendar_widget.pack()
        
        # replace the show end calendar button with a button to save the date
        self.end_date_button.destroy()
        self.end_date_button = tk.Button(self.frame, text=f"Save date", command=self.save_end_date)
        self.end_date_button.grid(row=1, column=2, columnspan=1, pady=10)

    def save_end_date(self):
        self.end_date = self.end_calendar_widget.get_date()
        # hide calendar and change save button back to button that shows the date

        self.end_date_button = tk.Button(self.frame, text=f"End Date: {self.end_date}", command=self.get_end_date)
        self.end_date_button.grid(row=1, column=2, columnspan=1, pady=10)
        self.end_calendar_widget.destroy()

    def __init__(self, master):
        super().__init__(master)
        self.root = master
        self.UserID = master.UserID
        self.start_calendar_widget = None
        self.end_calendar_widget = None
        self.start_date = "4/22/2025"
        self.end_date = "5/22/2025"
        self.title = "Expense Sheet"
        
        self.frame_object = ScrollableFrame(self.root)
        self.frame = self.frame_object.frame

        # maps category names, strings, to lists of tuples.
        # tuple[0] is the name of an expense, tuple[1] is its cost
        self.expenses_by_category = {"Housing": [], "Food": [], "Subscriptions": []}
        # Create the button to add new columns

                
        self.title_label = tk.Label(self.frame, text="Title: ")
        self.title_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")  # Align label to the right

        self.title_entry = tk.Entry(self.frame, width=35)
        self.title_entry.grid(row=0, column=1, padx=10, pady=10)
        self.title_entry.insert(0, "Expense Sheet")

        self.save_button = tk.Button(self.frame, text="Save Sheet", command=self.save_sheet)
        self.save_button.grid(row=0, column=2, padx=10, pady=10)

        self.add_column_button = tk.Button(self.frame, text="Add New Column", command=self.prompt_for_column)
        self.add_column_button.grid(row=1, column=0, columnspan=1, pady=10)
                                                                                
        self.start_date_button = tk.Button(self.frame, text=f"Start: 4/22/2025", 
                                           command=self.get_start_date)
        self.start_date_button.grid(row=1, column=1, columnspan=1, pady=10)

        self.end_date_button = tk.Button(self.frame, text="End: 4/22/2025", 
                                         command=self.get_end_date)
        self.end_date_button.grid(row=1, column=2, columnspan=1, pady=10)
        # Create the initial table
        self.create_table()

    def prompt_for_column(self):
        # Prompt the user for a new column name
        new_column = simpledialog.askstring("Input", "Enter the new column name:")

        if new_column:
            self.expenses_by_category[new_column] = []
            self.update_table()

    def prompt_for_expense(self, category_name): # expense_column is an index for expenses_by_category
        new_expense = simpledialog.askstring("Input", "Enter the new expense's name:")
        if not new_expense: return

        new_cost = simpledialog.askfloat("Input", "Enter the dollar amount:")
        self.expenses_by_category[category_name].append((new_expense, new_cost))
        
        self.update_table()

    def create_table(self):
        # Clear the existing table (if any)
        for widget in self.frame.winfo_children():
            # ignore column labels
            if widget not in [self.add_column_button, self.start_date_button, 
                              self.end_date_button, self.title_label, self.title_entry, self.save_button]:
                widget.destroy()

        # Create headers for the current columns
        for col, expense_list in enumerate(self.expenses_by_category.items()):
            category = expense_list[0]
            col_label = tk.Label(self.frame, text=category, relief="solid", width=15, height=2)
            col_label.grid(row=4, column=col, padx=5, pady=5)

        # display expenses and "New Expense" buttons
        ROW_PADDING = 5
        for col, expense_category in enumerate(self.expenses_by_category.items()):
            category_name, expense_list = expense_category
            print([category_name, col])

            for row, expense in enumerate(expense_list):
                expense_name, expense_cost = expense
                expense_label = tk.Label(self.frame, text=f"{expense_name}: {expense_cost}", width=15, height=2, relief="solid")
                expense_label.grid(row=row + ROW_PADDING, column=col)
                print(self.expenses_by_category)
                

            # display total cost of all items in the category
            category_total = sum([cost for expense, cost in expense_list])
            category_total_label = tk.Label(self.frame, text=f"Total: ${category_total}", relief="solid", 
                             width=15, height=2)
            category_total_label.grid(row=ROW_PADDING + len(expense_list), column=col) # not sure why + 3 works

            add_expense_button = tk.Button(self.frame, text=f"Add {category_name} Expense", relief="solid", 
                             command=lambda cat=category_name: self.prompt_for_expense(cat), 
                             width=25, height=2)
            add_expense_button.grid(row=ROW_PADDING + len(expense_list) + 1, column=col) # not sure why + 3 works

        
    def update_table(self):
        # Recreate the table with the updated column names
        self.create_table()

    def calculate_total(self):
        total = 0
        for list_of_expenses_in_category in self.expenses_by_category.items():
            total += sum(list_of_expenses_in_category)

        return total
    
    def destroy(self):
        if not self.frame_object: return
        canvas_id = self.frame_object.window_id
        self.frame_object.canvas.delete(canvas_id)

        for widg_name, widg in vars(self.frame_object).items():
            if widg_name == "window_id": continue
            widg.destroy()
            
        self.frame_object = None

    def save_sheet(self):
        title = self.title_entry.get()
        json_string = json.dumps(self.expenses_by_category)

        start_date = datetime.strptime(self.start_date, "%m/%d/%Y").date()
        end_date = datetime.strptime(self.end_date, "%m/%d/%Y").date()

        sheet_model = Sheet(UserID = self.UserID, start_date=start_date,
                            end_date=end_date, title=title, json_string=json_string)
        try:
            session.add(sheet_model)
            session.commit()
        except:
            session.rollback()

        print(json_string)
        print(session.query(Sheet).all())


#if __name__ == "__main__":
    #app = App()
    #app.mainloop()
