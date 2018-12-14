# coding=utf-8
from create_app import app

ZIP_PATH = app.root_path + "\\static\\download\\"
TMP_PATH = app.root_path + "\\static\\temp\\"
ZIP_FILE_NAME = "ticket.zip"


def get_ticket(ticket_obj):
    ticket = {'ticket_id': ticket_obj.ticket_id, 'tel_phone': ticket_obj.tel_phone, 'idcard_num': ticket_obj.idcard_num,
              'ticket_date': ticket_obj.ticket_date, 'start_from': ticket_obj.start_from, 'end_to': ticket_obj.end_to,
              'train_number': ticket_obj.train_number, 'passengers': ticket_obj.passengers,
              'passenger_num': ticket_obj.passenger_num,
              'success_rate': ticket_obj.success_rate, 'price': ticket_obj.price,
              'status': translate_status(ticket_obj.status),
              'create_date': ticket_obj.create_date.strftime("%Y-%m-%d %H:%M:%S"),
              'update_date': ticket_obj.update_date.strftime("%Y-%m-%d %H:%M:%S")}
    return ticket


# 生成xml内容
def get_xml_ticket(ticket_date, start_from, end_to, train_number, name, id_card_num):
    ticket_info_node, passenger_info_node = '', ''
    ticket_date_node = "<date>" + ticket_date + "</date>"
    start_from_node = "<start>" + start_from + "</start>"
    end_to_node = "<end_to>" + end_to + "</end_to>"
    train_number_node = "<train_number>" + train_number + "</train_number>"
    name_node = "<name>" + name + "</name>"
    id_card_num_node = "<id_card_num>" + id_card_num + "</id_card_num>"

    ticket_info_node = "<ticket>" + ticket_info_node + ticket_date_node + start_from_node + end_to_node + train_number_node + name_node + id_card_num_node + "</ticket>"
    passenger_info_node = "<passenger>" + passenger_info_node + name_node + id_card_num_node + "</passenger>"

    return ticket_info_node, passenger_info_node


def translate_status(status):
    if str(status) == '0':
        return '没有状态'

    if str(status) == '1':
        return '未提交'

    if str(status) == '2':
        return '已提交'

    if str(status) == '3':
        return '已完成'
