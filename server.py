from flask import Flask, render_template, request, flash, redirect, url_for, get_flashed_messages

app = Flask(__name__)
app.secret_key = 'some_secret'


@app.route('/', methods=['GET'])
def entry():
    return render_template('welcome.html')


@app.route('/', methods=['POST'])
def entry_form():
    if request.form['username'] and request.form['password']:
        # perform actual check
        # maybe some loading screen
        print("checking")
        return entry()
    else:
        # return alert/error, that fields cannot be left empty.
        if not request.form['username']:
            flash('Wypełnij pole „numer telefonu”')
        if not request.form['password']:
            flash('Wypełnij pole „hasło”')
        return redirect(url_for('entry'))


@app.route('/services')
def services_list():
    from random import randint
    accounts = [{'msdin': randint(500_000_000, 899_999_999), 'operator': 'Dombo SA', 'GBdue': randint(0, 100_0)/10,
                 'dateDue': randint(0, 365)} for _ in range(randint(1, 4))]
    accounts = sorted(accounts, key=lambda x: x['dateDue'])
    return (render_template('services_list.html', accounts=accounts))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
