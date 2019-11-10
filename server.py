from flask import Flask, render_template, request, redirect, url_for, flash, Response
import bcrypt
import common, validation


from wtforms import Form, BooleanField, StringField, PasswordField, validators

class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])




app = Flask(__name__)

LABELS = ["Id", "Story Title", "User Story", "Acceptance Criteria", "Business value", "Estimation", "Status"]


def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


@app.route('/set-cookie')
def cookie_insertion():
    redirect_to_index = redirect('/')
    response = Flask.make_response(redirect_to_index)
    response.set_cookie('cookie-name', value='values')
    return response


@app.route('/')
@app.route('/list')
def route_index():
    user_story_data = common.get_data_from_file()
    table_headers = LABELS
    try:
        if user_story_data is None:

            return render_template("index.html")  # tested - works
        else:

            return render_template("index.html",
                                   user_story_data=user_story_data,
                                   table_headers=table_headers)
    except Exception as e:
        return render_template('error.html', error=str(e))


@app.route('/story/', methods=['GET'])
def route_add():
    try:
        return render_template("add.html")
    except Exception as e:
        return render_template('error.html', error=str(e))


@app.route('/story/', methods=['POST'])
def add_story():
    try:
        business_value = request.form["Business value"]
        estimation = request.form["Estimation"]
        business_value_error = validation.validate_business_value(business_value)
        estimation_error = validation.estimation_value(estimation)

        if business_value_error == '' and estimation_error == '':
            form = request.form.to_dict()
            common.save_row_to_file(form)

            return redirect(url_for('route_index'))
        else:

            return render_template("add.html",
                                   business_value_error=business_value_error,
                                   estimation_error=estimation_error)
    except Exception as e:
        return render_template("error.html", error=str(e))


@app.route('/story/str:<story_id>', methods=['GET'])
def route_edit(story_id):
    try:
        stories = common.get_data_from_file()
        story_dict = stories[int(story_id)]  # dictionary within the list

        return render_template("edit.html",
                               story_dict=story_dict,
                               story_id=story_id,
                               statuses=common.STATUSES,
                               edit=story_dict)
    except Exception as e:
        return render_template("error.html", error=str(e))


@app.route('/story/<story_id>', methods=['POST'])
def edit_story(story_id: int):
    try:
        stories = common.get_data_from_file()
        story_dict = stories[int(story_id)]

        business_value = request.form["Business value"]
        estimation = request.form["Estimation"]
        business_value_error = validation.validate_business_value(business_value)
        estimation_error = validation.estimation_value(estimation)

        if business_value_error == '' and estimation_error == '':
            story = request.form.to_dict()
            common.update_story(story_id, story)

            return redirect(url_for('route_index'))
        else:

            return render_template("edit.html",
                                   business_value_error=business_value_error,
                                   estimation_error=estimation_error,
                                   story_dict=story_dict,
                                   story_id=story_id,
                                   statuses=common.STATUSES)
    except Exception as e:
        return render_template('error.html', error=str(e))


@app.errorhandler(404)  # Flask build-in decorator
def page_not_found(e):
    return render_template("error.html", error=str(e))


@app.route('/registration', methods=['GET'])
def show_registration_page():

    return render_template('register_form.html')


@app.route('/registration', methods=['POST'])
def register_new_user():
    #user_name = request.form.get('user_name')
    #password = request.form.get('password')
    #repeated_password = request.form.get('repeat_password')
    #return redirect(url_for("route_index"))

    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data,
                    form.password.data)
        #db_session.add(user)
        flash('Thanks for registering')
        return redirect(url_for('show_registration_page'))
    return render_template('register_form.html', form=form)




if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
