import re
from datetime import datetime, timedelta
# import time

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password


# Create your views here.
from uauth.models import MainWheel, MainNav, MainHotSale, MainShop, MainShow, UserModel, UserTicketModel, FoodType, \
    Goods, CartModel, OrderModel, OrderGoodsModel
from django.core.urlresolvers import reverse
from utils.function import get_ticket


def home(request):
    banners = MainWheel.objects.all()
    navs = MainNav.objects.all()
    hotsales = MainHotSale.objects.all()
    shops = MainShop.objects.all()
    shows = MainShow.objects.all()
    data = {
        'banners': banners,
        'navs': navs,
        'hotsales': hotsales,
        'shops': shops,
        'shows': shows,

    }
    return render(request, 'home/home.html', data)


def market(request):
    if request.method == 'GET':
        foodtypes = FoodType.objects.all()
        typeid = request.GET.get('typeid', 104749)
        foodtype = FoodType.objects.get(typeid=typeid)
        childname = foodtype.childtypenames.split('#')
        childname_list = re.findall(r'([\u4e00-\u9fa5]+[/]?[\u4e00-\u9fa5]+)', str(childname))
        childcname = request.GET.get('childcidname', '全部分类')
        # if childcname == '全部分类' or childcname == '':
        #     goods = Goods.objects.filter(categoryid=typeid)
        # else:
        #     goods = Goods.objects.filter(categoryid=typeid, childcidname=childcname)
        goods = Goods.objects.filter(categoryid=typeid) if \
            childcname == '全部分类' or childcname == '' else \
            Goods.objects.filter(categoryid=typeid, childcidname=childcname)
        sort_type = request.GET.get('sort_type', 0)
        if sort_type == '0':
            goods = goods.order_by('id')
        if sort_type == '1':
            goods = goods.order_by('-productnum')
        if sort_type == '2':
            goods = goods.order_by('-price')
        if sort_type == '3':
            goods = goods.order_by('price')
        user = request.user

        data = {
            'foodtypes': foodtypes,
            'typeid': typeid,
            'childname_list': childname_list,
            'goods': goods,
            'childcname': childcname,
            'sort_types': sort_type,
            'user': user
        }
        return render(request, 'market/market.html', data)


def ucart(request):
    if request.method == 'GET':
        user = request.user
        if user and user.id:
            # 如果用户已经登录，则加载购物车的数据
            carts = CartModel.objects.filter(user_id=user.id)
            total = calc_total(user)
            isall = is_select_all(user)
            return render(request, 'cart/cart.html', {'carts': carts, 'total': total, 'isall': isall})
        else:
            return HttpResponseRedirect(reverse('axf:log'))


def mine(request):
    if request.method == 'GET':
        user = request.user
        data = {}
        if user.id:
            orders = user.ordermodel_set.all()
            wait_pays, payeds = 0, 0
            for order in orders:
                if order.o_status == '0':
                    wait_pays += 1
                elif order.o_status == '1':
                    payeds += 1
            data['wait_pay'] = wait_pays
            data['payed'] = payeds
        return render(request, 'mine/mine.html', data)


def register(request):
    if request.method == 'GET':
        return render(request, 'user/user_register.html')
    if request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        icon = request.FILES.get('icon')
        password = make_password(password)
        UserModel.objects.create(username=name, password=password,
                                 email=email, icon=icon)
        return HttpResponseRedirect('/u/login/')


def login(request):
    if request.method == 'GET':
        return render(request, 'user/user_login.html')
    if request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')
        if UserModel.objects.filter(username=name).exists():
            user = UserModel.objects.get(username=name)
            if check_password(password, user.password):
                ticket = get_ticket()
                response = HttpResponseRedirect('/u/home/')
                out_time = datetime.now() + timedelta(days=1)
                response.set_cookie('ticket', ticket, expires=out_time)
                # 服务器存储时间
                UserTicketModel.objects.create(user=user,
                                               ticket=ticket,
                                               out_time=out_time)

                return response
            else:
                return render(request, 'user/user_login.html', {'password': '用户密码错误'})
        else:
            return render(request, 'user/user_login.html', {'name': '用户不存在'})


def logout(request):
    if request.method == "GET":
        response = HttpResponseRedirect('/u/mine/')
        response.delete_cookie('ticket')
        # 删除服务端
        ticket = request.COOKIES.get('ticket')
        uticket = UserTicketModel.objects.filter(ticket=ticket)
        uticket.delete()

        return response


