"""family_budget URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from budget_core import views
from users import views as users_views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'user', users_views.UserViewSet)
router.register(r'group', users_views.GroupViewSet)
router.register(r'category', views.CategoryViewSet)
router.register(r'budget', views.BudgetViewSet, basename='budget')
router.register(r'budget-item', views.BudgetItemViewSet, basename='budget-item')


urlpatterns = [
    # admin urls
    path('admin/', admin.site.urls),
    # auth token urls
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # app urls
    path('', include(router.urls)),
]
