from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField, DateField
from wtforms.validators import DataRequired

class CreateWorkOrderForm(FlaskForm):
    client_name = StringField('Client Name')
    job_address = StringField('Job Address')
    floor_prep = StringField('Floor Preparation')
    floor_type = SelectField('Flooring Type', choices=[('glue down', 'Glue Down'), ('vinyl', 'Vinyl'), ('laminate', 'Laminate'), ('floating', 'Floating')])
    baseboards = StringField('Baseboard')
    materials = TextAreaField('Materials')
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Create Work Order')