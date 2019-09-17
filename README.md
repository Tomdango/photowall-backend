# Photowall Backend Example

> Made for NHS Digital Academy Induction Hackathon 2019

## Running the Application

This application was built with Python 3.7.4, but should work with all versions of Python greater than 3.4.

### Clone the Repository

```bash
git clone https://github.com/Tomdango/photowall-backend.git photowall-backend
cd photowall-backend
```

### Create a virtual environment

```bash
python3 -m virtualenv venv
```

### Activate the virtual environment

```bash
# Windows
.\venv\Scripts\activate

# Linux
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the application

```bash
python main.py
```

## Endpoints

### `GET /people`

Retrieves a list of people from the database. Takes the following parameters:

| Parameter | Effect                                                                                                    | Default Value |
| --------- | --------------------------------------------------------------------------------------------------------- | ------------- |
| `limit`   | Limits the number of people returned. Set to `-1` to disable the limit.                                   | 50            |
| `tribe`   | Filters the list of people per tribe. It uses a loose match, so `tribe=spine` would match to `SpineCore`. | None          |
| `name`    | Filters the list of people by name. Also uses a loose match.                                              | None          |

#### Example Response

```json
{
    "meta": {
        "args": {
            "limit": 50,
            "tribe": null,
            "name": null,
            "num_results": 1
        }
    },
    "results": [
        {
            "id": "6FC9DIuVPW",
            "name": "Joe Bloggs",
            "fun_fact": "I can play the piano!",
            "tribe": "Spine Core"
        }
    ]
}
```

### `POST /people/add`

Adds a new person. Requires a POST with `form-data`, and with the following fields:

| Name       | Type           | Description           |
| ---------- | -------------- | --------------------- |
| `name`     | String         | The Person's Name     |
| `tribe`    | String         | The Person's Tribe    |
| `fun_fact` | String         | The Person's Fun Fact |
| `image`    | Uploaded Image | A JPEG or PNG image.  |

#### Example Response

```json
{
    "message": "Successfully added person.",
    "person": {
        "id": "6FC9DIuVPW",
        "name": "Joe Bloggs",
        "tribe": "Spine Core",
        "fun_fact": "I can play the piano!"
    }
}
```

### `GET /people/:id`

Retrieves a single person.

```json
{
    "id": "6FC9DIuVPW",
    "name": "Joe Bloggs",
    "fun_fact": "I can play the piano!",
    "tribe": "Spine Core"
}
```

### `GET /people/:id.jpg`

Returns the user's photo.

### `DELETE /people/:id`

Removes a user.

#### Example Response

```json
{
    "message": "Successfully deleted person."
}
```

### `POST /people/:id/edit`

Takes the exact same parameters as `/people/add`.

#### Example Response

```json
{
    "message": "Successfully edited person.",
    "person": {
        "id": "hk38gHAPN8",
        "name": "Joe Bloggy",
        "tribe": "Spine Core",
        "fun_fact": "I can't play the piano!"
    }
}
```

-------------------------------

##### Thomas Judd-Cooper. 2019
