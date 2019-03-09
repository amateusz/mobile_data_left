from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'some_secret'


@app.route('/', methods=['GET'])
def entry():
    return render_template('dynamic.html')


@app.route('/', methods=['POST'])
def entry_form():
    if request.form['username'] and request.form['password']:
        # perform actual check
        # maybe some loading screen
        print("checking")
        return entry()
    else:
        # return alert/error, that fields cannot be left empty.
        flash('You were successfully logged in', 'error')
        return redirect(url_for('entry'))


if __name__ == '__main__':
    app.run()
