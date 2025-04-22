from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity, verify_jwt_in_request

from App.models import User

def login(username, password):
  user = User.query.filter_by(username=username).first()
  if user and user.check_password(password):
    return create_access_token(identity=user.id)
  return None


def setup_jwt(app):
    jwt = JWTManager(app)

    # Configure Flask-JWT to resolve get_current_identity() to the corresponding user's ID
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        # Return the user ID directly
        return user if isinstance(user, int) else user.id

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.get(identity)  # Ensure this resolves to a valid user

    return jwt


# Context processor to make 'is_authenticated' available to all templates
def add_auth_context(app):
    @app.context_processor
    def inject_user():
        try:
            verify_jwt_in_request(optional=True)  # Allow requests without a token
            user_id = get_jwt_identity()
            current_user = User.query.get(user_id)
            is_authenticated = True
        except Exception as e:
          print(e)
          is_authenticated = False
          current_user = None
        return dict(is_authenticated=is_authenticated, current_user=current_user)