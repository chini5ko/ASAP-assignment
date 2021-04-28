from flask import Flask, render_template, request
import uuid
app = Flask(__name__)

# member ids database
members_id_db = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/member_id', methods=['POST'])
def member_id():

    # check if there is first_name....
    json_data = request.get_json()

    if "first_name" not in json_data:
        error = {"message": "the first_name field is missing"}
        return error, 400

    if "last_name" not in json_data:
        error = {"message": "the last_name is missing"}
        return error, 400

    if "dob" not in json_data:
        error = {"message": "the dob (date of birth) field is missing"}
        return error, 400

    if "country" not in json_data:
        error = {"message": "the country field is missing"}
        return error, 400

    # generate unique id
    is_unique = False
    while not is_unique:
        id_val = uuid.uuid4().int & (1 << 32)-1
        id = str(id_val)
        if id not in members_id_db:
            is_unique = True

    # save it in the memeber object
    members_id_db[id] = json_data
    members_id_db[id]["member_id"] = id

    return members_id_db[id]


@app.route('/member_id/validate',  methods=['GET', 'POST'])
def get_member_id():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        member_id = request.form['member_id']
        if member_id in members_id_db:
            return "The " + member_id + " is valid"
        else:
            message = "Sorry, the " + member_id + " is not registered in ASAP database"
            message += "<br>Please contac ASAP. Email: info@asylumadvocacy.org "
            return message


if __name__ == '__main__':
    app.run(debug=True)
