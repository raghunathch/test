""" Authentication API for SGConnect token informations """
from flask import g
from flask_restplus import Namespace, fields, marshal

from sg_datalake import DatalakeRecord

from package_as_a_service.core.decorators import DecoratedResource
import logging


dl_logger = logging.getLogger('datalake')

namespace = Namespace(
    'token', description='SGConnect token informations')

token_schema = namespace.model('Token', {
    'login_ad': fields.String(description='The Active Directory login'),
    'mail': fields.String(description='The contact email'),
    'expired': fields.Boolean(description='Is this token expired')
})


@namespace.doc(security=[{'oauth2_implicit': ['profile', 'itaas', 'openid']}])
@namespace.route('/')
class Authentication(DecoratedResource):
    """ Display your authentication informations """
    @namespace.marshal_list_with(token_schema, envelope="token")
    @namespace.doc(description='Allow you to retrieve \
                   information about your SGConnect token')
    def get(self):
        """ Your token informations """
        token_info = self.get_token_info(g.token)
        dl_logger.info(DatalakeRecord(g.correlation_id, event="response",
                                      response_http_code=200,
                                      response_message=marshal(token_info,
                                                               token_schema)))
        return token_info

    @staticmethod
    def get_token_info(token):
        """ Return informations from a given token """
        token_info = {"login_ad": token.login_ad(),
                      "mail": token.mail(),
                      "expired": token.is_expired()}
        return token_info
