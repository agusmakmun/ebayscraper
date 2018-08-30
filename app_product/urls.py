# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import path

from app_product.views import (ProductScrape, ProductCartDetail,
                               ProductPaymentDetail)

urlpatterns = [
    path('', ProductScrape.as_view(), name='product_scrape'),
    path('cart/<int:pk>/', ProductCartDetail.as_view(), name='product_cart_detail'),
    path('payment/<int:pk>/', ProductPaymentDetail.as_view(), name='product_payment_detail'),
]
