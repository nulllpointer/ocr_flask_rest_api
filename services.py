import my_utils
import os
import urllib.request
import base64, M2Crypto
import sys



def process_image_to_translated_text(form_values, image_file, assets_path):
    sess = start_session(form_values['username'])

    dest_lang_for_translate = form_values['dest'] if form_values['dest'] else None
    src_lang_ocr = form_values['src'] if form_values['src'] else None

    ocr_text_result = my_utils.image_to_text(my_utils.load_image(image_file, assets_path),
                                             lang=src_lang_ocr)
    result = my_utils.translate_text(ocr_text_result, dest_lang_for_translate[:2])

    if result == None or "could not convert" in result:
        return my_utils.json_response_failure(form_values, sess)
    else:
        file = my_utils.text_to_file(result, assets_path,
                                     filename="{}_output.txt".format(sess['sid']))
        return my_utils.json_response_success(file, form_values, sess)


def process_image_to_text(form_values, image_file, assets_path):
    """provide src language else it will change to auto eng"""

    sess = start_session(form_values['username'])



    src_lang_ocr = form_values['src'] if form_values['src'] else None

    ocr_text_result = my_utils.image_to_text(my_utils.load_image(image_file, assets_path),
                                             lang=src_lang_ocr)

    if ocr_text_result == None or "could not convert" in ocr_text_result:
        return my_utils.json_response_failure(form_values, sess)
    else:
        file = my_utils.text_to_file(ocr_text_result, assets_path,
                                     filename="{}_output.txt".format(sess['sid']))
        return my_utils.json_response_success(file, form_values, sess)


# /TODO


def process_bulk_image_to_translated_text(form_values, image_file_list):
    dest_lang = form_values['dest'] if form_values['dest'] else None
    src_lang = form_values['src'] if form_values['src'] else None

    for img in image_file_list:
        try:
            ocr_text_result = my_utils.image_to_text(my_utils.load_image(img, assets_path),
                                                     lang=src_lang)
            result = my_utils.translate_text(ocr_text_result, dest_lang)
            return result
        except:
            return None


def start_session(username):
    def generate_session_id(num_bytes=2):
        return base64.b64encode(M2Crypto.m2.rand_bytes(num_bytes))

    session = {'sid': generate_session_id(), 'username': username}

    return session
