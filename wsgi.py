from flask import Flask
from flask_restful import Resource, Api, reqparse, abort

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)

PERSONS = {
        '1': { 'name': 'Duncan' },
        }

def abort_if_not_exists(id, hash, caller):
    if id not in hash:
        abort(404, message="Id %s does not exist in %s" % (id, caller))

class Person(Resource):
    def get(self, person_id):
        print person_id
        abort_if_not_exists(person_id, PERSONS, 'persons')
        return PERSONS[person_id]
    def put(self, person_id):
        abort_if_not_exists(person_id, PERSONS, 'persons')
        args = parser.parse_args()
        person = { 'name': args['name'] }
        PERSONS[person_id] = person
        return person, 201

class PersonList(Resource):
    def get(self):
        return PERSONS
    def post(self):
        args = parser.parse_args()
        person_id = int(max(PERSONS.keys())) + 1
        PERSONS[person_id] = {'name': args['name']}
        return PERSONS[person_id], 201

api.add_resource(PersonList, '/persons')
api.add_resource(Person, '/persons/<person_id>')

if __name__ == '__main__':
    app.run(debug=True)

