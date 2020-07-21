from resources.user import UsersResources, UserResources, UserImageResources
from resources.role import RolesResources, RoleResources
from resources.auth import AuthResources
from resources.compare_image import CompareImageResources, CompareImagesResources


def init_routes(api):
    # User routes
    api.add_resource(UsersResources, '/api/users')
    api.add_resource(UserResources, '/api/users/<user_id>')
    api.add_resource(UserImageResources, '/api/users/image/<user_id>')
    # Role routes
    api.add_resource(RolesResources, '/api/roles')
    api.add_resource(RoleResources, '/api/roles/user')
    # Auth
    api.add_resource(AuthResources, '/api/signin')
    # Compare image
    api.add_resource(CompareImageResources, '/api/compare')
    api.add_resource(CompareImagesResources, '/api/compares')
