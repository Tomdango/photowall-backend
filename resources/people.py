"""
    People Flask-RESTful Resource
    Created 17/09/2019
"""
from flask import request, send_file, make_response
from flask_restful import Resource, reqparse, abort
from common.database import PeopleTable
from PIL import Image
import io
import os

PeopleDB = PeopleTable()

def check_upload(uploaded_file):
    """
    Check the uploaded image to ensure that it:
    - Is an image
    - Is a .jpg or .jpeg file
    - Is a .png that file that can be converted
    """
    if uploaded_file.filename == "":
        return False, "No image was selected", None
    if uploaded_file.content_type == "image/png":
        return True, None, True
    elif uploaded_file.content_type == "image/jpeg":
        return True, None, False
    else:
        return False, "Unknown Image File Type", None

def save_photo(image, person_id, is_png):
    """
    Saves the photo
    """
    pillow_image = Image.open(image)
    if is_png:
        pillow_image = pillow_image.convert("RGB")
    pillow_image.save("static/assets/images/{}.jpg".format(person_id), 'JPEG', quality=95)


class GetPeople(Resource):
    def get(self):
        """ Retrieves people within the SQLite database. """
        parser = reqparse.RequestParser()
        parser.add_argument("limit", type=int, help="Limit cannot be converted", default=50)
        parser.add_argument("tribe", type=str, help="Tribe cannot be converted", default=None)
        parser.add_argument("name", type=str, help="Name cannot be converted", default=None)
        args = parser.parse_args()
        results = PeopleDB.get_people(limit=args.get("limit"), tribe=args.get("tribe"), name=args.get("name"))
        return {
            "meta": {
                "args": {
                    "limit": args.get("limit"),
                    "tribe": args.get("tribe"),
                    "name": args.get("name"),
                    "num_results": len(results)
                }
            },
            "results": results
        }

class AddPerson(Resource):
    def post(self):
        """
        Uploads an image to the images directory, and
        inserts a new person into the database.
        """
        name = request.form.get("name")
        tribe = request.form.get("tribe")
        fun_fact = request.form.get("fun_fact")
        image = request.files.get("image")
        if not name or not tribe or not fun_fact or not image:
            return abort(400, message="name, tribe, fun_fact and image are all required.")

        is_valid, error, is_png = check_upload(image)
        if not is_valid:
            return abort(400, message=error)

        success, person_id = PeopleDB.add_person(name, fun_fact, tribe)
        if not success:
            return abort(500, message="Failed to add new person to DB")
        save_photo(image, person_id, is_png)
        return {
            "message": "Successfully added person.",
            "person": {
                "id": person_id,
                "name": name,
                "tribe": tribe,
                "fun_fact": fun_fact
            }
        }


class Person(Resource):
    def get(self, person_id):
        """
        Retrieves a Person from the DB
        """
        person = PeopleDB.get_person_by_id(person_id)
        if not person:
            return abort(404, message="Person Not Found")
        return person

    def delete(self, person_id):
        """
        Removes a person's image and entry from the database
        """
        person = PeopleDB.get_person_by_id(person_id)
        if not person:
            return abort(404, message="Person Not Found")
        success = PeopleDB.delete_person_by_id(person_id)
        if not success:
            return abort(500, message="Failed to remove person.")
        try:
            os.remove("static/assets/images/{}.jpg".format(person_id))
        except OSError:
            pass
        except:
            return {
                "message": "Failed to delete person."
            }, 500
        return {
            "message": "Successfully deleted person."
        }

class GetPersonPhoto(Resource):
    def get(self, person_id):
        """
        Responds with a person's image.
        """
        person = PeopleDB.get_person_by_id(person_id)
        if not person:
            return abort(404, message="Person Not Found")
        image_location = "static/assets/images/{}.jpg".format(person_id)

        if os.path.exists(image_location) and os.path.isfile(image_location):
            with open(image_location, "rb") as image_file:
                return send_file(
                    io.BytesIO(image_file.read()),
                    mimetype='image/jpeg',
                    as_attachment=False,
                    attachment_filename='%s.jpg' % person_id)
        else:
            return {
                "message": "Image for user not found."
            }, 404

class EditPerson(Resource):
    def post(self, person_id):
        """
        Edits a Person, both editing the entry in the database
        and the image if necessary.
        """
        person = PeopleDB.get_person_by_id(person_id)
        if not person:
            return abort(404, message="Person Not Found")
        name = request.form.get("name")
        tribe = request.form.get("tribe")
        fun_fact = request.form.get("fun_fact")
        image = request.files.get("image")

        if not name and not tribe and not fun_fact and not image:
            return abort(400, message="Either name, tribe, fun_fact or image are required.")
        if image:
            is_valid, error, is_png = check_upload(image)
            if not is_valid:
                return abort(400, message=error)
            imagepath = "static/assets/images/{}.jpg".format(person_id)
            if os.path.exists(imagepath):
                os.remove(imagepath)
            save_photo(image, person_id, is_png)

        # If name, tribe or fun_fact not supplied, there's no need to touch the DB
        new_person = person
        if name or tribe or fun_fact:
            success, new_person = PeopleDB.edit_person(person, name, tribe, fun_fact)
            if not success:
                return abort(400, message="Failed to edit person.")

        return {
            "message": "Successfully edited person.",
            "person": new_person
        }
