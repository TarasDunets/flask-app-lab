from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!', 200

@app.route('/homepage') 
def home():
    """View for the Home page of your website."""
    agent = request.user_agent
    
    return "This is your homepage :) - {agent}"
    
if __name__ == '__main__':
    app.run(debug=True)
