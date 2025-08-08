from django.shortcuts import render

from site_setting.models import SiteSetting

from hamayesh_module.models import Hamayesh_prices

from news_module.models import News


def site_header_component(request):
    setting : SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    context = {
        'site_setting': setting,
    }
    return render(request,'shared/site_header_component.html',context)

def site_footer_component(request):
    setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    context = {
        'site_setting': setting,
    }
    return render(request,'shared/site_footer_component.html',context)

# def page_not_found(request):
    # setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    # context = {
        # 'site_setting': setting,
    # }

    # return render(request,'shared/404_page.html', context)

def index(request):
    setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    # hamayesh_topics = Hamayesh_topics.objects.all()
    hamayesh_prices = Hamayesh_prices.objects.all()
    news_module = News.objects.all()
    context = {
        'site_setting': setting,
        # 'hamayesh_topics': hamayesh_topics,
        'hamayesh_prices': hamayesh_prices,
        'news_module': news_module,
    }
    return render(request, 'index_module/index.html', context)

# 404
def page_not_found(request):
    return render(request,'shared/404_page.html')

def handler404(request, exception):
    return render(request, 'shared/404_page.html', status=404)