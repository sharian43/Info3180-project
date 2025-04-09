# Add any form classes for Flask-WTF here
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, EmailField,IntegerField,FloatField
from wtforms.validators import InputRequired, Email
from flask_wtf.file import FileField, FileRequired, FileAllowed

class Signup(flaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = StringField('Password', validators=[InputRequired()])
    name=StringField('Name',validators=[InputRequired()])
    email=EmailField('Email',validators=[InputRequired(),Email()])
    photo=FileField('Photo',validators=[FileRequired(message="File is required!"),FileAllowed(['png','jpeg','jpg'])])

class Login(FlaskForm):
     username=StringField('Username',validators=[InputRequired()])
     password=PasswordField('Password',validators=[InputRequired()])

class Profiles(FlaskForm):
     description=TextAreaField('Description',validators=[InputRequired()])
     parish=StringField('Parish',validators=[InputRequired()])
     biography=TextAreaField('Biography',validator=[InputRequired()])
     sex=StringField('Sex',validators=[InputRequired(message="Male or Female")])
     race=StringField('Race',validators=[InputRequired()])
     birth_year=IntegerField('Parish',validators=[InputRequired()])
     height=FloatField('Height',validators=[InputRequired()])
     fav_cuisine=StringField('FavCuisine',validators=[InputRequired()])
     fav_color=StringField('FavColor',validators=[InputRequired()])
     fav_school_subject= StringField('FavSchoolSubject',validators=[InputRequired()])
     political=BooleanField('Political')
     religious=BooleanField('Religious')
     family_oriented=BooleanField('Family Oriented')
