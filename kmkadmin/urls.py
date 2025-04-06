from django.urls import path, include
from .views import *
from .views import StockReportView


urlpatterns = [
    
    # All DATA
    path('getAllStocks/', AllStocksView.as_view(), name='getAllStocks'),
    
    # create new instances of stocks and stockTargets
	path('addStock/', AddStockView.as_view(), name='addStock'),
	path('addStockTarget/', AddNewStockTarget.as_view(), name='addStockTarget'),

	#TO VIEW USER INSTANCE WHENEVER USER PERFORMS ANY ACTION ON A STOCK
	path('stock_log/', StockLogListView.as_view(), name='stock_log_list'),
 
	# edit the data in the stocks 
	path('editStockData/', EditStockData.as_view(), name='editStockData'),
 
	# delete Stocks and its targets
	path('deleteStock/' , DeleteStockView.as_view(), name='deleteStock'),
 
 
	#To delete all the data from the database
	path('deleteAllData/' , DeleteAllDataView.as_view(), name='deleteAllData'),


    #TO VIEW AND UPLOAD STOCK REPORT
    path('stock-report/', StockReportView.as_view(), name='stock_report'),
	# TO DELETE REPORT
	path('stock-reports/<int:report_id>/delete/', DeleteStockReportView.as_view(), name='delete-stock-report'),

	#TO VIEW USER INSTANCES FOR STOCKREPORT
    path('stock-report-logs/', StockReportLogView.as_view(), name='stock-report-logs'),


#Group Creation with Permissions and Assign Users to Group
     path('get_group/', get_all_groups, name='get_groups'),
	 path('create_group/', create_group, name='create_group'),
	 path('delete_group/<int:group_id>/' ,delete_group, name='delete_groups'),
	 path('assign_user_to_group/', assign_user_to_group, name='assign_user_to_group'),

	#CRUD in BLOGS
	 path('blog/', BlogViewSet.as_view(), name='blogs'),
	 path('blog/<int:pk>/', BlogViewSet.as_view(), name='blogs'),
]
