function addShop(goods_id) {
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    console.log('x');
    $.ajax({
        url: '/u/addgoods/',
        type: 'POST',
        data: {'goods_id': goods_id},
        datatype: 'json',
        headers: {'X-CSRFToken': csrf},
        success:function (msg) {
            s = '<span onclick="cartchangeselect(' + msg.cart_id + ')">√</span>';
            $('#changeselect_'+msg.cart_id).html(s);
            $('#num_' + goods_id).html(msg.c_num);
            $('#totalPrice').html('总价:' + msg.total);
            $('#price_'+goods_id).html('小计：￥'+msg.iprice+'元');

        },
        error:function (msg) {
            alert('请求错误')
        }
    })
}


function subShop(goods_id) {
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/u/subgoods/',
        type: 'POST',
        data: {'goods_id': goods_id},
        datatype: 'json',
        headers: {'X-CSRFToken': csrf},
        success:function (msg) {
            $('#num_' + goods_id).html(msg.c_num);
            $('#totalPrice').html('总价:' + msg.total);
            $('#price_'+goods_id).html('小计：￥'+msg.iprice+'元');
        },
        error:function (msg) {
            alert('请求错误')
        }
    })
}


function cartchangeselect(cart_id) {
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/u/change_select/',
        type: 'POST',
        data: {'cart_id': cart_id},
        datatype: 'json',
        headers: {'X-CSRFToken': csrf},
        success:function (msg) {
            if(msg.is_select){
                s = '<span onclick="cartchangeselect(' + cart_id + ')">√</span>'
            }else{
                s = '<span onclick="cartchangeselect(' + cart_id + ')">x</span>'
            }

            $('#changeselect_'+cart_id).html(s);
            $('#totalPrice').html('总价:' + msg.total);
        },
        error:function (msg) {
            alert('请求错误')
        }
    })
}

function allSelect() {
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/u/change_select/',
        type: 'POST',
        datatype: 'json',
        headers: {'X-CSRFToken': csrf},
        success:function (msg) {
            if(msg.is_selectall){
                s = '<span onclick="allSelect">√</span>'
            }else{
                s = '<span onclick="allSelect">x</span>'
            }

            $('#selectAll').html(s);
            $('#totalPrice').html('总价:' + msg.total);
        },
        error:function (msg) {
            alert('请求错误')
        }
    })
}
