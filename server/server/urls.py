from django.contrib import admin
from django.urls import path
from dealership import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication
    path('djangoapp/register', views.register, name='register'),
    path('djangoapp/loginuser', views.loginuser, name='loginuser'),
    path('djangoapp/logoutuser', views.logoutuser, name='logoutuser'),

    # Dealers
    path('djangoapp/getalldealers', views.getalldealers, name='getalldealers'),
    path('djangoapp/getdealerbyid/<int:dealer_id>', views.getdealerbyid, name='getdealerbyid'),
    path('djangoapp/getdealersbyState/<str:state>', views.getdealersbyState, name='getdealersbyState'),
    path('djangoapp/getdealerreviews/<int:dealer_id>', views.getdealerreviews, name='getdealerreviews'),

    # Reviews
    path('djangoapp/submit/<int:dealer_id>', views.submit, name='submit'),
    path('djangoapp/analyzereview', views.analyzereview, name='analyzereview'),

    # Cars
    path('djangoapp/getallcarmakes', views.getallcarmakes, name='getallcarmakes'),
]