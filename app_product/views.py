# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import (get_object_or_404, redirect)
from django.views.generic import (TemplateView, DetailView)

from app_scraper.utils.scraper import scrape_product_info
from app_product.models import Product


class ProductScrape(TemplateView):
    template_name = 'app_product/product_scrape.html'

    def post(self, request, *args, **kwargs):

        if 'url' in request.POST:
            ebay_url = request.POST.get('url')
            product_info = scrape_product_info(ebay_url)

            product = Product(item_id=product_info.get('item_id'),
                              name=product_info.get('name'),
                              price=product_info.get('current_price'),
                              color=product_info.get('item_specific').get('color'),
                              size=product_info.get('item_specific').get('size'))
            product.save()
            return redirect('product_cart_detail', pk=product.pk)

        return super().post(request, *args, **kwargs)


class ProductCartDetail(DetailView):
    template_name = 'app_product/product_cart_detail.html'
    context_object_name = 'product'
    model = Product


class ProductPaymentDetail(ProductCartDetail):
    template_name = 'app_product/product_payment_detail.html'
