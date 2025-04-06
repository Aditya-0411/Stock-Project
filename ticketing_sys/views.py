# from django.contrib.auth.decorators import user_passes_test
# from django.http import Http404
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status, viewsets
# from rest_framework.permissions import IsAuthenticated
# from .models import Ticket
# from .serializers import TicketSerializer
# from rest_framework.decorators import api_view, permission_classes
# def is_superuser(user):
#     return user.is_superuser
# # class TicketViewSet(APIView):
# #     permission_classes = [IsAuthenticated]
# #
# #     @user_passes_test(is_superuser)
# #     def get(self, request, format=None,pk=None, *args, **kwargs):
# #         user = request.user
# #
# #         if pk is not None:
# #             ticket = self.get_object(pk)
# #             serializer = TicketSerializer
# #             return Response(serializer.data)
# #         else:
# #             tickets = Ticket.objects.all()
# #             serializer = TicketSerializer(tickets, many=True)
# #             return Response(serializer.data, status=200)
# #
# #
# #     def post(self, request,pk=None, *args, **kwargs):
# #         user = request.user
# #         if pk is not None:
# #             return self.post(request,pk,*args, **kwargs)
# #         serializer = TicketSerializer(data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #
# #     def put(self, request, pk=None, *args, **kwargs):
# #         user = request.user
# #         if pk is not None:
# #             return self.put(request,pk,*args, **kwargs)
# #         serializer = TicketSerializer(data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data)
# #         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
# #
# #
# #
# #     def delete(self, request, pk=None, *args, **kwargs):
# #         ticket=self.get_object(pk)
# #         ticket.delete()
# #         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
#
#
#
#
# # @api_view(['GET'])
# # @permission_classes([IsAuthenticated])
# # @user_passes_test(is_superuser)
# class TicketAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request, pk=None):
#         if pk:
#             ticket = self.get_object(pk)
#             serializer = TicketSerializer(ticket)
#             return Response(serializer.data)
#         else:
#             tickets = Ticket.objects.all()
#             serializer = TicketSerializer(tickets, many=True)
#             return Response(serializer.data)
#
#     def get(self, request, pk=None):
#         if pk:
#             ticket = self.get_object(pk)
#             serializer = TicketSerializer(ticket)
#             return Response(serializer.data)
#         else:
#             tickets = Ticket.objects.all()
#             serializer = TicketSerializer(tickets, many=True)
#             return Response(serializer.data)
#
#     def post(self, request):
#         serializer = TicketSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def put(self, request, pk):
#         ticket = self.get_object(pk)
#         serializer = TicketSerializer(ticket, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         ticket = self.get_object(pk)
#         ticket.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#     def get_object(self, pk):
#         try:
#             return Ticket.objects.get(pk=pk)
#         except Ticket.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Query,Employee
from .serializers import QuerySerializer,EmployeeSerializer

class QueryListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queries = Query.objects.filter(user=request.user)
        serializer = QuerySerializer(queries, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = QuerySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AllQueriesAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        queries = Query.objects.all()
        serializer = QuerySerializer(queries, many=True)
        return Response(serializer.data)



class EmployeeListCreateAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeDetailAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        employee = self.get_object(pk)
        if not employee:
            return Response({'error': 'Employee not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Serialize employee details
        employee_serializer = EmployeeSerializer(employee)
        data = employee_serializer.data

        # Get assigned queries for the employee
        assigned_queries = Query.objects.filter(assigned_to=employee)
        query_serializer = QuerySerializer(assigned_queries, many=True)
        data['assigned_queries'] = query_serializer.data

        return Response(data)

    def put(self, request, pk):
        employee = self.get_object(pk)
        if not employee:
            return Response({'error': 'Employee not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        employee = self.get_object(pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AssignQueryAPIView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        # Deserialize the JSON data from the request body
        data = request.data

        # Extract query_id and employee_id from the JSON data
        query_id = data.get('query_id')
        employee_id = data.get('employee_id')

        try:
            query = Query.objects.get(pk=query_id)
            employee = Employee.objects.get(pk=employee_id)
        except (Query.DoesNotExist, Employee.DoesNotExist):
            return Response({'error': 'Query or employee not found.'}, status=status.HTTP_404_NOT_FOUND)

        query.assigned_to = employee
        query.save()
        return Response({'message': 'Query assigned successfully.'})