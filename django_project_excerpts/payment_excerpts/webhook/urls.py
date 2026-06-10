from django.urls import path
from .api import PayStackWebhookRouteView, StripeWebhookRouteView, FincraWebhookRouteView
urlpatterns = [
    path('paystack',PayStackWebhookRouteView.as_view()),
    path('stripe',StripeWebhookRouteView.as_view()),
    path('fincra',FincraWebhookRouteView.as_view())
]