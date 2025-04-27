import tkinter as tk
import tkinter.font as font
import createSheet

class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.root = master
        self.root.config(bg="white")
        self.styles = {
            "mainFrame": {"bg": "white"},
            "innerFrame": {"bg": "white"},
            "title": {"font": ("Helvetica", 40), "fg": "black", "bg": "white"},
            "button": {"bg": "lightblue", "fg": "black", "font": ("Helvetica", 20)}
        }
        self.create_sheet = None
        self.create_widgets()

    def create_widgets(self):
        # Create the main frame
        mainFrame = tk.Frame(self.root, **self.styles["mainFrame"])
        mainFrame.pack(fill=tk.BOTH, expand=True)

        # Create the inner frame
        innerFrame = tk.Frame(mainFrame, width=600, height=450, **self.styles["innerFrame"])
        innerFrame.pack(pady=50)  # Adds vertical space outside the frame

        # Add a label with the defined style
        label = tk.Label(innerFrame, text="Welcome to Freaky Finance 999!", **self.styles["title"])
        label.pack(pady=10)

        # Create a frame to wrap buttons for centering
        buttonFrame = tk.Frame(innerFrame, **self.styles["mainFrame"])
        buttonFrame.pack(pady=20)  # Adds space around the button frame

        # Add buttons inside the buttonFrame to horizontally center them
        createButton = tk.Button(buttonFrame, text="Create a sheet", command=self.link_to_create_sheet, **self.styles["button"])
        createButton.pack(side=tk.LEFT, padx=10)

        viewButton = tk.Button(buttonFrame, text="View sheets", command=self.link_to_view_sheets, **self.styles["button"])
        viewButton.pack(side=tk.LEFT, padx=10)

    def link_to_create_sheet(self):
        if self.create_sheet:  # If create_sheet already exists, destroy it
            self.create_sheet.destroy()
            self.create_sheet = None  
            return
        
        self.create_sheet = createSheet.App(self)  # Assuming createSheet.App() is another frame or window
        self.create_sheet.pack(fill=tk.BOTH, expand=True)
        
    def link_to_view_sheets(self):
        self.create_sheet.destroy()
        


