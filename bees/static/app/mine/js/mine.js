$(function () {

    $("#order_payed_list").click(function () {

        window.open("/uauth/orderlist/", target="_self");

    })

    $("#wait_pay_list").click(function () {

        window.open("/uauth/orderlistwaitpay/", target="_self");

    })

})