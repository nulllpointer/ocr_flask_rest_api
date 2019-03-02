import os

from fpdf import FPDF
import pytesseract
from PIL import Image
from flask import Session
from googletrans import Translator
import json


# def get_request_payload(request, required_keys, image_file):
#     request_form = {}
#     request_image_file = []
#     form_attributes = []
#
#     for f in image_file:
#         tmp = request.files[f]
#         request_image_file.append(tmp)
#
#         # request_image_file.append(request.files[f])
#
#     form_attributes.append(request.form)
#
#     attribute_list = list(map(lambda form_attributes: dict(form_attributes), form_attributes))[0]
#
#     for k in required_keys:
#         if dict(attribute_list)[k]:
#             request_form.update(dict(attribute_list))
#     return request_form, request_image_file


def get_request_payload(request, required_keys, image_file):
    request_form = {}
    form_attributes = []

    # TODO handle for list of images
    # print(request.files.getfiles())

    file = request.files[image_file]

    form_attributes.append(request.form)

    attribute_list = list(map(lambda form_attributes: dict(form_attributes), form_attributes))[0]

    for k in required_keys:
        if dict(attribute_list)[k]:
            request_form.update(dict(attribute_list))

    return request_form, file


def image_to_text(img, lang=None):
    image_text = pytesseract.image_to_string(img, lang=lang)
    output = image_text if image_text else "could not convert"
    return output


# //TODO
def image_to_pdf(img):
    # get a searchable PDF
    pdf = pytesseract.image_to_pdf_or_hocr(img, extension='pdf')
    output = pdf if pdf else "could not convert"
    return output


def translate_text(text, dest_lang):
    translator = Translator()
    translated_text = translator.translate(text, dest=dest_lang)
    if translated_text:
        return translated_text.text
    else:
        return UnicodeTranslateError


def load_image(files, img_save_path):
    img = Image.open(files, 'r')
    filename = os.path.join(img_save_path, 'image.png')
    # img.save(filename, img.format)
    return img


def get_image_file(img_save_path):
    filename = os.path.join(img_save_path, 'image.png')

    # a = Image.open(filename, 'r')
    return filename


def text_to_pdf(text_input, pdf_save_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, text_input)
    pdf.output(os.path.join(pdf_save_path, 'output.pdf'), 'F')


def multipart_response_success(file, form_values, s):
    my_output = {
        "status_code": "success",
        "session_id": s['sid'],
        "user": s['username'],
        'file': file,
        'data': form_values,

    }

    # for json use    # json.loads(json.dumps(my_output))

    return '{}'.format(my_output)


def multipart_response_failure(form_values):
    my_output = {
        "status_code": "failure",
        'data': form_values

    }

    # for json use    # json.loads(json.dumps(my_output))

    return '{}'.format(my_output)


def text_to_file(text, file_save_path, filename):
    if text:
        file = open(os.path.join(file_save_path, filename), 'a+', encoding='UTF-8')
        file.write(
            '\n' + '--------------------------------------------*******start******------------------------------------------------------' + '\n')

        file.write(text + '\n')
        file.write(
            '\n' + '---------------------------------------------------end------------------------------------------------------------' + '\n')

        if file:
            return file
    else:
        "could not find text to write to file"


def text_to_file_resource(text, file_save_path, filename):
    if text:
        file = open(os.path.join(file_save_path, filename), 'a+', encoding='UTF-8')
        file.write(
            '\n' + '--------------------------------------------*******start******------------------------------------------------------' + '\n')

        file.write(text + '\n')
        file.write(
            '\n' + '---------------------------------------------------end------------------------------------------------------------' + '\n')

        if True:
            filepath = os.path.join(file_save_path, filename)
            return filepath

    else:
        "could not find text to write to file"


def json_response_success(file, form_values,s):
    my_output = {
        "status": "success",
        "session_id":str(s['sid']),
        "user":s['username'],
        'file': file.name,
        'data': form_values,

    }
    return json.dumps(my_output,ensure_ascii=False, sort_keys=True)

def json_response_failure(form_values,sess):
    my_output = {
        "status": "failure",
        "session_id":sess['sid'],
        "user":sess['username'],
        'data': form_values,

    }
    return json.dumps(my_output,ensure_ascii=False, sort_keys=True)



