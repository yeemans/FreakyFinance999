# hello.py
from flask import Flask
#Flask is a micro web framework for Python,
# designed to enable the quick development of web applications.
#
# It is considered a "micro" framework because it provides only the essential components,
# such as routing and templating, leaving other functionalities like database interaction and
# form validation to be implemented through extensions or external libraries.
# This minimalist approach gives developers flexibility and control
# over their application's architecture.


app = Flask(__name__) # (1) Create Flask app instance

@app.route('/') # (2) Define a route for the root URL, this is a decorator
def hello_world(): # (3) View function for the route
    return '<p>Hello, World!</p>' # (4) Response returned to the browser

# Optional: Add for local running convenience
if __name__ == '__main__':
    # Runs the development server
    # debug=True enables auto-reloading and detailed error pages during development
    app.run(debug=True)

''' The Flask class is imported. An instance is created, passing __name__. 
This argument helps Flask locate resources like (WE will discuss about this in a bit) templates and static files relative to the application module.

Routing: The @app.route('/') decorator maps the URL path / to the hello_world function.
View Function: The hello_world() function is the view function associated with the / route. 
It contains the logic to handle requests to that URL.
Response: The function returns a simple HTML string. 
Flask wraps this string in an HTTP response object to send back to the client's browser.



Running the Development Server:
To run this application locally, you can use the Flask command-line interface. 
Open a terminal in the directory containing hello.py:
flask --app hello run

We added "if __name__ == '__main__':" , so we can run it directly: python hello.py

By default the server runs at http://127.0.0.1:5000
127.0.0.1 is a loopback address -> only good for interprocess or local machine. 
When we try on GCP - we must make minor adjustments to allow it to be accessible from any ip iddresses on the machine.
0.0.0.0 -> non-routable meta-address, so service listens to all ip addresses.

add a firewall rule to allow TCP connections (HTTP) on 5000.  
so your run will be updated to app.run(host='0.0.0.0', port=5000,debug=True)

Using nohup
The nohup command allows a process to continue running in the background, even after you disconnect from the SSH session.
Code

nohup python your_flask_app.py &

'''