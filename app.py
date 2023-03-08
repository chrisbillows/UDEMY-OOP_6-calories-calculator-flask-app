from flask import Flask, render_template
from my_classes import MyForm, User, Location


app = Flask(__name__)

app.secret_key = 'mysecretkey'  # store as environment variable


@app.route('/', methods=['GET', 'POST'])
def myform():
    form = MyForm()

    if form.validate_on_submit():

        # assign intermediate variables for own understanding later
        user_name = form.name.data
        user_weight = float(form.weight.data)
        user_height = float(form.height.data)
        user_age = float(form.age.data)
        user_country = form.country.data
        user_city = form.city.data

        # instantiate a location object based on user input
        user_location = Location(user_country, user_city)
        # scrape temp with get_temp method
        user_temp = user_location.get_temp()

        # instantiate a user
        my_user = User(user_weight, user_height, user_age, user_temp)
        #
        user_calorie_estimate = my_user.calculate_estimate_instructor_formula()

        return render_template('index.html', form=form, name=user_name, calories=user_calorie_estimate)

    return render_template('index.html', form=form)


app.run()
