import paramiko
from flask_restplus import Namespace, fields, reqparse, marshal
from package_as_a_service.core.decorators import DecoratedResource

namespace = Namespace(
    'connection', description='This will connect to server for information')

connection_schema = namespace.model('Connector', {
    'hostname': fields.String(description='First Value',
                          required=True),
    'username': fields.String(description='Second Value',
                          required=True),
    'password': fields.String(description='Sum action',
                          required=True),
    'command': fields.String(description='Sum action',
                          required=True)
})

@namespace.route('/')

class connectionclass(DecoratedResource):
    @namespace.doc(description="Doing post operation on connection")
    @namespace.expect(connection_schema, validate=True)
    @namespace.marshal_with(connection_schema, code=201)
    def post(self):
        data = self.connection_data()
        data = dict(data)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        output=[]
        try:
            ssh.connect(data['hostname'], username=data['username'], password=data['password'])
        except paramiko.SSHException:
            return "Getting the SSH Connection Error"
        else:
            stdin, stdout, stderr = ssh.exec_command(data['command'])
            stdin.close()

            for line in stdout.read().splitlines():
                output.append(line.decode("utf-8").strip())
            ssh.close()
            return output
    @staticmethod
    def connection_data():
        parser = reqparse.RequestParser()
        parser.add_argument('hostname', type=str)
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('command', type=str)
        return parser.parse_args()