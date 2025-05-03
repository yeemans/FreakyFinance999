import json
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
        self.create_sheet = master.create_sheet
        self.view_sheet = None

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
        if self.create_sheet: 
            self.create_sheet.destroy()
            self.create_sheet = None
        selected_item = self.treeview.selection()
        if not selected_item: return

        self.loading_sheet = True
        # Retrieve the values of the selected item
        item_values = self.treeview.item(selected_item[0])["values"]
        self.SheetID = item_values[0]
        self.title = item_values[1]
        self.start_date = self.reformat_date(item_values[2])
        self.end_date = self.reformat_date(item_values[3])

        # get columns and expenses
        sheet = session.query(Sheet).filter(Sheet.SheetID == self.SheetID).first()
        self.expenses_by_category = json.loads(sheet.json_string)

        # display the createSheet
        if self.view_sheet: 
            self.view_sheet.destroy()
            self.view_sheet = None

        # destroy the treeview when quitting
        self.destroy()
        self.view_sheet = createSheet.App(self)  # Assuming createSheet.App() is another frame or window
        self.view_sheet.pack(fill=tk.BOTH, expand=True)

    def reformat_date(self, date_string):
        year_month_date = date_string.split("-")
        return f"{year_month_date[1]}/{year_month_date[2]}/{year_month_date[0]}"
    
    def destroy(self):
        if self.select_sheet_button:
            self.select_sheet_button.destroy()
            self.select_sheet_button = None

        if self.treeview:
            self.treeview.destroy()
            self.treeview = None
        