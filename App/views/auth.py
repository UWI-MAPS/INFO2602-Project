from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, flash, redirect, url_for, session # Import session
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies, get_jwt_identity

from.index import index_views
from App.controllers import (
    login
)

from App.models import User # Import User model (needed to fetch user if needed in route)
from App.models import Location # Import Location model
from App.controllers.admin import createLocation

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')

'''
Page/Action Routes
'''    

@auth_views.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@auth_views.route('/login', methods=['POST'])
def login_action():
    username = request.form.get('username')
    password = request.form.get('password')
    next_url = url_for('index_views.index_page') 
    token, user = login(username, password) 

    if token and user: 
        flash('Login Successful!', 'success')
        session['is_authenticated'] = True
        session['admin_id'] = user.id 
        response = redirect(next_url)
        set_access_cookies(response, token)
        return response
    else:
        return redirect(url_for('auth_views.login_page'))


@auth_views.route('/logout', methods=['GET'])
def logout_action():
    response = redirect(request.referrer or url_for('index_views.index_page')) 
    flash("Logged Out!", "info") 
    session.pop('is_authenticated', None)
    session.pop('admin_id', None)

    unset_jwt_cookies(response)
    return response

'''
API Routes
'''



@auth_views.route('/api/markers', methods=['POST'])
@jwt_required() # Protect this route - only authenticated users can create markers
def create_marker_api():
    current_admin_id = get_jwt_identity() # Get the user ID from the JWT

    data = request.json # Get JSON data sent from the frontend

    # Basic Server-Side Validation
    if not data:
        return jsonify({"msg": "No data provided"}), 400

    # Required fields check (match Location model)
    # Adjusted required fields based on Location model nullable=False
    required_fields = ['name', 'latitude', 'longitude']
    for field in required_fields:
        if field not in data or data[field] is None or (isinstance(data[field], str) and data[field].strip() == ''):
             return jsonify({"msg": f"Missing or empty required field: {field}"}), 400

    # Validate data types (especially numbers)
    try:
        latitude = float(data['latitude'])
        longitude = float(data['longitude'])
        # Floors is not on Location model, don't validate or try to parse here
    except (ValueError, TypeError) as e:
        return jsonify({"msg": f"Invalid data type for latitude or longitude: {e}"}), 400

    # Collect optional fields
    marker_type = data.get('type')
    description = data.get('description')
    image = data.get('image') # Use 'image' key as sent from frontend/matches model

    # Call your controller function to create the Location in the database
    # Pass only the fields that the createLocation function and Location model accept
    new_location = createLocation(
        admin_id=current_admin_id, # Pass the logged-in admin's ID
        name=data['name'],
        latitude=latitude,
        longitude=longitude,
        type=marker_type, # Pass the collected type
        description=description, # Pass the collected description
        image=image # Pass the collected image (URL/path)
        # Do NOT pass faculty or floors to createLocation as they are not Location fields
    )

    if new_location:
        # Return the created location data using its toJSON method
        return jsonify({"msg": "Marker created successfully", "marker": new_location.toJSON()}), 201 # 201 Created
    else:
        # Handle potential errors during creation (e.g., database error, validation in controller)
        return jsonify({"msg": "Failed to create marker in database"}), 500 # Internal Server Error
