from __future__ import unicode_literals
from django.db import models
import bcrypt

class UserManager(models.Manager):
    def validate(self, form_data):
        errors = []
        user_record = User.objects.filter(email=form_data['email']).first()
        if len(form_data['name']) < 3:
            errors.append("Name must contain at least three characters")
        if len(form_data['alias']) < 3:
            errors.append("Alias must contain at least three characters")
        if user_record:
            errors.append("Email has already been registered, please login or choose another")
        if len(form_data['email']) < 3:
            errors.append("Email must contain at least three characters")
        if len(form_data['password']) < 8:
            errors.append("Password must contain at least eight characters")
        if form_data['password'] != form_data['password_confirm']:
            errors.append("Password does not match password confirmation")
        print "Inside the validate method"
        return errors

    def createUser(self, form_data):
        password = str(form_data['password'])
        hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())

        user = User.objects.create(
        name = form_data['name'],
        alias = form_data['alias'],
        email = form_data['email'],
        password = hashed_pw,
        date_of_birth = form_data['date_of_birth'],
        )
        return user

    def validate_login(self, form_data):
        errors = []
        if len(form_data['email']) < 3:
            errors.append("Must submit a valid email")
        if len(form_data['password']) < 8:
            errors.append("Password must contain at least eight characters")
        return errors

    def login(self, form_data):
        errors = self.validate_login(form_data)

        if not errors:
            user = User.objects.filter(email = form_data['email']).first()
            if user:
                password = str(form_data['password'])
                user_password = str(user.password)
                hashed_pw = bcrypt.hashpw(password, user_password)
                if user.password == hashed_pw:
                    return user

            errors.append('Invalid email/password')

        return errors

class User(models.Model):
    name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    email = models.EmailField(max_length=45)
    password = models.CharField(max_length=45)
    date_of_birth = models.DateField()
    friends = models.ManyToManyField("self", related_name = "friended_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        string_output = " ID: {} Name: {} Alias: {} Email: {} Password: {}"
        return string_output.format(
        self.id,
        self.name,
        self.alias,
        self.email,
        self.password,
    )

    objects = UserManager()
