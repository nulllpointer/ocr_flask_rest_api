import sys

from flask import Flask, request
from flask import Flask, session
import my_utils as my_utils
import os
import services

PATH = sys.path
print(PATH)
img_save_path = os.getcwd()+'/assets'
pdf_save_path = os.getcwd() + '/assets'
assets_path = os.getcwd() + '/assets'

app = Flask(__name__)
# app.secret_key = "hite"


@app.route("/", methods=['GET','POST'])
def index():
    return "Congrats, you reached nulllpointer's root!!!!"


@app.route('/api/tesseract/image/translate', methods=['POST'])
def image_translate():
    if request.method == 'POST':  # this block is only entered when the form is submitted

        required_keys = ['src', 'dest', 'framework', 'username']
        image_file = 'image1'

        form_values, image_file_list = my_utils.get_request_payload(request, required_keys, image_file)

        return services.process_image_to_translated_text(form_values, image_file_list, assets_path=assets_path)


@app.route('/api/tesseract/image/text', methods=['POST'])
def image_text():
    if request.method == 'POST':  # this block is only entered when the form is submitted

        required_keys = ['src', 'framework', 'username']
        image_file = 'image1'

        form_values, image_file_list = my_utils.get_request_payload(request, required_keys, image_file)

        return services.process_image_to_text(form_values, image_file_list, assets_path=assets_path)


@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404


if __name__ == '__main__':
    # create_app()
    # app.run(host='0.0.0.0', port=5001)

    app.run(host='0.0.0.0', debug=True)
