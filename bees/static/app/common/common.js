function addShop(goods_id) {
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/u/addgoods/',
        type: 'POST',
        data: {'goods_id': goods_id},
        datatype: 'json',
        headers: {'X-CSRFToken': csrf},
        success:function (msg) {
            s = '<span class="chsel" onclick="cartchangeselect(' + msg.cart_id + ')">√</span>';
            $('#changeselect_'+msg.cart_id).html(s);
            $('#num_' + goods_id).html(msg.c_num);
            $('#totalPrice').html('总价:' + msg.total);
            $('#price_'+goods_id).html('小计：￥'+msg.iprice+'元');
            if(msg.is_selectall){
                $('#selectAll').html('<span onclick="allSelect()">√</span>');
            }

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
            s = '<span class="chsel" onclick="cartchangeselect(' + msg.cart_id + ')">√</span>';
            $('#changeselect_'+msg.cart_id).html(s);
            $('#num_' + goods_id).html(msg.c_num);
            $('#totalPrice').html('总价:' + msg.total);
            $('#price_'+goods_id).html('小计：￥'+msg.iprice+'元');
            if(msg.is_selectall){
                $('#selectAll').html('<span onclick="allSelect()">√</span>');
            }
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
                s1 = '<span class="chsel" onclick="cartchangeselect(' + cart_id + ')">√</span>'
            }else{
                s1 = '<span class="chsel" onclick="cartchangeselect(' + cart_id + ')">x</span>'
            }
            if(msg.is_selectall){
                s2 = '<span onclick="allSelect()">√</span>'
            }else {
                s2 = '<span onclick="allSelect()">x</span>'
            }

            $('#changeselect_'+cart_id).html(s1);
            $('#selectAll').html(s2);
            $('#totalPrice').html('总价:' + msg.total);
        },
        error:function (msg) {
            alert('请求错误')
        }
    })
}

function allSelect() {
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    console.log(1)
    $.ajax({
        url: '/u/select_all/',
        type: 'POST',
        datatype: 'json',
        headers: {'X-CSRFToken': csrf},
        success:function (msg) {
            if(msg.selectall){
                s1 = '<span onclick="allSelect()">√</span>'
                s2 = '√'
            }else{
                s1 = '<span onclick="allSelect()">x</span>'
                s2 = 'x'
            }

            $('#selectAll').html(s1);
            $('.chsel').html(s1);
            $('#totalPrice').html('总价:' + msg.total);
        },
        error:function (msg) {
            alert('请求错误')
        }
    })
}
