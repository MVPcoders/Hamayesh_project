from django.shortcuts import render



def site_header_component(request):
    # setting : SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    context = {
        # 'site_setting': setting,
    }
    return render(request,'shared/site_header_component.html',context)

def site_footer_component(request):
    # setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    context = {
        # 'site_setting': setting,
    }
    return render(request,'shared/site_footer_component.html',context)

# def page_not_found(request):
    # setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    # context = {
        # 'site_setting': setting,
    # }

    # return render(request,'shared/404_page.html', context)

def index(request):
    # setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    context = {
        # 'site_setting': setting,
    }
    return render(request, 'index_module/index.html', context)




# Create your views here.