def add_goods(request):
    if request.method == 'POST':
        data = {
            'msg': '请求成功',
            'code': 200
        }
        user = request.user
        if user and user.id:
            goods_id = request.POST.get('goods_id')
            user_carts = CartModel.objects.filter(user=user, goods_id=goods_id).first()
            price = Goods.objects.filter(id=goods_id).first().price
            # price = user_carts.goods.price
            if user_carts:
                user_carts.c_num += 1
                user_carts.iprice = user_carts.c_num * price
                user_carts.iprice = float('%.2f' % user_carts.iprice)
                user_carts.is_select = True
                user_carts.save()
                data['c_num'] = user_carts.c_num
            else:
                # 用户没选商品，则创建
                CartModel.objects.create(user=user, goods_id=goods_id, c_num=1, iprice=price)
                user_carts = CartModel.objects.get(user=user, goods_id=goods_id, c_num=1, iprice=price)
                data['c_num'] = 1

            data['iprice'] = user_carts.iprice
            data['total'] = calc_total(user)
            data['cart_id'] = user_carts.id
            data['is_selectall'] = is_select_all(user)
        return JsonResponse(data)


def sub_goods(request):
    if request.method == 'POST':
        data = {
            'msg': '请求成功',
            'code': 200
        }
        user = request.user
        if user and user.id:
            goods_id = request.POST.get('goods_id')
            # 查看当前商品是否已经在购物车中
            user_carts = CartModel.objects.filter(user=user, goods_id=goods_id).first()
            price = user_carts.goods.price
            # 如果存在则减1
            if user_carts:
                if user_carts.c_num == 1:
                    user_carts.delete()
                    data['c_num'] = 0
                else:
                    user_carts.c_num -= 1
                    user_carts.iprice = user_carts.c_num * price
                    user_carts.iprice = float('%.2f' % user_carts.iprice)
                    user_carts.is_select = True
                    user_carts.save()
                    data['c_num'] = user_carts.c_num

            data['total'] = calc_total(user)
            data['iprice'] = user_carts.iprice
            data['cart_id'] = user_carts.id
            data['is_selectall'] = is_select_all(user)
        return JsonResponse(data)


def user_change_select(request):
    if request.method == 'POST':
        cart_id = request.POST.get('cart_id')
        user = request.user
        data = {
            'code': 200,
            'msg': '请求成功'
        }

        if user and user.id:
            cart = CartModel.objects.filter(pk=cart_id).first()
            if cart.is_select:
                cart.is_select = False
            else:
                cart.is_select = True
            cart.save()
            data['is_select'] = cart.is_select
            total = calc_total(user)
            data['total'] = total
            data['is_selectall'] = is_select_all(user)
        return JsonResponse(data)


def select_all(request):
    if request.method == 'POST':
        user = request.user
        data = {
            'code': 200,
            'msg': '请求成功'
        }
        if user and user.id:
            carts = CartModel.objects.filter(user=user)
            if is_select_all(user):
                for cart in carts:
                    cart.is_select = False
                    cart.save()
            else:
                for cart in carts:
                    cart.is_select = True
                    cart.save()

            data['selectall'] = is_select_all(user)
            data['total'] = calc_total(user)
        return JsonResponse(data)


def is_select_all(user):
    selected = 0
    carts = CartModel.objects.filter(user=user)
    for cart in carts:
        if cart.is_select:
            selected += 1
    is_selectall = True if selected == len(carts) else False
    return is_selectall


def calc_total(user):
    carts = CartModel.objects.filter(user=user, is_select=1)
    total = 0
    for cart in carts:
        total += cart.iprice
        total = float('%.2f' % total)
    return total


def gen_order(request):
    if request.method == 'GET':
        user = request.user
        if user and user.id:
            # 查询购物车中选中的商品
            carts_goods = CartModel.objects.filter(user=user, is_select=True)
            # 创建订单
            order = OrderModel.objects.create(user=user, o_status=0, o_total=calc_total(user))
            # 创建订单详情信息
            for carts in carts_goods:
                OrderGoodsModel.objects.create(goods=carts.goods,
                                               order=order,
                                               goods_num=carts.c_num)
                carts.delete()
            # carts_goods.delete()
            return HttpResponseRedirect(reverse('axf:pay', args=(order.id,)))


def pay(request, order_id):
    if request.method == 'GET':
        orders = OrderModel.objects.filter(pk=order_id).first()
        data = {
            'order_id': order_id,
            'orders': orders
        }
        return render(request, 'order/order_info.html', data)


def orderpay(request, order_id):
    if request.method == "GET":
        OrderModel.objects.filter(pk=order_id).update(o_status=1)
        return HttpResponseRedirect(reverse('axf:mine'))


def wait_pay(request):
    if request.method == 'GET':
        user = request.user
        if user and user.id:
            orders = OrderModel.objects.filter(user=user, o_status=0)

            return render(request, 'order/order_list_wait_pay.html', {'orders': orders})


def payed(request):
    if request.method == 'GET':
        user = request.user
        if user and user.id:
            orders = OrderModel.objects.filter(user=user, o_status=1)

            return render(request, 'order/order_list_payed.html', {'orders': orders})
