from flask import Flask, render_template, request, flash, redirect, url_for, session

import business_logic

app = Flask(__name__)
app.secret_key = 'some_secret'  # development only


# @TODO what should client store ? All the data necessary to recreate the services_list. That is: a lits of credentials per operator. What should be passed within session then? I guess the same. Every refresh should fetch the data from the operator

@app.route('/', methods=['GET'])
def entry():
    try:
        for cookied_account_str in session['accounts']:
            cookied_account = business_logic.Account.deserialize(cookied_account_str)
            if type(cookied_account) == business_logic.Account:
                # the client already has an account in theirs cookie
                return redirect(url_for('services_list'))
    except KeyError:
        pass
    return render_template('welcome.html')


@app.route('/services', methods=['POST'])
def services_add():
    if request.form['username'] and request.form['password']:
        # sanitize
        def sanitize_input(input):
            return input.strip()

        sanitized = {}
        for key in request.form.keys():
            sanitized[key] = sanitize_input(request.form[key])

        # maybe some loading screen
        print("checking")
        try:
            print(*sanitized.values())
            new_account = business_logic.Account.guess_operator(*sanitized.values())
        except LookupError:
            flash('Podane dane logowania są błędne. Żaden operator się do nich nie przyznaje', 'error')
        else:

            # add new service to the services
            try:
                new_account.fetch()
            except Exception as e:
                raise (e)  # idk
            else:
                duplicate_found = False
                sessions_accounts = []
                if 'accounts' in session:
                    # prune existing sessions from the cookie
                    sessions_accounts = session.get('accounts')

                    # check if already in session cookie
                    # does any's cookied subAccount number equals new subAccounts number?

                    for cookied_account_str in sessions_accounts:
                        cookied_account = business_logic.Account.deserialize(cookied_account_str)
                        for cookied_subAccount in cookied_account.subAccounts:
                            for new_subAccount in new_account.subAccounts:
                                if cookied_subAccount[business_logic.AccountSub.NUMBER] == \
                                        new_subAccount[business_logic.AccountSub.NUMBER]:
                                    # duplication
                                    duplicate_found = True

                if duplicate_found:
                    flash('Już masz to konto na swojej liście', 'error')
                    abort(302)
                else:
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
            print(account.client.friendly_name)
            for subAccount in account.subAccounts:
                try:
                    accounts_template.append(subAccount)
                except LookupError as e:
                    raise (e)  # our entry might got outdated, corrupted or emptied

    # else:
    #     from random import randint
    #     for _ in range(randint(1, 4)):
    #         accounts_template.append(
    #             {'msdin': randint(500_000_000, 899_999_999), 'operator': 'Dombo SA', 'GBdue': randint(0, 100_0) / 10,
    #              'dateDue': randint(0, 365)})

    accounts_template = sorted(accounts_template, key=lambda x: x['dateDue'])
    return (render_template('services_list.html', accounts=accounts_template))

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8000, debug=False)
