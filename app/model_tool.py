import random

from app.config import SINGLE_PRICE
from app.models import Ticket


def get_tid():
    flag = True
    tid = ""
    while flag:
        tid = create_ticket_id()
        num = Ticket.query.filter(
            Ticket.ticket_id == tid
        ).count()
        if num <= 0:
            flag = False
    return tid


def create_ticket_id():
    t_id = ""
    for i in range(0, 2):
        s = random.randint(65, 90)
        t_id += chr(s)
    for i in range(0, 2):
        s = random.randint(0, 9)
        t_id += str(s)
    return t_id


def get_price(passenger_num, percent):
    if str(percent) == "0":
        return 0

    if str(percent) == "25":
        return SINGLE_PRICE * int(passenger_num)

    if str(percent) == "50":
        return SINGLE_PRICE * int(passenger_num)

    if str(percent) == "75":
        return SINGLE_PRICE * int(passenger_num)

    if str(percent) == "96":
        return SINGLE_PRICE * int(passenger_num)


def get_from_to(start_from, end_to):
    temp = start_from.split("][")[0].replace("[", "") + "--" + end_to.split("][")[0].replace("[", "")
    return temp


def get_ticket_json2(ticket):
    ticket = {'ticket_id': ticket.ticket_id, 'tel_phone': ticket.tel_phone, 'idcard_num': ticket.idcard_num,
              'ticket_date': ticket.ticket_date, 'start_from': ticket.start_from, 'end_to': ticket.end_to,
              'train_number': ticket.train_number, 'passengers': ticket.passengers,
              'passenger_num': ticket.passenger_num,
              'success_rate': ticket.success_rate, 'price': ticket.price,
              'status': ticket.status,
              'create_date': ticket.create_date,
              'update_date': ticket.update_date}
    return ticket
