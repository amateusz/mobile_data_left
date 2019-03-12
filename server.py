from flask import Flask, render_template, request, flash, redirect, url_for, get_flashed_messages
import business_logic

app = Flask(__name__)
app.secret_key = 'some_secret'


@app.route('/', methods=['GET'])
def entry():
    return render_template('welcome.html')


@app.route('/services', methods=['POST'])
def services_add():
    print(request.path, request.host_url)
    if request.form['username'] and request.form['password']:
        # perform actual check
        # maybe some loading screen
        print("checking")
        try:
            new_service = business_logic.Service.guess_service(*request.form)
        except LookupError:
            flash('Podane dane logowania są błędne. Żaden operator się do nich nie przyznaje', 'error')

        # add new service to the services
        return redirect(url_for('services_list'))
    else:
        # return alert/error, that fields cannot be left empty.
        if not request.form['username']:
            flash('Wypełnij pole „numer telefonu”')
        if not request.form['password']:
            flash('Wypełnij pole „hasło”')
        return redirect(request.path)


@app.route('/services')
def services_list():
    from random import randint
    accounts = [{'msdin': randint(500_000_000, 899_999_999), 'operator': 'Dombo SA', 'GBdue': randint(0, 100_0) / 10,
                 'dateDue': randint(0, 365)} for _ in range(randint(1, 4))]
    accounts = sorted(accounts, key=lambda x: x['dateDue'])
    return (render_template('services_list.html', accounts=accounts))

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8000, debug=False)
