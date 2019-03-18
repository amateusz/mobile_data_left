from flask import Flask, render_template, request, flash, redirect, url_for, session

import business_logic

app = Flask(__name__)
app.secret_key = 'some_secret'  # development only


# @TODO what should client store ? All the data necessary to recreate the services_list. That is: a lits of credentials per operator. What should be passed within session then? I guess the same. Every refresh should fetch the data from the operator

@app.route('/', methods=['GET'])
def entry():
    return render_template('welcome.html')


@app.route('/services', methods=['POST'])
def services_add():
    if request.form['username'] and request.form['password']:
        # perform actual check
        # maybe some loading screen
        print("checking")
        try:
            new_account = business_logic.Account.guess_operator(*request.form.values())
        except LookupError:
            flash('Podane dane logowania są błędne. Żaden operator się do nich nie przyznaje', 'error')
        else:
            # add new service to the services
            sessions_accounts = []
            if 'accounts' in session:
                sessions_accounts = session.pop('accounts')
            sessions_accounts.append(business_logic.Account.serialize(new_account))
            session['accounts'] = sessions_accounts

            session.permanent = True

        return redirect(url_for('services_list'))
    else:
        # this should never happen, as we validate client side. BUT STILL
        return redirect(request.path)


@app.route('/services')
def services_list():
    '''
    @TODO: take something as an input. either JWT or session cookie... or both. / Currently session cookie
    :return:
    '''

    accounts_template = []

    if 'accounts' in session:
        for account_str in session['accounts']:
            account = business_logic.Account.deserialize(account_str)
            for subAccount in account.subAccounts:
                try:
                    accounts_template.append(subAccount.dict())
                except LookupError as e:
                    raise (e) # our entry might got outdated, corrupted or emptied

    else:
        from random import randint
        for _ in range(randint(1, 4)):
            accounts_template.append(
                {'msdin': randint(500_000_000, 899_999_999), 'operator': 'Dombo SA', 'GBdue': randint(0, 100_0) / 10,
                 'dateDue': randint(0, 365)})

    accounts_template = sorted(accounts_template, key=lambda x: x['dateDue'])
    return (render_template('services_list.html', accounts=accounts_template))

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8000, debug=False)
