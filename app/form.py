from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, ValidationError
import datetime

# Creating an input form that allows the user to input the date and how much of each meat type they have eaten that day.
class InputForm(FlaskForm):
    date = DateField('Date', validators = [DataRequired()])
    poultry = IntegerField('Amount of poultry eaten in grams')
    pork = IntegerField('Amount of pork eaten in grams')
    beef = IntegerField('Amount of beef eaten in grams')
    submit = SubmitField('Save')

    # The input date cannot be in the future.
    def validate_date(form, field):
        if field.data > datetime.date.today():
            raise ValidationError("The date cannot be in the future!")

# A form for the deletion of entries, the only input required is the date, for which all entries will be deleted.
class DeleteForm(FlaskForm):
    date = DateField('Select date to delete entries', validators = [DataRequired()])
    submit = SubmitField('Delete')
