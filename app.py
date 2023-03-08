from flask import Flask, request, render_template
from my_classes import MyForm, UserEstimate, Temperature


app = Flask(__name__)

app.secret_key = 'mysecretkey'  # store as environment variable


@app.route('/', methods=['GET', 'POST'])
def myform():
    form = MyForm()

    if form.validate_on_submit():
        user_name = form.name.data
        user_weight = form.weight.data
        user_height = form.height.data
        user_age = form.age.data
        user_country = form.country.data
        user_city = form.city.data
        calculated_field = float(user_weight) * float(user_height)
        my_user = UserEstimate(user_weight, user_height, user_age, temperature=10)
        user_method_check = my_user.test_method()
        return render_template('index.html', form=form, name=user_name, weight=user_weight,
                               age=user_age, country=user_country,
                               city=user_city, method_check=user_method_check,
                               calc_field=calculated_field)

    return render_template('index.html', form=form)


app.run()
