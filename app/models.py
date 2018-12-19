# coding=utf-8
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from create_app import app

db = SQLAlchemy(app)


class Ticket(db.Model):
    __tablename__ = 'ticketinfo'

    # 需要保证名字的格式, telPhone这样不可以，使用 tel_phone.不包含大写字符
    ticket_id = db.Column(db.String(20), primary_key=True, nullable=False)
    tel_phone = db.Column(db.String(11), nullable=False)
    idcard_num = db.Column(db.String(18), nullable=False)
    ticket_date = db.Column(db.TEXT, nullable=False)  # 存放多个
    start_from = db.Column(db.TEXT, nullable=False)  # 存放多个
    end_to = db.Column(db.TEXT, nullable=False)  # 存放多个
    train_number = db.Column(db.TEXT, nullable=False)  # 存放多个
    passengers = db.Column(db.TEXT, nullable=False)  # 存放多个
    passenger_num = db.Column(db.Integer, nullable=False)
    success_rate = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.Integer)
    create_date = db.Column(db.TIMESTAMP(True), nullable=False)
    update_date = db.Column(db.TIMESTAMP(True), nullable=False)

    # add new column
    seat_type = db.Column(db.TEXT, nullable=True)  # 存放多个
    is_student = db.Column(db.Integer, nullable=True)
    from_to = db.Column(db.TEXT, nullable=True)  # 存放单个

    def __init__(self, ticket_id, tel_phone, idcard_num, ticket_date, start_from, end_to, train_number, passengers,
                 passenger_num,
                 success_rate, price, status, seat_type, is_student, from_to):
        self.ticket_id = ticket_id
        self.tel_phone = tel_phone
        self.idcard_num = "" if idcard_num == "" else idcard_num
        self.ticket_date = ticket_date
        self.start_from = start_from
        self.end_to = end_to
        self.train_number = train_number
        self.passengers = passengers
        self.passenger_num = passenger_num
        self.success_rate = success_rate
        self.price = price
        self.status = status
        self.create_date = datetime.now()
        self.update_date = datetime.now()

        self.seat_type = seat_type
        self.is_student = is_student
        self.from_to = from_to

    def __repr__(self):
        return '<Ticket: {0}\n{1}\n{2}\n{3}\n{4}\n{5}\n{6}\n{7}\n{8}\n{9}\n{10}\n{11}\n{12}\n{13}\n{14}\n{15}>'.format(
            self.ticket_id, self.tel_phone, self.idcard_num, self.ticket_date, self.start_from, self.end_to,
            self.train_number,
            self.passengers, self.passenger_num,
            self.from_to, self.seat_type, self.is_student,
            self.success_rate, self.price, self.status, self.create_date, self.update_date)

    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'ticket_id': self.ticket_id,
            'tel_phone': self.tel_phone,
            'idcard_num': self.idcard_num,
            'ticket_date': self.ticket_date,
            'start_from': self.start_from,
            'end_to': self.end_to,
            'train_number': self.train_number,
            'passengers': self.passengers,
            'passenger_num': self.passenger_num,
            'from_to': self.from_to,
            'seat_type': self.seat_type,
            'is_student': self.is_student,
            'success_rate': self.success_rate,
            'price': self.price,
            'status': self.status,
            'createDate': self.create_date,
            'updateDate': self.update_date
        }
