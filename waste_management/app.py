from flask import Flask
from flask_restful import Api

from resource.Customer import Registration, UserList, UserLogin, UserLogout, UserDelete

from app_init import app,api,jwt
blocklist = set()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JWT_BLOCKLIST_ENABLED'] = True
app.config['JWT_BLOCKLIST_TOKEN_CHECKS'] = ['access', 'refresh']


@app.before_first_request
def init():
    db.create_all()

# @jwt.token_in_blocklist_loader
# def check_if_token_in_blocklist(decrypted_token):
#     jti = decrypted_token['jti']
#     return jti in blocklist
#     # return models.RevokedTokenModel.is_jti_blocklisted(jti)


# @jwt.token_in_blocklist_loader
# def check_if_token_in_blacklist(decrypted_token):
#     jti = decrypted_token["jti"]
#     return jti in blacklist

api.add_resource(Registration, '/auth/registration')
api.add_resource(UserLogin, '/auth/login')
api.add_resource(UserList, '/userlist')
api.add_resource(UserLogout, '/logout')
api.add_resource(UserDelete, '/delete')

# print(Test())

# api.add_resource(Admin, '/admin')
# api.add_resource(Vendor, '/vendor')

if __name__ == '__main__':
    from config import db
    db.init_app(app)
    app.run(port=5000, debug=True)
