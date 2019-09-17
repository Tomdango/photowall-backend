from flask import Flask
from flask_restful import Resource, Api
from resources import GetPeople, AddPerson, Person, GetPersonPhoto, EditPerson

app = Flask(__name__)
api = Api(app)


api.add_resource(GetPeople, "/people/")
api.add_resource(AddPerson, "/people/add", "/people/add/")
api.add_resource(Person, "/people/<person_id>", "/people/<person_id>/")
api.add_resource(GetPersonPhoto, "/people/<person_id>.jpg")
api.add_resource(EditPerson, "/people/<person_id>/edit", "/people/<person_id>/edit/")


if __name__ == "__main__":
    app.run(debug=True)




