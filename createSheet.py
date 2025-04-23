import tkinter as tk
from tkinter import simpledialog
import tkcalendar


class MyApp:
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

    def __init__(self, root):
        self.root = root
        self.root.title("Create Sheets")
        self.start_calendar_widget = None
        self.end_calendar_widget = None
        self.start_date = None
        self.end_date = None
        self.total = 0
        
        self.frame = tk.Frame(root)
        self.frame.pack(padx=20, pady=20)

        self.expenses_by_category = {"Housing": [], "Food": [], "Subscriptions": []}
        # Create the button to add new columns
        self.add_column_button = tk.Button(self.frame, text="Add New Column", command=self.prompt_for_column)
        self.add_column_button.grid(row=1, column=0, columnspan=1, pady=10)
                                                                                
        self.start_date_button = tk.Button(self.frame, text=f"Start: 4/22/2025", 
                                           command=self.get_start_date)
        self.start_date_button.grid(row=1, column=1, columnspan=1, pady=10)

        self.end_date_button = tk.Button(self.frame, text="End: 5/22/2025", 
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
            if widget not in [self.add_column_button, self.start_date_button, self.end_date_button]:
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
    
if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
