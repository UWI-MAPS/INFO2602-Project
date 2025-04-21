from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, flash, redirect, url_for, session # Import session
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies, get_jwt_identity


from.index import index_views
from App.controllers import (
    login
)

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



@auth_views.route('/api/login', methods=['POST'])
def user_login_api():
    data = request.json
    token = login(data['username'], data['password'])
    if not token:
        return jsonify(error='Bad username or password given'), 401
    response = jsonify(redirect='/', access_token=token)
    set_access_cookies(response, token)
    return response

@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user():
    return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})

@auth_views.route('/api/logout', methods=['GET'])
def logout_api():
    response = jsonify(message="Logged Out!")
    unset_jwt_cookies(response)
    return response