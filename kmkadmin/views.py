
from .models import StockTarget
import datetime
from .serializers import StockLogSerializer
from .serializers import StockReportSerializer
from .models import StockReportLog
from .serializers import StockReportLogSerializer
from django.shortcuts import get_object_or_404
from .models import StockReport
from rest_framework.views import APIView
from rest_framework import serializers
from django.db import IntegrityError
from .models import Stock, Stocklog
from .serializers import StockSerializer, StockTargetSerializer
from .custom_formula import update_stock_data
from django.contrib.auth.models import Group, User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Permission
from .models import Blogs
from .serializers import BlogSerializer
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from uuid import UUID

#StockLog
class StockLogListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        logs = Stocklog.objects.filter(user=user)
        serializer = StockLogSerializer(logs, many=True)
        return Response(serializer.data)



# Get all stocks data
class AllStocksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        print(f"User {user.username} is retrieving all stocks data.")
        response = Response()

        try:
            # Get all stocks
            queryset = Stock.objects.all()

            # Serialize each stock along with its attached report (if any)
            stocks_data = []
            for stock in queryset:
                stock_data = StockSerializer(stock).data

                # Get the attached reports for the current stock
                reports = StockReport.objects.filter(user=user, stock_id=stock.id)
                if reports.exists():
                    # Assuming you want to include the details of the latest report if multiple exist
                    latest_report = reports.latest('created_at')
                    stock_data['report_id'] = latest_report.id
                    stock_data['report_file'] = latest_report.report_file.url
                    stock_data['report_created_at'] = latest_report.created_at

                stocks_data.append(stock_data)

            response.data = stocks_data
            response.status_code = 200

        except Exception as e:
            response.data = {'error': str(e)}
            response.status_code = 500  # Internal server error

        return response


#ADD/CREATE STOCKS
class AddStockView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        response = Response()

        # Extracting data from request
        stock_symbol = request.data.get('stock_symbol')
        stock_scrip_code = request.data.get('stock_scrip_code')
        entry_price = float(request.data.get('entry_price', 0.0))
        target_price = float(request.data.get('target_price', 0.0))
        stock_name = request.data.get('stock_name')
        stock_industry = request.data.get('stock_industry', '').upper()
        no_of_shares = int(request.data.get('no_of_shares', 0))
        stock_exchange = request.data.get('stock_exchange', '').upper()
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        risk = request.data.get('risk', '').capitalize()
        tag1 = request.data.get('tag1', '').strip()
        tag2 = request.data.get('tag2', '').strip()
        status_value = request.data.get('status', '').strip()
        action = request.data.get('action', '').strip()
        live_price = request.data.get('live_price')
        upside_left = request.data.get('upside_left')
        gain_loss = request.data.get('gain_loss')
        market_cap = request.data.get('market_cap')
        expected_returns = request.data.get('expected_returns')
        time_left = request.data.get('time_left')

        if 'BSE' in stock_exchange and stock_scrip_code is None:
         response.data = {"error": "Scrip code required for BSE stocks"}
         response.status_code = status.HTTP_400_BAD_REQUEST
         return response

        if 'NSE' in stock_exchange and stock_symbol is None:
         response.data = {"error": "Stock symbol required for NSE stocks"}
         response.status_code = status.HTTP_400_BAD_REQUEST
         return response

        # if end_date < start_date:
        #   response.data = {"error": "End date must be greater than start date"}
        #   response.status_code = status.HTTP_400_BAD_REQUEST
        #   return response

        try:
            # Attempt to create a new stock instance
            serializer = StockSerializer(data={
                'stock_symbol': stock_symbol,
                'stock_scrip_code': stock_scrip_code,
                'stock_name': stock_name,
                'stock_industry': stock_industry,
                'stock_exchange': stock_exchange,
                'no_of_shares': no_of_shares,
                'risk': risk,
                'start_date': start_date,
                'end_date': end_date,
                'tag1': tag1,
                'tag2': tag2,
                'live_price': live_price,
            })

            # Check if the serializer is valid
            if serializer.is_valid(raise_exception=True):
                # Save the stock instance
                serializer.save()

                # Save instance in Stocklog model whenever user creates a new stock
                Stocklog.objects.create(user=user, stock=serializer.instance.id, action='Stock Added')

                # Create a new stock target instance
                stock_target_serializer = StockTargetSerializer(data={
                    'stock': serializer.data['id'],
                    'entry_price': entry_price,
                    'target_price': target_price,
                    'target_status': status_value,
                    'target_date': end_date,
                    'target_action': 'BUY',
                })

                # Check if the stock target serializer is valid
                stock_target_serializer.is_valid(raise_exception=True)

                # Save the stock target instance
                stock_target_serializer.save()

                # Update stock data
                update_stock_data(serializer.instance.id)

                # Retrieve the updated stock instance
                updated_stock = Stock.objects.get(id=serializer.instance.id)

                # Serialize the updated stock instance
                updated_serializer = StockSerializer(instance=updated_stock)

                # Set the response data and status code
                response.data = {
                    "user_id": user.id,
                    "username": user.username,
                    "stock_data": updated_serializer.data,
                }
                response.status_code = status.HTTP_201_CREATED

        except ValidationError as e:
            # Handle validation errors
            print("ValidationError", e)
            response.data = {"error": str(e)}
            response.status_code = status.HTTP_400_BAD_REQUEST

        except Exception as e:
            # Handle other exceptions
            response.data = {'error': str(e)}
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        return response

