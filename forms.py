from wtforms import Form, StringField, validators


class SearchForm(Form):
    searchVal = StringField('Search Value', validators=[validators.required()])
