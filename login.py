from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import User, Sheet
import bcrypt
import tkinter as tk
import main

engine = create_engine('sqlite:///database.db')  # or your DB of choice
Session = sessionmaker(bind=engine)
session = Session()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.styles = {
            "mainFrame": {"bg": "white"},
            "innerFrame": {"bg": "white"},
            "title": {"font": ("Helvetica", 40), "fg": "black", "bg": "white"},
            "button": {"bg": "lightblue", "fg": "black", "font": ("Helvetica", 20)}
        }
        self.error_label = tk.Label(self, text="")
        self.error_label.place(x=150, y=100) 
        self.create_widgets()

    # Method to set the password (hashes it before storing)
    def generate_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Method to check the password
    def check_password(self, username, password):
        user = session.query(User).filter(User.username == username).first()
        if not user:
            self.error_label.config(text="Login not recognized.")  
            return
        
        password_hash = user.password_hash
        logged_in = bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
        if logged_in: 
            self.show_main_page()
        else:
            self.error_label.config(text="Login not recognized.") 

    def register(self, username, password):
        password_hash = self.generate_password(password)
        user_model = User(username=username, password_hash=password_hash)
        
        try:
            session.add(user_model)
            session.commit()
            self.show_main_page()
        except:
            session.rollback()
            self.error_label.config(text="Username is in use.")  

    def create_widgets(self):
        # Defining the first row
        lblfrstrow = tk.Label(self, text ="Username -", )
        lblfrstrow.place(x = 50, y = 20)
        
        self.Username = tk.Entry(self, width = 35)
        self.Username.place(x = 150, y = 20, width = 100)
        
        lblsecrow = tk.Label(self, text ="Password -")
        lblsecrow.place(x = 50, y = 50)
        
        self.password = tk.Entry(self, width = 35)
        self.password.place(x = 150, y = 50, width = 100)
        
        loginbtn = tk.Button(self, text ="Login", 
                            bg ='blue', command =lambda: self.check_password(self.Username.get(), self.password.get()))
        loginbtn.place(x = 150, y = 135, width = 55)

        registerbtn = tk.Button(self, text ="Register", 
                            bg ='blue', command =lambda: self.register(self.Username.get(), self.password.get()))
        registerbtn.place(x = 250, y = 135, width = 55)

    def show_main_page(self):
        # get id of logged in user
        user = session.query(User).filter(User.username == self.Username.get()).first()
        self.UserID = user.UserID
        self.main_page = main.App(self)
        self.main_page.pack()

if __name__ == "__main__":
    app = App()
    app.attributes("-fullscreen", True)
    app.mainloop()

    #print(app.check_password("bluea88", "gobluea88"))