# to add a new target of the same stock
class AddNewStockTarget(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        print(f"User {user.username} is adding a new target to stocks data.")

        # Initialize the response
        response = Response()

        # Extract data from the request
        stock_id = request.data.get('stock_id')
        entry_price = request.data.get('entry_price')
        target_price = request.data.get('target_price')
        target_date = request.data.get('target_date')
        target_action = request.data.get('target_action')
        target_status = request.data.get('target_status')

        # Validate the incoming data
        if None in [stock_id, entry_price, target_price, target_date, target_action, target_status]:
            response.data = {"error": "Incomplete data provided"}
            response.status_code = status.HTTP_400_BAD_REQUEST
            return response

        try:
            # Retrieve the stock instance
            stock_instance = Stock.objects.get(id=stock_id)
        except Stock.DoesNotExist:
            response.data = {"error": f"Invalid stock_id: {stock_id}"}
            response.status_code = status.HTTP_400_BAD_REQUEST
            return response

        # Create a new StockTarget instance
        serializer = StockTargetSerializer(data={
            'stock': stock_id,
            'entry_price': entry_price,
            'target_price': target_price,
            'target_date': target_date,
            'target_status': target_status,
            'target_action': target_action
        })

        # Validate the serializer and handle errors
        if serializer.is_valid():
            serializer.save()

            # Create a new entry in Stocklog
            Stocklog.objects.create(user=user, stock=serializer.instance.id, action='Stock Target Added')

            # Update the target_met value in the stock instance
            stock_instance.target_met = timezone.now().date()
            stock_instance.save()

            # Update stock data
            update_stock_data(stock_id)

            # Retrieve the updated stock instance and serialize it
            updated_stock = Stock.objects.get(id=stock_id)
            response.data = StockSerializer(updated_stock, many=False).data
            response.status_code = status.HTTP_200_OK
        else:
            response.data = serializer.errors
            response.status_code = status.HTTP_400_BAD_REQUEST

        return response



# edit data in stock model
class EditStockData(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, *args, **kwargs):
        user = request.user
        print(f"User {user.username} is editing stocks data.")
        response = Response()

        # Extract data from request
        print(request.data)
        stock_id = request.data.get('stock_id')
        stock_name = request.data.get('stock_name')
        stock_exchange = request.data.get('stock_exchange', '').strip()
        stock_industry = request.data.get('stock_industry', '').strip()
        no_of_shares = request.data.get('no_of_shares')
        stock_symbol = request.data.get('stock_symbol', '').strip()
        risk = request.data.get('risk', '').strip()
        tag1 = request.data.get('tag1', '').strip()
        tag2 = request.data.get('tag2', '').strip()

        try:
            # Get the stock instance
            stock = Stock.objects.get(id=stock_id)
            print('stock', stock)

            # Update stock fields
            stock.stock_name = stock_name
            stock.stock_exchange = stock_exchange
            stock.stock_industry = stock_industry
            stock.no_of_shares = no_of_shares
            stock.stock_symbol = stock_symbol
            stock.risk = risk
            stock.tag1 = tag1
            stock.tag2 = tag2

            # Save the changes
            stock.save()
            print('stock', stock)

            #TO SAVE THE INSTANCE IN STOCKLOG MODEL WHEN USER EDITS A STOCK
            Stocklog.objects.create(user=user,stock=stock.id,action='Stock Edited',)

            response.data = {"message": "Stock data updated successfully"}
            response.status_code = 200  # OK
            return response

        except Stock.DoesNotExist:
            response.data = {"error": "Stock not found"}
            response.status_code = 404  # Not found

        except (IntegrityError, serializers.ValidationError) as e:
            response.data = {"error": str(e)}
            response.status_code = 400  # Bad request

        except Exception as e:
            print('e', e)
            response.data = {'error': str(e)}
            response.status_code = 500  # Internal server error
            return response



#DELETE A PARTICULAR STOCK
class DeleteStockView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, *args, **kwargs):
        user = request.user
        print(f"User {user.username} is deleting stock data.")
        response = Response()
        stock_id = request.data.get('stock_id')
        try:
            stock_instance = Stock.objects.get(id=stock_id)
        except Stock.DoesNotExist:
            response.data = {"error": "Stock not found"}
            response.status_code = status.HTTP_404_NOT_FOUND
            return response


        # Delete all stock targets
        StockTarget.objects.filter(stock=stock_instance).delete()
        # Save log entry before deleting the stock instance
        Stocklog.objects.create(user=user, stock=stock_id, action='Stock Deleted')

        # Delete the stock instance
        result = stock_instance.delete()
        print('result', result)

        response.data = {"message": "Stock and associated targets deleted successfully"}
        response.status_code = status.HTTP_204_NO_CONTENT
        return response


