import os
import zipfile

from create_app import app

ZIP_PATH = app.root_path + "\\static\\download\\"
TMP_PATH = app.root_path + "\\static\\temp\\"
ZIP_FILE_NAME = "ticket.zip"


def create_file(file_content, file_path):
    file_path = file_path.decode('utf-8')
    if os.path.exists(file_path):
        os.remove(file_path)

    file1 = open(file_path, "ab")
    file1.write(file_content)
    file1.close()


def process_file_content(s):
    """remove the leading unicode designator from a string"""
    s2 = s.replace("\'", "\"")
    s2 = s2.replace("u'", "'")
    s2 = s2.replace('u"', '"')
    return s2.encode("utf-8")


def delete_path():
    del_file(ZIP_PATH)
    del_file(TMP_PATH)


def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)


def byteify(input_content):
    if isinstance(input_content, dict):
        return {byteify(key): byteify(value) for key, value in input_content.iteritems()}
    elif isinstance(input_content, list):
        return [byteify(element) for element in input_content]
    elif isinstance(input_content, unicode):
        return input_content.encode('utf-8')
    else:
        return input_content


def zip_dir():
    zip_file_path = ZIP_PATH + ZIP_FILE_NAME
    if os.path.exists(zip_file_path):
        os.remove(zip_file_path)
    zip1 = zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(TMP_PATH):
        fpath = path.replace(TMP_PATH, '')
        for filename in filenames:
            zip1.write(os.path.join(path, filename), os.path.join(fpath, filename))
    zip1.close()


def generate_xml(current_passenger_num, ticket_info_node, passenger_info_node):
    file_name = str(current_passenger_num / 10)
    xml_header = "<?xml version=\"1.0\" encoding=\"utf-8\" ?>"
    ticket_info = xml_header + "<tickets>" + ticket_info_node + "</tickets>"
    passenger_info = xml_header + "<passengers>" + passenger_info_node + "</passengers>"

    ticket1_name = TMP_PATH + "ticket_" + file_name + ".xml"
    create_file(ticket_info, ticket1_name)

    passenger2_name = TMP_PATH + "passenger_" + file_name + ".xml"
    create_file(passenger_info, passenger2_name)
