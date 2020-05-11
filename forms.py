from wtforms import Form, StringField, validators, IntegerField, BooleanField, RadioField


class SearchForm(Form):
    searchVal = StringField('Search Value', validators=[validators.required()])


class ScrapeForm(Form):
    max_pages = IntegerField('Max pages', validators=[validators.required()])
    start_url = StringField('Start url', validators=[validators.required()])
    stay_on_domain = RadioField('Stay on domains', choices=['True', 'False'], validators=[validators.required()])
    update_existing = RadioField('Update existing database ?', choices=['True', 'False'], validators=[validators.required()])