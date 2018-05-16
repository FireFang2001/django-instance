from django.conf.urls import url

from uauth import views

urlpatterns = [
    url(r'^home/', views.home, name='home'),
    url(r'^market/', views.market, name='market'),
    url(r'^mine/', views.mine, name='mine'),
    url(r'^cart/', views.ucart, name='cart'),
    url(r'^register/', views.register, name='reg'),
    url(r'^login/', views.login, name='log'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^addgoods/', views.add_goods, name='addgoods'),
    url(r'^subgoods/', views.sub_goods, name='subgoods'),
    url(r'^change_select/', views.user_change_select, name='changeselect'),
    url(r'^select_all/', views.select_all, name='selectall'),
    # 下单
    url(r'^generate_order', views.gen_order, name='genorder'),
    # 付款
    url(r'^pay/(\d+)/', views.pay, name='pay'),
    # 确认付款
    url(r'^orderpay/(\d+)/', views.orderpay, name='orderpay'),
    # 待付款
    url(r'^waitpay/', views.wait_pay, name='waitpay'),
    # 待收货
    url(r'^payed/', views.payed, name='payed'),
    # url(r'^checkuser/', views.checkuser, name='check'),
]
