from flask import Flask

app = Flask(__name__) # Create a Flask application instance

@app.route('/') # Define the route for the home page
def home(): # Define the view function for the home page
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True) # Run the application in debug mode