import os
from flask_admin import Admin
from models import db, User, Planet, People, Vehicle, Favorite
from flask_admin.contrib.sqla import ModelView
from markupsafe import Markup

def favorite_user_formatter(view, context, model, name):
    favorites = getattr(model, name)
    user_list = []
    for fav in favorites:
        user_name = fav.user_item.name if fav.user_item else "Usuario Desconocido"
        user_list.append(user_name)
    return Markup(", ".join(user_list))

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    class User_admin(ModelView):
        column_list= ["id", "username", "name", "email", "password", "subscription_date", "upgrade", "favorites_item"]

    class People_admin(ModelView):
        column_list= ["id", "full_name", "gender", "description", "height", "url", "favorite_people"]
        column_formatters = {'favorite_people': favorite_user_formatter}

    class Planets_admin(ModelView):
        column_list= ["id", "name", "climate", "description", "population", "url", "favorite_planets"]
        column_formatters = {'favorite_planets': favorite_user_formatter}

    class Vehicles_admin(ModelView):
        column_list= ["id", "name", "model", "description", "capacity", "url", "favorite_vehicles"]
        column_formatters = {'favorite_vehicles': favorite_user_formatter}

    class Favorite_admin(ModelView):
        column_list= ["id", "user_id", "planet_id", "people_id", "vehicle_id", "user_item", "planet_item", "people_item", "vehicle_item"]

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(User_admin(User, db.session))
    admin.add_view(People_admin(People, db.session))
    admin.add_view(Planets_admin(Planet, db.session))
    admin.add_view(Vehicles_admin(Vehicle, db.session))
    admin.add_view(Favorite_admin(Favorite, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))