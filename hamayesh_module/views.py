from django.shortcuts import render
from hamayesh_module.models import Hamayesh_topics, Hamayesh_prices, Hamayesh_signup_categories


def HamayeshModule(request):
    hamayesh_topics = Hamayesh_topics.objects.all()
    hamayesh_prices = Hamayesh_prices.objects.all()
    hamayesh_signup_category = Hamayesh_signup_categories.objects.all()


    context = {
        'hamayesh_topics': hamayesh_topics,
        'hamayesh_prices': hamayesh_prices,
        'hamayesh_signup_category': hamayesh_signup_category,

    }
    return render(request, 'hamayesh_module/hamayesh_page.html', context)
