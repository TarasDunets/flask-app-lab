from flask import Flask, request, url_for

app = Flask(__name__)
app.config.from_pyfile("config.py")

@app.route('/')
def hello_world():
    return 'Hello, World!', 200

@app.route('/homepage') 
def home():
    """View for the Home page of your website."""
    agent = request.user_agent

    return "This is your homepage :) - {agent}"

@app.route("/hi/<string:name>/<int:age>")
def greetings(name, age):
    name = name.upper()
    age = request.args.get("age", 0, int)
    year = 2024 - age

    return f"Welcome, {name} {year}"

@app.route("/admin")
def admin():
    to_url = url_for("greetings", name="administrator", age=45, _external=True)     # "http://localhost:8080/hi/administrator?age=45"
    print(to_url)
    return redirect(to_url)

if __name__ == '__main__':
    app.run(debug=True)
