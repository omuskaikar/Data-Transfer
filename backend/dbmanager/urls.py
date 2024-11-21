#backend/dbmanager/urls.py
from django.urls import path
from .views import ConnectToPostgres, ConnectToMssql, UploadCsvPostgres,FetchTablesPostgres,FetchTablesMssql,MssqlToPostgres,TransferDataView

urlpatterns = [
    # PostgreSQL Routes
    path('connect-postgres/', ConnectToPostgres.as_view(), name='connect_postgres'),
    path('upload-csv-postgres/', UploadCsvPostgres.as_view(), name='upload_csv_postgres'),
    path('fetch-tables-postgres/', FetchTablesPostgres.as_view(), name='fetch_tables_postgres'),
    # MSSQL Routes
    path('connect-mssql/', ConnectToMssql.as_view(), name='connect_mssql'),
    path('fetch-tables-mssql/', FetchTablesMssql.as_view(), name='fetch_tables_postgres'),
    path('mssql-to-postgres/', MssqlToPostgres.as_view(), name='mssql_to_postgres'),
    path("mh_voters_ac/", TransferDataView.as_view(), name="transfer_data"),
]
