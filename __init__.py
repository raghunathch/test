""" Defining Routes for the API """
from package_as_a_service.core.patch import Api
from package_as_a_service.apis.contacts import namespace as contact
from package_as_a_service.apis.authentication import namespace as token
from package_as_a_service.apis.test_code import namespace as testing
from package_as_a_service.apis.queryserver import namespace as connection

authorizations = {
    'oauth2_implicit': {
        'type': 'oauth2',
        'flow': 'implicit',
        'authorizationUrl': 'https://sso.sgmarkets.com/sgconnect/oauth2/authorize',
        'scopes': {
            'openid': 'OpenID connect scope',
            'itaas': 'ITaaS profil',
            'profile': 'For Active directory login'
        }
    }
}

api = Api(title='Package As a Service API',
          version='0.1',
          description=' "Unix packge as a service"',
          doc=False,
          security=[{'oauth2_implicit': ['openid', 'itaas',
                    'profile']}],
          authorizations=authorizations)

api.add_namespace(contact)
api.add_namespace(token)
api.add_namespace(testing)
api.add_namespace(connection)