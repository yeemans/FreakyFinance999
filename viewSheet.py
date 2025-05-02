import tkinter as tk
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tkinter import ttk
from database import Sheet
import createSheet

engine = create_engine('sqlite:///database.db')  # or your DB of choice
Session = sessionmaker(bind=engine)
session = Session()

class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.root = master
        self.UserID = master.UserID
        self.sheets = self.get_sheets()


    def get_sheets(self):
        sheets = session.query(Sheet).filter(Sheet.UserID == self.UserID).all()
        print(sheets)

        self.treeview = ttk.Treeview(self.root, columns=("ID", "title", "Start", "End"))
        # Hide the first column (column #0)
        self.treeview.heading("#0", text="")  # Remove the header of the first column
        self.treeview.column("#0", width=0, stretch=tk.NO)  # Set the column width to 0 and make it non-stretchable

        self.treeview.heading("#1", text="ID")
        self.treeview.heading("#2", text="Title")
        self.treeview.heading("#3", text="Start")
        self.treeview.heading("#4", text="End")
       

        for sheet in sheets:
            self.treeview.insert("", 0, values=(sheet.SheetID, sheet.title, sheet.start_date, sheet.end_date))

        self.select_sheet_button = tk.Button(self, text="View Selected Sheet", command=self.view_sheet)
        self.select_sheet_button.pack()
        self.treeview.pack(expand=True, fill=tk.BOTH)

    def view_sheet(self):
        selected_item = self.treeview.selection()
        if not selected_item: return

        self.loading_sheet = True
        # Retrieve the values of the selected item
        item_values = self.treeview.item(selected_item[0])["values"]
        print(item_values)
        self.sheet_id = item_values[0]
        self.title = item_values[1]
        self.start_date = item_values[2]
        self.end_date = item_values[3]

        # get columns and expenses
        sheet = session.query(Sheet).filter(Sheet.SheetID == self.sheet_id).first()
        self.expenses_by_category = sheet.json_string
        print(self.expenses_by_category)


        