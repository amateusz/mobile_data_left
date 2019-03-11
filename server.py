from flask import Flask, render_template, request, flash, redirect, url_for, get_flashed_messages

server = Flask(__name__)
server.secret_key = 'some_secret'


@server.route('/', methods=['GET'])
def entry():
    return render_template('welcome.html')


@server.route('/', methods=['POST'])
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


@server.route('/services')
def services_list():
    accounts = [{'msdin': 123123123, 'operator': 'Dombo SA', 'GBdue': 12.5, 'dateDue': 13},
                {'msdin': 123123123, 'operator': 'Dombo SA', 'GBdue': 12.5, 'dateDue': 13},
                {'msdin': 123123123, 'operator': 'Dombo SA', 'GBdue': 12.5, 'dateDue': 13},
                {'msdin': 123123123, 'operator': 'Dombo SA', 'GBdue': 12.5, 'dateDue': 13}]
    return (render_template('services_list.html', accounts=accounts))


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=8000, debug=False)
