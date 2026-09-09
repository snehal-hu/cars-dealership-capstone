from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from dealership import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='About.html'), name='home'),

    path('admin/', admin.site.urls),

    # Existing authentication routes
    path('djangoapp/register', views.register, name='register'),
    path('djangoapp/loginuser', views.loginuser, name='loginuser'),
    path('djangoapp/logoutuser', views.logoutuser, name='logoutuser'),

    # Existing dealer routes
    path('djangoapp/getalldealers', views.getalldealers, name='getalldealers'),
    path('djangoapp/getdealerbyid/<int:dealer_id>', views.getdealerbyid, name='getdealerbyid'),
    path('djangoapp/getdealersbyState/<str:state>', views.getdealersbyState, name='getdealersbyState'),
    path('djangoapp/getdealerreviews/<int:dealer_id>', views.getdealerreviews, name='getdealerreviews'),

    # Existing review routes
    path('djangoapp/submit/<int:dealer_id>', views.submit, name='submit'),
    path('djangoapp/analyzereview', views.analyzereview, name='analyzereview'),

    # Existing car route
    path('djangoapp/getallcarmakes', views.getallcarmakes, name='getallcarmakes'),

    # Grader-required API aliases
    path('fetchDealers', views.getalldealers, name='fetchDealers'),
    path('fetchDealer/<int:dealer_id>', views.getdealerbyid, name='fetchDealer'),
    path('fetchDealers/<str:state>', views.getdealersbyState, name='fetchDealersByState'),
    path('fetchReviews/dealer/<int:dealer_id>', views.getdealerreviews, name='fetchReviewsDealer'),
    path('analyze/<str:review>', views.analyze_review_get, name='analyze'),

    # Frontend pages
    path(
        'About.html',
        TemplateView.as_view(template_name='About.html'),
        name='about'
    ),
    path(
        'Contact.html',
        TemplateView.as_view(template_name='Contact.html'),
        name='contact'
    ),
]
