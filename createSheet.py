import tkinter as tk
from tkinter import simpledialog
import tkcalendar


    
class MyApp:
    def setStartDate(self):
        for widget in self.root.winfo_children():
            if widget is self.startCalendarWidget: widget.destroy()

        self.startCalendarWidget = tkcalendar.Calendar(self.root)
        self.startCalendarWidget.pack()
        # replace the show start calendar button with a button to save the date
        

    def setEndDate(self):
        for widget in self.root.winfo_children():
            if widget is self.endCalendarWidget: widget.destroy()

        self.endCalendarWidget = tkcalendar.Calendar(self.root)
        self.endCalendarWidget.pack()

    def __init__(self, root):
        self.root = root
        self.root.title("Create Sheets")
        self.startCalendarWidget = None
        self.endCalendarWidget = None
        self.startDate = None
        self.endDate = None
        
        self.frame = tk.Frame(root)
        self.frame.pack(padx=20, pady=20)

        # date picker for start and end dates of sheet


        # dictionary of lists. maps strings to lists of tuples with length 2.
        # tuples are (expense_name, expense_cost)
        self.expenses_by_category = {"Housing": [], "Food": [], "Subscriptions": []}
        
        # Create the button to add new columns
        self.add_column_button = tk.Button(self.frame, text="Add New Column", command=self.prompt_for_column)
        self.add_column_button.grid(row=0, column=0, columnspan=1, pady=10)

        self.start_date_button = tk.Button(self.frame, text="Set Start Date", command=self.setStartDate)
        self.start_date_button.grid(row=0, column=1, columnspan=1, pady=10)

        self.end_date_button = tk.Button(self.frame, text="Set End Date", command=self.setEndDate)
        self.end_date_button.grid(row=0, column=2, columnspan=1, pady=10)
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
            if widget not in [self.add_column_button, self.start_date_button, self.end_date_button]:
                widget.destroy()

        # Create headers for the current columns
        for col, expense_list in enumerate(self.expenses_by_category.items()):
            category = expense_list[0]
            col_label = tk.Label(self.frame, text=category, relief="solid", width=15, height=2)
            col_label.grid(row=3, column=col, padx=5, pady=5)

        # display expenses and "New Expense" buttons
        for col, expense_category in enumerate(self.expenses_by_category.items()):
            ROW_PADDING = 4
            category_name, expense_list = expense_category
            print([category_name, col])

            for row, expense in enumerate(expense_list):
                expense_name, expense_cost = expense
                expense_label = tk.Label(self.frame, text=f"{expense_name}: {expense_cost}", width=15, height=2, relief="solid")
                expense_label.grid(row=row + ROW_PADDING, column=col)
                print(self.expenses_by_category)
                
            add_expense_button = tk.Button(self.frame, text=f"Add {category_name} Expense", relief="solid", 
                             command=lambda cat=category_name: self.prompt_for_expense(cat), 
                             width=25, height=2)
            add_expense_button.grid(row=ROW_PADDING + len(expense_list), column=col) # not sure why + 3 works

    def update_table(self):
        # Recreate the table with the updated column names
        self.create_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
