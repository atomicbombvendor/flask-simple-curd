# coding=utf-8

from flask import Flask, request, render_template, jsonify, redirect, url_for, json
from create_app import app
from models import db, Ticket
from config import PAGE_SIZE, TABLE_NAME


@app.route('/')
@app.route('/scan/all/', methods=['GET', 'POST'])
def scan_all():
    if request.method == 'GET':
        return render_template('base.html')


"""
获取ajax传过来的参数,根据参数状态进行不同的操作
共有四种操作:搜索数据（直接显示数据等同于搜索关键字全为空），排序，删除数据，更新数据

1.进行搜索(全局搜索)时不需要关心sort,del,update信息,每次进行搜索操作,前端需要把sort_info,del_info,update_info设为'none'
if sort_info='none' and del_info='none' and update_info='none':
    跳转到搜索(search_info)

2.进行排序(全局排序)时不需要关心search,del,update信息,每次进行排序操作,前端需要把search_info,del_info,update_info设为'none'
if sort_info!='none':
    跳转到排序(sort_info)

3.如果是在排序的基础上进行更新操作,执行更新操作后,需要跳转到排序操作;如果是在搜索的基础上进行更新操作,执行更新操作后,需要跳转到搜索操作
if update_info!='none'：
    if sort_info!='none'：
        跳转到更新(update_info, sort_info)
        执行更新操作后跳转到排序(sort_info)
    if sort_info=='none':
        跳转到更新(update_info, search_info)
        执行更新操作后跳转到搜索(search_info)

4.del操作和update操作类似
"""


@app.route('/getargs/')
def getArgs():
    page = request.args.get('Page', 1, type=int)
    search_info = request.args.get('SearchInfo', '', type=str)
    del_info = request.args.get('DelInfo', '', type=str)
    update_info = request.args.get('UpdateInfo', '', type=str)
    sort_info = request.args.get('SortInfo', '', type=str)
    add_info = request.args.get('AddInfo', '', type=str)
    modify_status_value = request.args.get('modify_status_value', '', type=str)
    modify_status_info = request.args.get('modify_status_info', '', type=str)

    print "getargs input>> "
    print page, del_info, sort_info, update_info, search_info, add_info, modify_status_value, modify_status_info
    if modify_status_info == 'none' and sort_info == 'none' and update_info == 'none' and add_info == 'none':
        print '进行查找操作'
        return redirect(url_for('search', search_info=search_info, page=page))

    if sort_info != 'none' and modify_status_info == 'none' and update_info == 'none' and add_info == 'none':
        print '进行排序操作'
        return redirect(url_for('sort', page=page, sort_info=sort_info))

    if modify_status_info != 'none' and modify_status_value is not None:
        print '进行更新操作'
        batch_update_event(update_info=modify_status_info, update_status_value=modify_status_value)
        if sort_info != 'none':
            print '更新操作执行完毕，按原样进行排序', sort_info
            return redirect(url_for('sort', page=page, sort_info=sort_info))
        else:
            print '更新操作执行完毕，按原样进行搜索', search_info
            return redirect(url_for('search', page=page, search_info=search_info))
    #
    # if del_info != 'none':
    #     print '进行删除操作'
    #     del_event(del_info=del_info)
    #     if sort_info != 'none':
    #         print '删除操作执行完毕，按原样进行排序', sort_info
    #         return redirect(url_for('sort', page=page, sort_info=sort_info))
    #     else:
    #         print '删除操作执行完毕，按原样进行搜索', search_info
    #         return redirect(url_for('search', page=page, search_info=search_info))
    #
    # if add_info != 'none':
    #     print '进行添加操作'
    #     add_event(add_info=add_info)
    #     if sort_info != 'none':
    #         print '添加操作执行完毕，按原样进行排序', sort_info
    #         return redirect(url_for('sort', page=page, sort_info=sort_info))
    #     else:
    #         print '添加操作执行完毕，按原样进行搜索', search_info
    #         return redirect(url_for('search', page=page, search_info=search_info))


@app.route('/search/<search_info>/', methods=['GET', 'POST'])
@app.route('/search/<search_info>/<int:page>', methods=['GET', 'POST'])
def search(search_info='', page=1):
    ticket_id, tel_phone, idcard_num, status_t = '', '', '', None
    print search_info, page
    if search_info != 'none':
        search_info_t = []
        for x in search_info.split('&'):
            if x == 'undefined':
                search_info_t.append('')
            else:
                search_info_t.append(x)

        search_info = search_info_t

        # search_info = ['' if x == 'undefined' else x for x in search_info.split('&')]
        print search_info
        ticket_id = search_info[0]
        tel_phone = search_info[1]
        idcard_num = search_info[2]
        status_t = "1" if search_info[3] is None else search_info[3]
        print ticket_id, tel_phone, idcard_num

    try:
        total_num = Ticket.query.filter().count()
        status_t = "1" if status_t is None else status_t
        num, paginate = get_search_data(ticket_id, tel_phone, idcard_num, page, status_t)

    except Exception, e:
        print 'Error:', e
        result = 'error:未找到数据'
        # return render_template('back.html', result=result)
        return jsonify(result=result)

    else:
        if not paginate.pages:
            result = 'error:未找到数据'
            # result = json.dumps(result)
            # return render_template('back.html', result=result)
            return jsonify(result=result)
        else:
            print '共%s页数据,当前%s页' % (paginate.pages, page)
            tickets = []
            pagination = {'total_num': total_num, 'num': num, 'total_pages': paginate.pages, 'current_page': page,
                          'per_page': PAGE_SIZE}
            tickets.append(pagination)
            object_list = paginate.items
            for i in object_list:
                tickets.append(get_ticket(i))
            return jsonify(result=tickets)  # 返回数据到ajax


