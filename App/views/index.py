from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, current_app, session
from App.controllers import create_user, initialize
from App.models import User, Location # Import User and Location models

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    google_maps_api_key = current_app.config['GOOGLE_MAPS_API_KEY']

    # Fetch all Location markers from the database
    try:
        # Fetch Location objects and convert them to dictionaries using toJSON
        all_locations = Location.query.all()
        all_locations_data = [location.toJSON() for location in all_locations]
        print(f"Fetched {len(all_locations_data)} locations for initial load.")
    except Exception as e:
        print(f"Error fetching locations for initial load: {e}")
        all_locations_data = [] # Return empty list on error


    # Pass the list of location data (as dictionaries) to the template
    # Pass authentication status and user object from session for conditional UI
    return render_template(
        'index.html',
        google_maps_api_key=google_maps_api_key,
        show_map=True, # Assuming this controls map visibility in layout.html
        markers=all_locations_data, # <<< Pass the location data
        is_authenticated=session.get('is_authenticated', False), # Pass auth status
        # Pass user object if logged in (used by {{ current_user.username }} in index.html)
        current_user=User.query.get(session.get('admin_id')) if session.get('is_authenticated') else None
    )
    
@index_views.route('/init', methods=['GET'])
def init():
    initialize()
    return jsonify(message='db initialized!')
