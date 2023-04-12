from flask_wtf import FlaskForm
from wtforms import fields, validators, widgets


class LoginForm(FlaskForm):

    username = fields.StringField(
        label='Имя пользователя', 
        validators=[validators.DataRequired()],
    )
    password = fields.PasswordField(
        label='Пароль', 
        validators=[validators.DataRequired()],
    )
    remember = fields.BooleanField(label='Запомнить меня')
    submit = fields.SubmitField(label='Войти')


class RegisterForm(FlaskForm):

    username = fields.StringField(
        label='Имя пользователя', 
        validators=[validators.DataRequired(), validators.Length(min=5, max=20)],
    )
    password = fields.PasswordField(
        label='Пароль', 
        validators=[validators.DataRequired(), validators.Length(min=8)],
    )
    password2 = fields.PasswordField(
        label='Повторите пароль', 
        validators=[validators.DataRequired(), validators.EqualTo('password')],
    )
    submit = fields.SubmitField(label='Зарегистрироваться')
    
class MultiCheckboxField(fields.SelectMultipleField):
    
    widget = widgets.ListWidget(prefix_label=False, html_tag='ul')
    option_widget = widgets.CheckboxInput()

class NewsForm(FlaskForm):

    title = fields.StringField(label='Название статьи', validators=[validators.DataRequired()])
    text = fields.TextAreaField(label='Текст статьи', validators=[validators.DataRequired()])
    categories = MultiCheckboxField(label='Категории', coerce=int)


class CreateForm(NewsForm):

    submit = fields.SubmitField(label='Создать')


class UpdateForm(NewsForm):

    submit = fields.SubmitField(label='Обновить')


class DeleteUserForm(FlaskForm):

    submit = fields.SubmitField(label='Удалить')
    cancel = fields.SubmitField(label='Отмена')


class EditUserForm(FlaskForm):

    username = fields.StringField(label='Имя пользователя', validators=[validators.DataRequired(), validators.Length(min=5, max=20)])
    password = fields.PasswordField(label='Пароль', validators=[validators.DataRequired(), validators.Length(min=8)])
    
    submit = fields.SubmitField(label='Применить')


class EditUserAdminForm(EditUserForm):
    
    username = fields.StringField(label='Имя пользователя', validators=[validators.DataRequired(), validators.Length(min=5, max=20)])
    password = fields.PasswordField(label='Пароль', validators=[validators.DataRequired(), validators.Length(min=8)])
    admin_level = fields.SelectField(
        label='Уровень администратора', 
        choices=[(0, 'Пользователь'), (1, 'Модератор'), (2, 'Администратор')],
    )
    
    submit = fields.SubmitField(label='Применить')


class CreateCategoryForm(FlaskForm):

    title = fields.StringField(label='Название категории', validators=[validators.DataRequired()])
    submit = fields.SubmitField(label='Создать')


class UpdateCategoryForm(FlaskForm):

    title = fields.StringField(label='Название категории', validators=[validators.DataRequired()])
    submit = fields.SubmitField(label='Обновить')


class CategorySelectForm(FlaskForm):

    categories = MultiCheckboxField(label='Категории', coerce=int)
    page = fields.HiddenField(default=1)
    
    submit = fields.SubmitField(label='Применить фильтр')
