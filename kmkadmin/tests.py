from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from .models import Stock
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class AddStockViewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_successful_stock_addition(self):
        url = reverse('addStock')  # Replace this with your actual API URL
        data = {
            'stock_symbol': 'AAPL',
            #'stock_scrip_code': '123',
            'entry_price': 150.0,
            'target_price': 170.0,
            'stock_name': 'Apple Inc.',
            'stock_industry': 'Technology',
            'no_of_shares': 100,
            'stock_exchange': 'NSE',
            'start_date': '2024-03-19',
            'end_date': '2025-03-26',
            'risk': 'Low',
            'tag1': 'Tech',
            'tag2': 'Investment',
            'status': 'Active',
            'action': 'Buy',
            'live_price': 160.0,
            # 'upside_left': 10.0,
            # 'gain_loss': 200.0,
            # 'market_cap': 2000000000,
            # 'expected_returns': 10.0,
            # 'time_left': '1 week'
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')

        # Debugging information
        print("Response status code:", response.status_code)
        print("Response data:", response.data)

        if response.status_code != status.HTTP_201_CREATED:
            print("Validation errors:", response.data.get("error"))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_stock_data(self):
        url = reverse('addStock')
        data = {
            # Omitting required fields intentionally to make the data invalid
            'stock_symbol': 'AAPL',
            'entry_price': 150.0,
            'target_price': 170.0,
            'no_of_shares': 100,
            'stock_exchange': 'NSE',
            'start_date': '2024-03-19',
            'end_date': '2024-03-26',
            'risk': 'Low',
            'status': 'Pending',
            'action': 'Buy',
            'live_price': 160.0,
            'upside_left': 10.0,
            'gain_loss': 200.0,
            'market_cap': 2000000000,


        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')

        # Debugging information
        print("Response status code:", response.status_code)
        print("Response data:", response.data)

        # Assert that the response status code is 400 (Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_stock_symbol(self):
        url = reverse('addStock')
        data = {
            'stock_scrip_code': '123',
            'entry_price': 150.0,
            'target_price': 170.0,
            'stock_name': 'Apple Inc.',
            'stock_industry': 'Technology',
            'no_of_shares': 100,
            'stock_exchange': 'NSE',
            'start_date': '2024-03-19',
            'end_date': '2024-03-26',
            'risk': 'Low',
            'tag1': 'Tech',
            'tag2': 'Investment',
            'status': 'Pending',
            'action': 'Buy',
            'live_price': 160.0,
            'upside_left': 10.0,
            'gain_loss': 200.0,
            'market_cap': 2000000000,
            'expected_returns': 10.0,
            'time_left': '1 week'
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        print(response.data)
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)




class AddNewStockTargetTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.stock = Stock.objects.create(
            stock_symbol='AAPL',
            stock_name='Apple Inc.',
            stock_industry='Technology',
            stock_exchange='NYSE',
            no_of_shares=100,
            risk='Low',

            tag1='Tech',
            tag2='Investment',
            # status: 'Active',
            # action: 'Buy',
            live_price=160.0,
            upside_left=10.0,
            #gain_loss=200.0,
            market_cap=2000000000,
            expected_returns=10.0,
            #time_left='1 week'
        )

    def test_successful_stock_target_addition(self):
        url = reverse('addStockTarget')
        data = {
            'stock_id': self.stock.id,
            'entry_price': 150.0,
            'target_price': 170.0,
            'target_date': '2024-03-26',
            'target_action': 'BUY',
            'target_status': 'Active'
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        print('Response data:', response.data)

        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_incomplete_data_provided(self):
        url = reverse('addStockTarget')
        data = {
            # Omitting required fields intentionally to make the data incomplete
            'entry_price': 150.0,
            'target_price': 170.0,
            'target_date': '2024-03-26',
            'target_action': 'SELL',
            'target_status': 'Pending'
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        print(response.data)
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
 
    def test_invalid_stock_id(self):
        url = reverse('addStockTarget')
        data = {
            'stock_id': 9999,  # Invalid stock ID
            'entry_price': 150.0,
            'target_price': 170.0,
            'target_date': '2024-03-26',
            'target_action': 'Buy',
            'target_status': 'Pending'
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        print(response.data)
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)





#
# class EditStockDataViewTest(APITestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user(username='test_user', email='test@example.com', password='password123')
#         self.client.force_authenticate(user=self.user)
#
#         # Create a sample stock
#         self.stock = Stock.objects.create(
#             stock_name='LIC',
#             stock_exchange='BSE',
#             stock_industry='Fixed Deposits',
#             no_of_shares=100,
#             stock_symbol='LIC',
#             risk='Low',
#             tag1='Tag1',
#             tag2='Tag2'
#         )
#
#     def test_edit_stock_data_success(self):
#         url = reverse('editStockData')
#         data = {
#             'stock_id': (self.stock.id),
#             'stock_name': 'LIC pvt ltd',
#             'stock_exchange': 'BSE',
#             'stock_industry': 'Deposit Industry',
#             'no_of_shares': 200,
#             'stock_symbol': 'UPD',
#             'risk': 'High',
#             'tag1': 'Updated Tag1',
#             'tag2': 'Updated Tag2'
#         }
#         response = self.client.put(url, data, format='json')
#         print(response.data)
#         print(response.status_code)
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['message'], 'Stock data updated successfully')
#
#         # Check if the stock was actually updated
#         updated_stock = Stock.objects.get(id=self.stock.id)
#         self.assertEqual(updated_stock.stock_exchange, 'Updated Exchange')
#         self.assertEqual(updated_stock.stock_industry, 'Updated Industry')
#         self.assertEqual(updated_stock.no_of_shares, 200)
#         self.assertEqual(updated_stock.stock_symbol, 'UPD')
#         self.assertEqual(updated_stock.risk, 'High')
#         self.assertEqual(updated_stock.tag1, 'Updated Tag1')
#         self.assertEqual(updated_stock.tag2, 'Updated Tag2')
#
#     def test_edit_nonexistent_stock(self):
#         url = reverse('editStockData')
#         data = {
#             'stock_id': 99000,# Nonexistent stock ID
#             'stock_name': 'Updated Stock Name',
#             'stock_exchange': 'Updated Exchange',
#             'stock_industry': 'Updated Industry',
#             'no_of_shares': 200,
#             'stock_symbol': 'UPD',
#             'risk': 'High',
#             'tag1': 'Updated Tag1',
#             'tag2': 'Updated Tag2'
#         }
#         response = self.client.put(url, data, format='json')
#         print(response.data)
#         print(response.status_code)
#
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#
#     def test_missing_stock_id(self):
#         url = reverse('editStockData')
#         data = {
#             # Missing stock_id
#             'stock_name': 'Updated Stock Name',
#             'stock_exchange': 'Updated Exchange',
#             'stock_industry': 'Updated Industry',
#             'no_of_shares': 200,
#             'stock_symbol': 'UPD',
#             'risk': 'High',
#             'tag1': 'Updated Tag1',
#             'tag2': 'Updated Tag2'
#         }
#         response = self.client.put(url, data, format='json')
#         print(response.data)
#         print(response.status_code)
#
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)








# class EditStockDataViewTest(APITestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user(username='test_user', password='password123')
#         self.stock = Stock.objects.create(stock_name='Test Stock', no_of_shares=100, stock_symbol='TST')
#
#     def test_edit_stock_data(self):
#         url = reverse('editStockData')
#         request_data = {
#             'stock_id': self.stock.id,
#             'stock_name': 'New Test Stock Name',
#             'stock_exchange': 'BSE',
#             'stock_industry': 'COMMERCIAL',
#
#         }
#
#         response = self.client.put(url, request_data, format='json')
#         # request.user = self.user
#         print(response.data)
#         print(response.status_code)
#
#
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data['message'], 'Stock data updated successfully')
#         self.stock.refresh_from_db()  # Refresh the stock instance from the database
#         self.assertEqual(self.stock.stock_name, 'New Test Stock Name')
#         self.assertEqual(self.stock.stock_exchange, 'BSE')
#         self.assertEqual(self.stock.stock_industry, 'COMMERCIAL')
#
#     def test_edit_non_existing_stock(self):
#         url = reverse('editStockData')
#         request_data = {
#             'stock_id': 999,  # Non-existing stock ID
#             'stock_name': 'New Test Stock Name',
#             'no_of_shares': 150,
#             'stock_symbol': 'NTS',
#
#         }
#
#         response = self.client.put(url, request_data, format='json')
#         #request.user = self.user
#         print(response.data)
#         print(response.status_code)
#
#         self.assertEqual(response.status_code, 404)
#         self.assertEqual(response.data['error'], 'Stock not found')