def get_search_data(ticket_id, tel_phone, idcard_num, page, status_t):
    if str(status_t) == '0' or status_t is None:
        num = Ticket.query.filter(
            Ticket.ticket_id.like('%' + ticket_id + '%'),
            Ticket.tel_phone.like('%' + tel_phone + '%'),
            Ticket.idcard_num.like('%' + idcard_num + '%')
        ).count()

        paginate = Ticket.query.filter(
            Ticket.ticket_id.like('%' + ticket_id + '%'),
            Ticket.tel_phone.like('%' + tel_phone + '%'),
            Ticket.idcard_num.like('%' + idcard_num + '%')
        ).order_by(Ticket.update_date.asc()).paginate(page, PAGE_SIZE, False)
    else:
        num = Ticket.query.filter(
            Ticket.ticket_id.like('%' + ticket_id + '%'),
            Ticket.tel_phone.like('%' + tel_phone + '%'),
            Ticket.idcard_num.like('%' + idcard_num + '%'),
            Ticket.status == status_t
        ).count()

        paginate = Ticket.query.filter(
            Ticket.ticket_id.like('%' + ticket_id + '%'),
            Ticket.tel_phone.like('%' + tel_phone + '%'),
            Ticket.idcard_num.like('%' + idcard_num + '%'),
            Ticket.status == status_t
        ).order_by(Ticket.update_date.asc()).paginate(page, PAGE_SIZE, False)

    return num, paginate


@app.route('/sort/<sort_info>/<int:page>', methods=['GET', 'POST'])
def sort(sort_info='', page=1):
    print sort_info, page
    sort_info = sort_info.split('&')
    sort_info = ['' if x == 'undefined' else x for x in sort_info]
    keyword = sort_info[0]
    sort = sort_info[1]
    print page, keyword, sort
    print getattr(getattr(Ticket, keyword), sort)()
    total_num = Ticket.query.filter().count()
    '''根据变量来调用类对应的属性和方法，这里需要用到python的自省和反射,getattr(obj, attr)将返回obj中名为attr的属性的值'''
    paginate = Ticket.query.filter().order_by(
        getattr(getattr(Ticket, keyword), sort)()).paginate(page, PAGE_SIZE, False)

    tickets = []
    pagination = {'total_num': total_num, 'num': total_num, 'total_pages': paginate.pages, 'current_page': page}
    tickets.append(pagination)
    object_list = paginate.items
    for i in object_list:
        tickets.append(get_ticket(i))
    return jsonify(result=tickets)


@app.route('/update/<update_info>', methods=['GET', 'POST'])
def update_event(update_info='', update_status_value=''):
    print update_info
    update_info = ['' if x == 'undefined' else x for x in update_info.split('&')]
    print update_info
    event_id = update_info[0]
    keyword = update_info[1]
    value = update_info[2]
    print event_id, keyword, value
    try:
        db.session.execute('update %s set %s="%s" where ID=%s' % (TABLE_NAME, keyword, value, event_id))
        p = Ticket.query.get(event_id)
        # getattr(p, keyword) = value
        # print p.ExpoName
    except Exception, e:
        print 'Error:', e
        result = u'修改失败'
        print result
        return
    else:
        db.session.commit()
        print '修改ID为%s的%s的值为%s' % (event_id, keyword, value)
        return


@app.route('/update/<update_info>/<update_status_value>', methods=['GET', 'POST'])
def batch_update_event(update_info='', update_status_value=1):
    ticket_ids = update_info.split('&')
    key_word = 'status'
    print ticket_ids
    for ticket_id in ticket_ids:
        try:
            print ticket_id
            print '准备更新ID为%s的数据' % ticket_id
            db.session.execute(
                'update %s set %s="%s" where ticket_id="%s"' % (TABLE_NAME, key_word, update_status_value, ticket_id))
        except Exception, e:
            print 'Error:', e
            result = u'修改失败'
            print result
        else:
            db.session.commit()
            print '修改ID为%s的%s的值为%s' % (ticket_id, key_word, update_status_value)
    return


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


def translate_status(status):
    if str(status) == '0':
        return '没有状态'

    if str(status) == '1':
        return '未提交'

    if str(status) == '2':
        return '已提交'

    if str(status) == '3':
        return '已完成'


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080, debug=True)
    app.run(debug=True)
