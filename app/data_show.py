# coding=utf-8
from flask import Flask, request, render_template, jsonify, redirect, url_for, json
from create_app import app
from models import db, Ticket
from config import PAGE_SIZE

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


@app.route('/getargs')
def getArgs():
    page = request.args.get('Page', 1, type=int)
    search_info = request.args.get('SearchInfo', '', type=str)
    del_info = request.args.get('DelInfo', '', type=str)
    update_info = request.args.get('UpdateInfo', '', type=str)
    sort_info = request.args.get('SortInfo', '', type=str)
    add_info = request.args.get('AddInfo', '', type=str)
    print page, del_info, sort_info, update_info, search_info, add_info
    if del_info == 'none' and sort_info == 'none' and update_info == 'none' and add_info == 'none':
        print '进行查找操作'
        return redirect(url_for('search', search_info=search_info, page=page))

    if sort_info != 'none' and del_info == 'none' and update_info == 'none' and add_info == 'none':
        print '进行排序操作'
        return redirect(url_for('sort', page=page, sort_info=sort_info))

    if del_info == 'none' and sort_info == 'none' and update_info == 'none' and add_info == 'none':
        print '进行查找操作'
        return redirect(url_for('search', search_info=search_info, page=page))

    if sort_info != 'none' and del_info == 'none' and update_info == 'none' and add_info == 'none':
        print '进行排序操作'
        return redirect(url_for('sort', page=page, sort_info=sort_info))

    # if update_info != 'none':
    #     print '进行更新操作'
    #     update_event(update_info=update_info)
    #     if sort_info != 'none':
    #         print '更新操作执行完毕，按原样进行排序', sort_info
    #         return redirect(url_for('sort', page=page, sort_info=sort_info))
    #     else:
    #         print '更新操作执行完毕，按原样进行搜索', search_info
    #         return redirect(url_for('search', page=page, search_info=search_info))
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
    ticket_id, tel_phone, idcard_num = '', '', ''
    print search_info, page
    if search_info != 'none' and search_info != u'undefined':
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
        print ticket_id, tel_phone, idcard_num

    try:
        total_num = Ticket.query.filter().count()
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
    except Exception, e:
        print 'Error:', e
        result = '未找到数据'
        return render_template('back.html', result=result)

    else:
        if not paginate.pages:
            result = '未找到数据'
            result = json.dumps(result)
            return render_template('back.html', result=result)
        else:
            print '共%s页数据,当前%s页' % (paginate.pages, page)
            tickets = []
            pagination = {'total_num': total_num, 'num': num, 'total_pages': paginate.pages, 'current_page': page,
                          'per_page': PAGE_SIZE}
            tickets.append(pagination)
            object_list = paginate.items
            for i in object_list:
                ticket = {'ticket_id': i.ticket_id, 'tel_phone': i.tel_phone, 'idcard_num': i.idcard_num,
                          'ticket_date': i.ticket_date, 'start_from': i.start_from, 'end_to': i.end_to,
                          'train_number': i.train_number, 'passengers': i.passengers, 'passenger_num': i.passenger_num,
                          'success_rate': i.success_rate, 'price': i.price, 'status': i.status,
                          'create_date': i.create_date, 'update_date': i.update_date}

                tickets.append(ticket)
            return jsonify(result=tickets)  # 返回数据到ajax


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080, debug=True)
    app.run(debug=True)
