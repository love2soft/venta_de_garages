"""
URL configuration for vgaraje project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from web import views as webview
from administracion import views as root

urlpatterns = [
    path('root/', root.main),
    path('root/<str:path>', root.main),
    path('admin/', admin.site.urls),
    path('Template/css/<str:path>', webview.handler),
    path('Template/fonts/<str:path>', webview.handler),
    path('Template/media/<str:path>', webview.handler),
    path('web/Template/media/<str:path>', webview.handler),
    path('Template/media/Prod/<str:path>', webview.handler),
    path('Template/media/promo/<str:path>', webview.handler),
    path('Template/media/icons/<str:path>', webview.handler),
    path('Template/scripts/<str:path>', webview.handler),
    path('Template/<str:path>', webview.handler),
    path('Template/Inicio/<str:path>', webview.handler),
    path('Template/Dueño/<str:path>', webview.handler),
    path('Template/User/<str:path>', webview.handler),
    path('media/<str:path>', webview.handler),
    path('media/icons/<str:path>', webview.handler),
    path('', webview.handler),
    path("signup/", webview.signup),
    path("signin/", webview.signin),
    path("auth/<str:path>", webview.auth),
    path("logout/", webview.logout),
    path("deleteProducto/", webview.deleteProducto),
    path("delGarage/", webview.delGarage),
    path("delPromocion/", webview.delPromocion),
    path("addGarage/", webview.addGarage),
    path("addProducto/", webview.addProducto),
    path("addPromocion/", webview.addPromocion),
    path("editProductoView/", webview.editProductoView),
    path("editProducto/", webview.editProducto),
    path("editGarageView/", webview.editGarageView),
    path("editGarage/", webview.editGarage),
    path("Template/product/<int:id>" ,webview.showProduct),
    path("Template/garage/<int:id>" ,webview.showGarage),
    path("search/" ,webview.search),
]
