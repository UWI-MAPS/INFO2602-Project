from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, current_app
from App.controllers import create_user, initialize

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    google_maps_api_key = current_app.config['GOOGLE_MAPS_API_KEY']
    return render_template('index.html', google_maps_api_key=google_maps_api_key, show_map=True)

@index_views.route('/init', methods=['GET'])
def init():
    initialize()
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})