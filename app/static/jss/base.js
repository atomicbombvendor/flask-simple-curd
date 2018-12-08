$(function () {
    //页面加载时调用show()获取数据，此时搜索关键字全为空，所以后台返回全部数据
    show();

    function show(page) {
        $.ajax({
            type: 'GET',
            url: '/getargs',
            data: {
                Page: page,
                SearchInfo: $("#search_info").val(),
                SortInfo: $("#sort_info").val(),
                UpdateInfo: $("#update_info").val(),
                modify_status_info: $("#modify_status_info").val(),
                modify_status_value: $("#modify_status_value").val(),
                DelInfo: $("#del_info").val(),
                AddInfo: $("#add_info").val(),
                PageSize: $("#adjust_page_size").val()
            },
            success: function (data) {

                if (typeof data.result == "string" && data.result.search("error") !== -1) {
                    alert(data.result.replace("error:", ""));
                    return;
                }

                tickets = data.result.splice(1);     //result的第一项是页数信息，从第二项开始才是ticket数据
                pagination = data.result[0];
                total_num = pagination.total_num;
                num = pagination.num;
                total_pages = pagination.total_pages;
                current_page = pagination.current_page;

                $("#current_page").val(current_page);
                var $table = $('#ticket-info');
                $table.empty();
                createTable(tickets);    //创建表格
                createPage(total_pages, current_page);  //创建分页
                showNum(total_num, num);
                showColumn();
                restore_value();
            },
            error: function (data) {
                alert('error');
                alert(data);

            }
        });
    }

    function restore_value() {
        $("#modify_status_value").val("none");
        $("#modify_status_info").val("none");
        $("#update_info").val("none");
        $("#add_info").val("none");
        $("#del_info").val("none");
    }

    //显示数据总条数和符合查询条件的条数
    function showNum(totalNum, num) {
        $("#showNum").html('总数量' + totalNum + ',符合查询条件的数量' + num);
    }

    //创建分页
    function createPage(count, index) {
        $("[id*='paginate']").paginate({
            count: count,
            start: index,
            display: 9,
            border: true,
            border_color: '#fff',
            text_color: '#fff',
            background_color: 'black',
            border_hover_color: '#ccc',
            text_hover_color: '#000',
            background_hover_color: '#fff',
            images: false,
            mouse: 'press',
            onChange: function (page) {
                //$('._current', '#paginationdemo').removeClass('_current').hide();
                //$('#p' + page).addClass('_current').show();
                show(page);
            }
        });
    }

    //创建表格
    function createTable(data) {
        for (i in data) {
            //for (var i=1;i<data.length;i++)
            $('#ticket-info').append(
                "<tr>" +
                "<td><span><input type='checkbox' name='select' id='select' value=" + data[i].ticket_id + "></span></td>" +
                "<td>" + i + "</td>" +
                "<input type='hidden' name='id' value=" + data[i].ticket_id + ">" +
                "<td>" + data[i].ticket_id + "</td>" +
                "<td>" + data[i].tel_phone + "</td>" +
                "<td>" + data[i].idcard_num + "</td>" +
                "<td>" + data[i].ticket_date + "</td>" +
                "<td>" + data[i].start_from + "</td>" +
                "<td>" + data[i].end_to + "</td>" +
                "<td>" + data[i].train_number + "</td>" +
                // "<td>" + "<textarea " + "id=" + data[i].ticket_id + "&passengers" + " readonly=\"readonly\" " +
                // "onclick='layer_content(data[i].ticket_id)'>" + data[i].passengers + "</textarea>" +
                "<td>" + "<a href='javascript:void(0);' onclick='show_content(this)' class='passengers_text' id=" + data[i].ticket_id + "&passengers >" + '查看详情' + "</a>" +
                "<textarea style=\"display:none\" id=" + data[i].ticket_id + "_content >" + data[i].passengers + "</textarea></td>" +
                "<td>" + data[i].passenger_num + "</td>" +
                "<td>" + data[i].success_rate + "</td>" +
                "<td>" + data[i].price + "</td>" +
                "<td>" + data[i].status + "</td>" +
                "<td>" + data[i].create_date + "</td>" +
                "<td>" + data[i].update_date + "</td>" +
                "<td><a href='#' id=" + data[i].ticket_id + ">" + 'del' + "</a></td>" +
                "</tr>");
        }
    }

    //根据hidden_column输入框的值显示或隐藏列
    function showColumn() {
        var status = $("#status_select_column").val();
        if (status != '') {
            select_column = column.toString().split(',');
            //alert(select_column);
            $('table tr').find("th").show();
            $('table tr').find("td").show();
            $.each(select_column, function (n, value) {
                $('table tr').find("th:eq(" + value + ")").hide();
                $('table tr').find("td:eq(" + value + ")").hide();
            });
        }
    }

    //点击搜索，把sort,del,update信息都设为none
    $('#search').bind('click', function () {
        ticket_id = $('input[name="ticket_id"]').val();
        tel_phone = $('input[name="tel_phone"]').val();
        id_card_num = $('input[name="id_card_num"]').val();
        status = $('select[name="status_select"]').val();
        $("#search_info").val(ticket_id + '&' + tel_phone + '&' + id_card_num + '&' + status); //为排序信息输入框赋值，以便后续翻页时取得该值
        $("#update_info").val('none');
        $("#del_info").val('none');
        $("#sort_info").val('none');
        $("#add_info").val('none');
        show();
        return false;
    });

    /*点击排序,把search,del,update信息都设为none
    排序有三种状态：无序，升序，降序，默认为无序，第一次点击为升序，第二次点击为降序，第三次点击为无序*/
    $('th>a').bind('click', function () {
        sort = $(this).attr('sort');    //首先取出上次的排序方式
        //alert(sort);
        if (sort == '') {
            $(this).attr('sort', 'asc');
            $(this).next().attr('class', "datagrid-sort-asc");
        }
        if (sort == 'asc') {
            $(this).attr('sort', 'desc');
            $(this).next().attr('class', "datagrid-sort-desc");
        }
        if (sort == 'desc') {
            $(this).attr('sort', '');
            $(this).next().attr('class', "datagrid-sort");
        }
        // 得到sort属性
        sort = $(this).attr('sort');
        //alert(sort);
        if (sort != '') {
            // 得到标签的名字
            keyword = $(this).attr('name');
            //alert(sort+keyword);
            $("#sort_info").val(keyword + '&' + sort); //为排序信息输入框赋值，以便后续翻页时取得该值
            $("#update_info").val('none');
            $("#del_info").val('none');
            $("#search_info").val('none');
            $("#add_info").val('none');
            show();
        } else {
            $("#sort_info").val('none');
        }
    });

    //根据复选框状态进行删除
    $('#mutiple_del').bind('click', function () {
        var ids = "";
        $('input[type="checkbox"][name="select"]:checked').each(function () {
            ids = ids + "&" + $(this).val();
            $(this).css("background-color", "#FFFFCC");
        });
        ids = ids.substring(1, ids.Length);
        if (ids) {
            alert(ids);
            //$("#del_info").attr("value",ids);
            $("#del_info").val(ids);
            $("#update_info").val('none');
            //$("#search_info").val();
            current_page = $('#current_page').val();
            show(current_page);
        } else {
            alert('请至少选择一项！');
            return false;
        }
    });

    //根据复选框状态进行更新
    $('#modify_status_1').bind('click', function () {
        batch_modify_status("1")
    });

    //根据复选框状态进行更新
    $('#modify_status_2').bind('click', function () {
        batch_modify_status("2")
    });

    //根据复选框状态进行更新
    $('#modify_status_3').bind('click', function () {
        batch_modify_status("3")
    });

    //根据复选框状态进行更新
    $('#only_import').bind('click', function () {
        batch_modify_status("3")
    });

    function batch_modify_status(status_val) {
        var ids = "";
        $('input[type="checkbox"][name="select"]:checked').each(function () {
            ids = ids + "&" + $(this).val();
            $(this).css("background-color", "#FFFFCC");
        });
        ids = ids.substring(1, ids.Length);
        if (ids) {
            alert(ids);
            $("#modify_status_info").val(ids);
            $("#modify_status_value").val(status_val);
            current_page = $('#current_page').val();
            show(current_page);
        } else {
            alert('请至少选择一项！');
            return false;
        }
    }

    //选中行变色
    $('#ticket-info').on('change', "td>span>input", function () {
        $(this).parent().parent().parent().toggleClass("tr_select");
    });

    //拖动改变表格宽度
    $(function () {
        $("#tickets").colResizable({
            liveDrag: true,
            gripInnerHtml: "<div class='grip'></div>",
            draggingClass: "dragging"
        });
    });

    $("#select_all").click(function () {
        if (this.checked) {
            $("#ticket-info :checkbox").prop("checked", true);
        } else {
            $("#ticket-info :checkbox").prop("checked", false);
        }
    });

    $("#refresh_current_page").click(function () {
        show();
    });

    $("#adjust_page_size").blur(function () {
        show();
    })
});