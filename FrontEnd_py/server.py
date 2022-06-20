from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')

# Creating simple Routes 
@app.route('/test')
def test():
    return "Home Page"

@app.route('/test/about/')
def about_test():
    return "About Page"

# Routes to Render Something
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about', strict_slashes=False)
def about():
    return render_template("about.html")

# Make sure this we are executing this file
if __name__ == '__main__':
    app.run(port = 1313, debug=True)  #La applicacion está en mododo de prueba, gracias a esta linea cada vez que cambio algo se reinicia el servidor