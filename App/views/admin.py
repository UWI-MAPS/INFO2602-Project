from flask_admin.contrib.sqla import ModelView
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies
from flask_admin import Admin
from flask import render_template, flash, redirect, request, url_for  
from App.models import db, User 
class AdminView(ModelView):

    @jwt_required()
    def is_accessible(self):
        return current_user is not None

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        flash("Login to access admin")
        return redirect(url_for('index_page', next=request.url))

def setup_admin(app):
    admin = Admin(app, name='FlaskMVC', template_mode='bootstrap3')
    admin.add_view(AdminView(User, db.session))

#from flask import Blueprint
#admin_views = Blueprint('admin_views', __name__, template_folder='../templates')

#@admin_views.route('/admin/locations')
#@jwt_required()
#def admin_locations():
#    locations = Location.query.all()
#    return render_template('admin/manage_locations.html', locations=locations, is_authenticated=True)

#@admin_views.route('/admin/buildings')
#@jwt_required()
#def admin_buildings():
#    buildings = BuildingDetails.query.all()
#    return render_template('admin/manage_buildings.html', buildings=buildings, is_authenticated=True)

#@admin_views.route('/admin/rooms')
#@jwt_required()
#def admin_rooms():
#    rooms = Room.query.all()
#    return render_template('admin/manage_rooms.html', rooms=rooms, is_authenticated=True)