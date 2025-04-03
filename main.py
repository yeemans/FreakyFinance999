import tkinter as tk

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.config(bg="white")
        self.styles = {
            "mainFrame": {"bg": "white"},
            "innerFrame": {"bg": "white"},
            "label": {"font": ("Helvetica", 14), "fg": "black", "bg": "white"},
            "button": {"bg": "lightgreen", "fg": "black", "font": ("Helvetica", 12)}
        }

        self.create_widgets()

    def create_widgets(self):
        # Create the main frame
        mainFrame = tk.Frame(self.root, **self.styles["mainFrame"])
        mainFrame.pack(fill=tk.BOTH, expand=True)

        # Create the inner frame
        innerFrame = tk.Frame(mainFrame, width=600, height=450, **self.styles["innerFrame"])
        innerFrame.pack(pady=50)  # Adds vertical space outside the frame

        # Add a label with the defined style
        label = tk.Label(innerFrame, text="Welcome to Freaky Finance 999!", **self.styles["label"])
        label.pack(pady=10)

        # Create a frame to wrap buttons for centering
        buttonFrame = tk.Frame(innerFrame, **self.styles["mainFrame"])
        buttonFrame.pack(pady=20)  # Adds space around the button frame

        # Add buttons inside the buttonFrame to horizontally center them
        createButton = tk.Button(buttonFrame, text="Create a sheet", command=self.on_button_click, **self.styles["button"])
        createButton.pack(side=tk.LEFT, padx=10)

        viewButton = tk.Button(buttonFrame, text="View sheets", command=self.on_button_click, **self.styles["button"])
        viewButton.pack(side=tk.LEFT, padx=10)

    def on_button_click(self):
        print("Button clicked!")

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
