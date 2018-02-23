""" Contact API for Contact Information """
from flask_restplus import Namespace, fields, reqparse, marshal
from flask import jsonify, g

from sg_datalake import DatalakeRecord

from package_as_a_service.resources.contact import Contact as ContactModel
from package_as_a_service.resources.base import db
from package_as_a_service.core.exception import PackageAsAServiceError
from package_as_a_service.core.decorators import DecoratedResource

import logging


dl_logger = logging.getLogger('datalake')


namespace = Namespace(
    'contacts', description='Operations on contacts information')

contact_schema = namespace.model('Contact', {
    'team': fields.String(description='The contact person name',
                          required=True),
    'mail': fields.String(description='The contact email',
                          required=True),
    'phone': fields.String(description='The contact telephone number',
                           required=True),
    'impulse_group': fields.String(description='The impulse group \
                                                of your team'),
    'jive': fields.String(description='The URL of your jive'),
    'doc_url': fields.String(description='The URL documention of yours APIs',
                             required=True)
})


@namespace.errorhandler(PackageAsAServiceError)
def handle_invalid_usage(error):
    """ Catch and forward to app.errorhandler PackageAsAServiceError exceptions """
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@namespace.doc(security=[{'oauth2_implicit': ['profile', 'itaas', 'openid']}])
@namespace.route('/')
class ContactList(DecoratedResource):
    """Shows a list of all contacts, and lets you POST to add new contact"""

    @staticmethod
    @namespace.marshal_list_with(contact_schema, envelope='contacts')
    @namespace.doc(description='This is a package_as_a_service API. ' +
                   'It returns all our team contacts')
    def get():
        """ All our team contacts list """
        contacts_list = ContactModel.query.all()
        dl_logger.info(
            DatalakeRecord(
                g.correlation_id,
                event="response",
                response_http_code=200,
                response_message=marshal(contacts_list,
                                         contact_schema,
                                         envelope='contacts')))
        return contacts_list

    @namespace.doc('create_contact', description='It\'s an example to demonstrate \
                    how to create a new package_as_a_service contact list')
    @namespace.expect(contact_schema, validate=True)
    @namespace.marshal_with(contact_schema, code=201)
    def post(self):
        """Add a new package_as_a_service contact list"""
        data = self.parse_contact_data()
        contact = ContactModel(data)
        db.session.add(contact)
        db.session.commit()
        dl_logger.info(DatalakeRecord(
                       g.correlation_id, event="response",
                       response_http_code=201,
                       response_message=marshal(contact, contact_schema)))
        return contact, 201

    @staticmethod
    def parse_contact_data():
        """ Parse arguments """
        parser = reqparse.RequestParser()
        parser.add_argument('team', type=str)
        parser.add_argument('impulse_group', type=str)
        parser.add_argument('mail', type=str)
        parser.add_argument('phone', type=str)
        parser.add_argument('jive', type=str)
        parser.add_argument('doc_url', type=str)
        return parser.parse_args()
