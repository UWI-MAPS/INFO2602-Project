from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.controllers import create_user, initialize
from App.models import Location, BuildingDetails

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@index_views.route('/init', methods=['GET'])
def init():
    initialize()
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})

@index_views.route('/location/<int:id>', methods=['GET'])
def location_detail(id):
    location = Location.query.get_or_404(id)
    return render_template('location_detail.html', location=location, is_authenticated=True)

@index_views.route('/building/<int:id>', methods=['GET'])
def building_detail(id):
    building = BuildingDetails.query.get_or_404(id)
    return render_template('building_detail.html', building=building, is_authenticated=True)
