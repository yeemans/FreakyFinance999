from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import User, Sheet
import bcrypt
import tkinter as tk

engine = create_engine('sqlite:///database.db')  # or your DB of choice
Session = sessionmaker(bind=engine)
session = Session()


class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.config(bg="white")
        self.styles = {
            "mainFrame": {"bg": "white"},
            "innerFrame": {"bg": "white"},
            "title": {"font": ("Helvetica", 40), "fg": "black", "bg": "white"},
            "button": {"bg": "lightblue", "fg": "black", "font": ("Helvetica", 20)}
        }

        self.create_widgets()
    # Method to set the password (hashes it before storing)
    def generate_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Method to check the password
    def check_password(self, username, password):
        user = session.query(User).filter(User.username == username).first()
        if not user: return False

        password_hash = user.password_hash
        print(bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')))
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

    def register(self, username, password):
        password_hash = self.generate_password(password)
        user_model = User(username=username, password_hash=password_hash)
        
        session.add(user_model)
        session.commit()

    def create_widgets(self):
        # Defining the first row
        lblfrstrow = tk.Label(root, text ="Username -", )
        lblfrstrow.place(x = 50, y = 20)
        
        Username = tk.Entry(root, width = 35)
        Username.place(x = 150, y = 20, width = 100)
        
        lblsecrow = tk.Label(root, text ="Password -")
        lblsecrow.place(x = 50, y = 50)
        
        password = tk.Entry(root, width = 35)
        password.place(x = 150, y = 50, width = 100)
        
        submitbtn = tk.Button(root, text ="Login", 
                            bg ='blue', command =lambda: self.check_password(Username.get(), password.get()))
        submitbtn.place(x = 150, y = 135, width = 55)
  

    def on_button_click(self):
        print("Button clicked!")

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()

    #print(app.check_password("bluea88", "gobluea88"))