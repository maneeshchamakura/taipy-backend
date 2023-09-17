from flask import Flask, request, session, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Set a secret key for session management
api = Api(app)

# Dummy user data for demonstration
users = {
    'maneesh': {'password': 'securepassword'}
}

# Login Resource
class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        print("hello")
        # Check if user exists and password is correct
        if username in users and users[username]['password'] == password:
            # Simulate receiving a JWT token from a third-party API
            jwt_token = "your_received_jwt_token"

            # Store the JWT token in the session
            session['jwt_token'] = jwt_token

            return {'message': 'Login successful'}, 200
        else:
            return {'message': 'Invalid credentials'}, 401

# Protected Resource
class ProtectedResource(Resource):
    def get(self):
        # Check if the JWT token is present in the session
        if 'jwt_token' in session:
            jwt_token = session['jwt_token']

            # You can add logic here to verify the JWT token if needed
            # For simplicity, we assume the token is valid

            return {'message': 'Access granted for protected route', 'jwt_token': jwt_token}, 200
        else:
            return {'message': 'Access denied'}, 401

# Add resources to the API
api.add_resource(LoginResource, '/login')
api.add_resource(ProtectedResource, '/protected')

if __name__ == '__main__':
    app.run(debug=True)