#!!!!!!!!!!!!!!!!!!!! To Delete all the data from the database !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

class DeleteAllDataView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, *args, **kwargs):
        user = request.user
        print(f"User {user.username} is deleting all stocks data.")
        response = Response()

        try:
            # Delete all stock targets
            StockTarget.objects.all().delete()

            # Delete all stocks
            Stock.objects.all().delete()

            response.data = {"message": "All data deleted successfully"}
            response.status_code = status.HTTP_204_NO_CONTENT
        except Exception as e:
            response.data = {"error": str(e)}
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        return response



#TO GET AND POST REPORT OF A STOCK
class StockReportView(APIView):
    permission_classes = [IsAuthenticated]


    def post(self, request, *args, **kwargs):
        user = request.user
        stock_id = request.data.get('stock_id')
        report_file = request.data.get('report_file')

        try:
            if not stock_id:
                raise ValueError("Stock ID is required.")

            stock_report = StockReport.objects.create(user=user, stock_id=stock_id, report_file=report_file)
            StockReportLog.objects.create(user=user, stock_id=stock_id, action='Stock Report Added')
            serializer = StockReportSerializer(stock_report)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as ve:
            return Response({'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, *args, **kwargs):
        user = request.user
        stock_id = request.query_params.get('stock_id')

        try:
            if stock_id:
                reports = StockReport.objects.filter(user=user, stock_id=stock_id)
            else:
                reports = StockReport.objects.filter(user=user)

            serializer = StockReportSerializer(reports, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#DELETE STOCKREPORT
class DeleteStockReportView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, report_id, *args, **kwargs):
        user = request.user
        report = get_object_or_404(StockReport, id=report_id, user=user)

        # Log the deletion action
        StockReportLog.objects.create(user=user, stock_id=report.stock_id, action='Stock Report Deleted')

        report.delete()
        return Response({"message": "Report deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

#TO GET STOCKREPORT
class StockReportLogView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        logs = StockReportLog.objects.filter(user=user)
        serializer = StockReportLogSerializer(logs, many=True)
        return Response(serializer.data)



#TO CREATE GROUPS WITH PERMISSIONS AND ASSIGN USERS TO GROUPS

def is_superuser(user):
    return user.is_superuser
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@user_passes_test(is_superuser)
def create_group(request):
    group_name = request.data.get('group_name')
    permissions = request.data.getlist('permissions')

    if not group_name:
        return Response({'error': 'Group name is required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Create the group or retrieve it if it already exists
    group, created = Group.objects.get_or_create(name=group_name)

    # Assign permissions to the group
    for codename in permissions:
        try:
            permission = Permission.objects.get(codename=codename)
            group.permissions.add(permission)
        except Permission.DoesNotExist:
            return Response({'error': f'Permission with codename "{codename}" does not exist.'},
                            status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': f'Group "{group_name}" created successfully with permissions.'},
                    status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@user_passes_test(is_superuser)
def get_all_groups(request):
    groups = Group.objects.all()

    group_data = []
    for group in groups:
        group_data.append({
            'id': group.id,
            'name': group.name,
            # 'permissions': list(group.permissions.values())
        })

    return Response(group_data, status=status.HTTP_200_OK)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@user_passes_test(is_superuser)
def edit_group(request):
    group_name = request.data.get('group_name')
    permissions = request.data.getlist('permissions')

    if not group_name:
        return Response({'error': 'Group name is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Retrieve the group
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        return Response({'error': f'Group "{group_name}" does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    # Clear existing permissions from the group
    group.permissions.clear()

    # Assign permissions to the group
    for codename in permissions:
        try:
            permission = Permission.objects.get(codename=codename)
            group.permissions.add(permission)
        except Permission.DoesNotExist:
            return Response({'error': f'Permission with codename "{codename}" does not exist.'},
                            status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': f'Permissions for group "{group_name}" updated successfully.'},
                    status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@user_passes_test(is_superuser)
def delete_group(request, group_id):
    try:
        group = Group.objects.get(id=group_id)
        group.delete()
        return Response({'message': f'Group "{group.name}" deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

    except Group.DoesNotExist:
        return Response({'error': 'Group not found.'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
@user_passes_test(is_superuser)
def assign_user_to_group(request):
    username = request.data.get('username')
    group_name = request.data.get('group_name')

    if not username or not group_name:
        return Response({'error': 'Username and group name are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(username=username)
        group = Group.objects.get(name=group_name)

        # Assign the user to the group
        user.groups.add(group)

        return Response({'message': f'User {username} assigned to group {group_name} successfully.'}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    except Group.DoesNotExist:
        return Response({'error': 'Group not found.'}, status=status.HTTP_404_NOT_FOUND)



class BlogViewSet(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        blogs = Blogs.objects.all()
        serializers= BlogSerializer(blogs, many=True)
        return Response(serializers.data)

    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        blog = get_object_or_404(Blogs, pk=pk)
        serializer = BlogSerializer(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        blog = get_object_or_404(Blogs, pk=pk)
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

