from flask import Flask, request, render_template, \
    redirect

from model_sqlite import createTables, \
    createCode, \
    getCode, \
    getAllCode, \
    updateCode, \
    createEdition, \
    getEdition

from colorizing import colorize

app = Flask(__name__)
createTables()

# ---------------------------------------------------------

@app.route('/')
def index():
    data = getAllCode()
    html = []

    for row in data :
        d = dict(
            uid = row[0],
            code = colorize(row[1], row[2]),
            language = row[2]
        )

        html.append(d)

    return render_template('index.html', data = html)

# ---------------------------------------------------------

@app.route('/create/')
def create():
    uid = createCode()
    createEdition(uid, request.remote_addr, request.user_agent.string)
    return redirect("{}edit/{}".format(request.host_url,uid))

# ---------------------------------------------------------

@app.route('/edit/<string:uid>/')
def edit(uid):
    row = getCode(uid)

    if row is None:
        return render_template('error.html',uid = uid)

    d = dict(
        uid=uid,
        code=row[0],
        language=row[1],
        url="{}view/{}".format(request.host_url,uid)
    )

    return render_template('edit.html', **d) 

# ---------------------------------------------------------

@app.route('/publish',methods=['POST'])
def publish():
    code = request.form['code']
    uid  = request.form['uid']
    language  = request.form['language']

    updateCode(uid, code, language)
    createEdition(uid, request.remote_addr, request.user_agent.string)

    return redirect(
        "{}{}/{}".format(request.host_url,
        request.form['submit'],
        uid)
    )

# ---------------------------------------------------------

@app.route('/view/<string:uid>/')
def view(uid):
    row = getCode(uid)

    if row is None:
        return render_template('error.html',uid = uid)

    d = dict(
        uid=uid,
        code = colorize(row[0], row[1]),
        language=row[1],
        url="{}view/{}".format(request.host_url,uid)
    )

    return render_template('view.html', **d)

# ---------------------------------------------------------

@app.route('/admin/')
def admin():
    return render_template('admin.html', data = getEdition())

# ---------------------------------------------------------

if __name__ == '__main__':
    app.run()

