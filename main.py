from flask import Flask, render_template, request
import map
from twitter2 import get_info_by_nickname
app = Flask(__name__)


@app.route("/", methods=['GET'])
def index1():
    """
    This function returns web page 'index.html'
    """
    return render_template("index.html")


@app.route("/map", methods=['POST'])
def index3():
    """
    This function returns web page 'friends.html'
    if Twitter nickname exsists, and returns
    string "There are no user with this nickname."
    otherwise.
    """
    nick = request.form['nickname']
    try:
        f_dict = get_info_by_nickname(nick)
        contex = {"html_string": map.web_map(f_dict)}
        return render_template("friends.html", **contex)
    except:
        return "There are no user with this nickname."


@app.errorhandler(404)
def invalid_route(e):
    """
    This function returns web page 'index.html'
    if error 404 is raised.
    """
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=4237)
