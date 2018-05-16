// 页面加载准备好了     就是页面基本结构加载完成
$(function () {


    $(".is_choose").click(function () {
        console.log("点击");
        var current_li = $(this);
        var cart_id = current_li.parents("li").attr("cartid");
        console.log(cart_id);

        $.getJSON("/uauth/changecartstatus/", {"cart_id":cart_id}, function (data) {
            console.log(data);
            if (data["status"] == "200"){
                if (data["check"]){
                    var span = current_li.find("span");
                    span.html("√");

                    if(data["is_all_select"]){
                        $("#all_select").find("span").html("<span>√</span>");
                    }

                }else{
                    var span = current_li.find("span");
                    span.html("");
                    $("#all_select").find("span").html("<span></span>");
                }
                current_li.attr("is_select",data["check"]);
            }
        })
    })


    $(".subShopping").click(function () {
        // 代表记住我们这一样  真实是点击的button
        var current_li = $(this);
        var cart_id = current_li.parents("li").attr("cartid");
        console.log(cart_id);

        $.getJSON("/uauth/subcart/", {"cart_id": cart_id}, function (data) {

            console.log(data);

            if (data["status"] == "200"){
                current_li.next().html(data["c_num"]);
            }else if (data["status"] == "903"){
                current_li.parents("li").remove();
            }
        })

    })


    // $(".addShopping").click(function () {
    //
    //     var current_li = $(this);
    //     var cart_id = current_li.parents("li").attr("cartid");
    //
    //     $.getJSON("/uauth/addcart/", {"cart_id": cart_id}, function (data) {
    //         console.log(data);
    //         if (data["status"] == "200"){
    //             current_li.prev().html(data["c_num"]);
    //         }
    //     })
    //
    // })




//     $("#generate_order").click(function () {
//
//
//         var select_list = [];
//
//         $(".is_choose").each(function () {
//
//             var current = $(this);
//
//             if (current.attr("is_select").toLowerCase() == "true") {
//                    var cart_id = current.parents("li").attr("cartid");
//                    select_list.push(cart_id);
//             }
//         })
//
//         if (select_list.length == 0) {
//             alert("您还没有选择任何商品");
//             return false
//         }else{
//
//             $.getJSON("/uauth/generateorder/", {"selects": select_list.join("#")}, function (data) {
//                 console.log(data);
//
//                 if (data["status"] == "200"){
//
//                     window.open("/uauth/orderinfo/"+data["order_id"]+"/", target="_self");
//
//                 }
//
//             })
//
//
//
//
//         }
//
//     })
//
//
//
})