import tkinter as tk
from tkinter import simpledialog

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic Column Addition")
        
        self.frame = tk.Frame(root)
        self.frame.pack(padx=20, pady=20)

        # list of dicts, one dict for each category. Dicts map strings to lists
        self.expenses_by_category = [] 
        
        # Create the button to add new columns
        self.add_column_button = tk.Button(self.frame, text="Add New Column", command=self.prompt_for_column)
        self.add_column_button.grid(row=0, column=0, columnspan=2, pady=10)

        # Create the initial table
        self.create_table()

    def prompt_for_column(self):
        # Prompt the user for a new column name
        new_column = simpledialog.askstring("Input", "Enter the new column name:")

        if new_column:
            self.expenses_by_category.append({new_column: []})
            self.update_table()

    def prompt_for_expense(self):
        new_expense = simpledialog.askstring("Input", "Enter the new expense's name:")
        new_cost = simpledialog.askfloat("Input", "Enter the dollar amount:")

    def create_table(self):
        # Clear the existing table (if any)
        for widget in self.frame.winfo_children():
            if isinstance(widget, tk.Label) and widget != self.add_column_button:
                widget.destroy()

        # Create labels for the current columns
        for col, expense_list in enumerate(self.expenses_by_category):
            category = list(expense_list.keys())[0]
            col_label = tk.Label(self.frame, text=category, relief="solid", width=15, height=2)
            col_label.grid(row=3, column=col, padx=5, pady=5)


        for col, expense_category in enumerate(self.expenses_by_category):
            cell = tk.Button(self.frame, text="Add Expense", relief="solid", command=None, width=15, height=2)
            cell.grid(row=len(expense_category) + 3, column=col) # not sure why + 3 works

    def update_table(self):
        # Recreate the table with the updated column names
        self.create_table()


if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
