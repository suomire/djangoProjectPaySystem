from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import TransactionsViewSet, TransactionsView, UsersViewSet, UsersView

app_name = "PaySystem"

router = DefaultRouter()
router.register(r'usersViewSet', UsersViewSet)

router.register(r'transactionViewSet', TransactionsViewSet)

urlpatterns = router.urls + [
    path('users/', UsersView.as_view()),
    path('transactions/', TransactionsView.as_view()),
]
