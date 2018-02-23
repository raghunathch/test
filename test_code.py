import subprocess
from flask_restplus import Namespace, fields, reqparse, marshal
from package_as_a_service.core.decorators import DecoratedResource
from package_as_a_service.apis.PackageLogic import CalculatorSample

namespace = Namespace(
    'testing', description='Operations on contacts information')

calculator_schema = namespace.model('Calculator', {
    'input1': fields.Integer(description='First Value',
                          required=True),
    'input2': fields.Integer(description='Second Value',
                          required=True),
    'sum': fields.Integer(description='Sum action')
})

@namespace.route('/')
class HelloWorld(DecoratedResource):
  def get(self):
    object1 = CalculatorSample()
    result = object1.performmaths(1,2,3)
    text = "Unix team learning coding on BeAPI Oh!"
    #result1 = os.system("dir c:\\")
    #proc = subprocess.Popen('dir c:\\', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    #proc = subprocess.Popen(["echo", "hello world"], stdout=subprocess.PIPE)
    #stdout, stderr = proc.communicate()
    return text #str(stdout)


  @namespace.doc(description="Doing post opetation on calculator")
  @namespace.expect(calculator_schema, validate=True)
  @namespace.marshal_with(calculator_schema, code=201)
  def post(self):
      data = self.calculator_data()
      data=dict(data)
      sum = str(int(data['input1']) + int(data['input2']))
      d={'input1':data['input1'],'input2':data['input2'],'sum':sum}
      return d

  @staticmethod
  def calculator_data():
     parser = reqparse.RequestParser()
     parser.add_argument('input1', type=int)
     parser.add_argument('input2', type=int)
     return parser.parse_args()

