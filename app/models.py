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
    ticket_date = db.Column(db.String(10), nullable=False)
    start_from = db.Column(db.String(20), nullable=False)
    end_to = db.Column(db.String(20), nullable=False)
    train_number = db.Column(db.String(20), nullable=False)
    passengers = db.Column(db.TEXT, nullable=False)
    passenger_num = db.Column(db.Integer, nullable=False)
    success_rate = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.Integer)
    create_date = db.Column(db.TIMESTAMP(True), nullable=False)
    update_date = db.Column(db.TIMESTAMP(True), nullable=False)

    def __init__(self, ticket_id, tel_phone, idcard_num, ticket_date, start_from, end_to, train_number, passengers,
                 passenger_num,
                 success_rate, price, status):
        self.ticket_id = ticket_id
        self.tel_phone = tel_phone
        self.idcard_num = idcard_num
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

    def __repr__(self):
        return '<Ticket: {0}\n{1}\n{2}\n{3}\n{4}\n{5}\n{6}\n{7}\n{8}\n{9}\n{10}\n{11}\n{12}\n>'.format(
            self.ticket_id, self.telPhone, self.IdCard_num, self.ticket_date, self.start_from, self.end_to,
            self.train_number,
            self.passengers, self.passenger_num,
            self.success_rate, self.price, self.status, self.createDate, self.updateDate)

    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'ticket_id': self.ticket_id,
            'telPhone': self.tel_phone,
            'IdCard_num': self.idcard_num,
            'ticket_date': self.ticket_date,
            'start_from': self.start_from,
            'end_to': self.end_to,
            'train_number': self.train_number,
            'passengers': self.passengers,
            'passenger_num': self.passenger_num,
            'success_rate': self.success_rate,
            'price': self.price,
            'status': self.status,
            'createDate': self.create_date,
            'updateDate': self.update_date
        }
