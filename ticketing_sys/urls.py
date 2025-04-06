from django.urls import path
from .views import QueryListCreateAPIView, AllQueriesAPIView, AssignQueryAPIView
from .views import EmployeeListCreateAPIView, EmployeeDetailAPIView, AssignQueryAPIView




urlpatterns = [
    path('queries/', QueryListCreateAPIView.as_view(), name='query-list-create'),
    path('all-queries/', AllQueriesAPIView.as_view(), name='all-queries'),
    path('assign_queries/', AssignQueryAPIView.as_view(), name='assign_queries'),

    path('employees/', EmployeeListCreateAPIView.as_view(), name='employee-list-create'),
    path('employees/<int:pk>/', EmployeeDetailAPIView.as_view(), name='employee-detail'),
    path('queries/assign/', AssignQueryAPIView.as_view(), name='assign-query'),

]