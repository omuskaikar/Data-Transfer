#backend/dbmanager/views.py
import os
import psycopg2
import pyodbc  # For MSSQL
import pandas as pd
import traceback
from rest_framework.views import APIView
from concurrent.futures import ThreadPoolExecutor
import logging
from rest_framework.response import Response
from rest_framework import status
import traceback
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .serializers import DbConnectionSerializer
import csv

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# PostgreSQL Connection
class ConnectToPostgres(APIView):
    def post(self, request):
        serializer = DbConnectionSerializer(data=request.data)
        if serializer.is_valid():
            ip_address = serializer.validated_data['host']
            user = serializer.validated_data['user']
            password = serializer.validated_data['password']
            try:
                # Connect to PostgreSQL without specifying a database
                connection = psycopg2.connect(
                    host=ip_address,
                    user=user,
                    password=password,
                    dbname="postgres"  # Connect to the default 'postgres' database
                )
                cursor = connection.cursor()
                cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
                databases = cursor.fetchall()
                db_list = [db[0] for db in databases]
                cursor.close()
                connection.close()
                return Response({'status': 'success', 'databases': db_list}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# MSSQL Connection
class ConnectToMssql(APIView):
    def post(self, request):
        serializer = DbConnectionSerializer(data=request.data)
        if serializer.is_valid():
            ip_address = serializer.validated_data['host']
            user = serializer.validated_data['user']
            password = serializer.validated_data['password']
            try:
                # Connect to MSSQL without specifying a database
                connection_string = f'DRIVER={{SQL Server}};SERVER={ip_address};UID={user};PWD={password}'
                connection = pyodbc.connect(connection_string)
                cursor = connection.cursor()
                cursor.execute("SELECT name FROM sys.databases WHERE name NOT IN ('master', 'tempdb', 'model', 'msdb');")
                databases = cursor.fetchall()
                db_list = [db[0] for db in databases]
                cursor.close()
                connection.close()
                return Response({'status': 'success', 'databases': db_list}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# File Upload for PostgreSQL (Same as your existing UploadCsv)
class UploadCsvPostgres(APIView):
    def post(self, request):
        table_name = request.data.get('table_name')
        csv_file = request.FILES.get('file')
        ip_address = request.data.get('host')
        db_name = request.data.get('dbname')
        user = request.data.get('user')
        password = request.data.get('password')

        if not csv_file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        if not table_name:
            return Response({'error': 'No table name provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Save the CSV file temporarily
            temp_dir = settings.TEMP_FILE_DIR
            fs = FileSystemStorage(location=temp_dir)
            filename = fs.save(csv_file.name, csv_file)
            file_path = os.path.join(temp_dir, filename)

            # Connect to PostgreSQL
            connection = psycopg2.connect(
                host=ip_address,
                database=db_name,
                user=user,
                password=password
            )
            cursor = connection.cursor()

            # Use PostgreSQL's COPY command to bulk load the CSV into the specified table
            with open(file_path, 'r', encoding='utf-8') as f:
                cursor.copy_expert(f"COPY {table_name} FROM STDIN WITH CSV HEADER NULL AS 'NULL'", f)
                connection.commit()

            cursor.close()
            connection.close()

            # Remove the temporary CSV file
            if os.path.exists(file_path):
                os.remove(file_path)

            return Response({'status': 'success', 'message': 'CSV uploaded and data inserted successfully'}, status=status.HTTP_200_OK)

        except Exception as e:
            # Capture the full traceback and print it for debugging
            error_traceback = traceback.format_exc()  # Get the full error traceback
            print(error_traceback)  # Print to console for debugging

            # Return the exact error in the response (optionally with less detail for security reasons)
            return Response({
                'status': 'error',
                'message': str(e),  # Error message only
                'details': error_traceback  # Full traceback (optional for debugging)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# File Upload for MSSQL
class UploadCsvMssql(APIView):
    def post(self, request):
        table_name = request.data.get('table_name')
        csv_file = request.FILES.get('file')
        ip_address = request.data.get('ip')
        db_name = request.data.get('dbname')
        user = request.data.get('user')
        password = request.data.get('password')

        if not csv_file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        if not table_name:
            return Response({'error': 'No table name provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            temp_dir = settings.TEMP_FILE_DIR
            fs = FileSystemStorage(location=temp_dir)
            filename = fs.save(csv_file.name, csv_file)
            file_path = os.path.join(temp_dir, filename)
            df = pd.read_csv(file_path)

            # Connect to the selected MSSQL database
            connection_string = f'DRIVER={{SQL Server}};SERVER={ip_address};DATABASE={db_name};UID={user};PWD={password}'
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()


            columns = df.columns.tolist()
            placeholders = ', '.join(['?'] * len(columns))
            columns_str = ', '.join(columns)
            insert_query = f'INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})'

            for row in df.itertuples(index=False, name=None):
                cursor.execute(insert_query, row)

            connection.commit()
            cursor.close()
            connection.close()

            if os.path.exists(file_path):
                os.remove(file_path)

            return Response({'status': 'success', 'message': 'CSV uploaded successfully'}, status=status.HTTP_200_OK)

        except pd.errors.EmptyDataError:
            return Response({'status': 'error', 'message': 'CSV file is empty or invalid'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)},  status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class FetchTablesPostgres(APIView):
    def post(self, request):
        host = request.data.get('host')
        user = request.data.get('user')
        password = request.data.get('password')
        db_name = request.data.get('dbName')

        try:
            # Connect to the specified PostgreSQL database
            connection = psycopg2.connect(
                host=host,
                database=db_name,
                user=user,
                password=password
            )
            cursor = connection.cursor()
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'    AND table_type = 'BASE TABLE'  AND table_name NOT IN (SELECT inhrelid::regclass::text FROM pg_inherits);")
            tables = cursor.fetchall()
            table_list = [table[0] for table in tables]
            cursor.close()
            connection.close()

            return Response({'status': 'success', 'tables': table_list}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                            
class FetchTablesMssql(APIView):
    def post(self, request):
        host = request.data.get('host')
        user = request.data.get('user')
        password = request.data.get('password')
        db_name = request.data.get('dbName')

        try:
            # Connect to the specified MSSQL database
            connection_string = f'DRIVER={{SQL Server}};SERVER={host};DATABASE={db_name};UID={user};PWD={password}'
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            # Fetch table names from the specified database using INFORMATION_SCHEMA
            cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE';")
            tables = cursor.fetchall()

            # Extract table names
            table_list = [table[0] for table in tables]

            # Close the connection
            cursor.close()
            connection.close()

            # Return the list of tables
            return Response({'status': 'success', 'tables': table_list}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



class MssqlToPostgres(APIView):
    def post(self, request):
        # Get connection details and table names from request data
        mssql_details = {
            'host': request.data.get('mssql_host'),
            'user': request.data.get('mssql_user'),
            'password': request.data.get('mssql_password'),
            'db_name': request.data.get('mssql_dbname'),
            'table_name': request.data.get('mssql_table')  # Now we're dynamically choosing table
        }

        postgres_details = {
            'host': request.data.get('postgres_host'),
            'user': request.data.get('postgres_user'),
            'password': request.data.get('postgres_password'),
            'db_name': request.data.get('postgres_dbname'),
            'table_name': request.data.get('postgres_table')
        }

        acno = request.data.get('acno')  # Get acno value (can be 'ALL')
        batch_size = 1000
        max_workers = min(10, os.cpu_count() * 2)

        def establish_connections():
            """Establish connections to SQL Server and PostgreSQL."""
            # Construct SQL Server connection string
            mssql_connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={mssql_details["host"]};DATABASE={mssql_details["db_name"]};UID={mssql_details["user"]};PWD={mssql_details["password"]}'
            mssql_connection = pyodbc.connect(mssql_connection_string)
            mssql_cursor = mssql_connection.cursor()

            # Construct PostgreSQL connection string
            pg_conn = psycopg2.connect(
                host=postgres_details['host'],
                database=postgres_details['db_name'],
                user=postgres_details['user'],
                password=postgres_details['password']
            )
            pg_cursor = pg_conn.cursor()

            return mssql_connection, mssql_cursor, pg_conn, pg_cursor

        def close_connections(mssql_conn, mssql_cursor, pg_conn, pg_cursor):
            """Close the connections to SQL Server and PostgreSQL."""
            mssql_cursor.close()
            pg_cursor.close()
            mssql_conn.close()
            pg_conn.close()

        def fetch_sql_server_data(sql_cursor, ac_no, table_name):
            """Fetch data from SQL Server based on the table name and AC_No."""
            # Define SQL queries for different tables
            if table_name == 'assembly_master':
                sql_query = f"SELECT * FROM {mssql_details['table_name']} WHERE ac_no = ?" if ac_no != 'ALL' else f"SELECT * FROM {mssql_details['table_name']}"
            elif table_name == 'booth_master':
                sql_query = f"""
                    SELECT [ac_no], 
                    [district_id], 
                    [booth_uid], 
                    [booth_id], 
                    [booth_name_eng], 
                    [booth_name_mar], 
                    [matdan_kendra_id], 
                    [total_voter_count]
                    FROM {mssql_details['table_name']} WHERE ac_no = ?
                """ if ac_no != 'ALL' else f"SELECT * FROM {mssql_details['table_name']}"
            elif table_name == 'list_master':
                sql_query = f"""
                    SELECT [ac_no], [district_id], [list_no], [list_name_eng], [list_name_mar], [booth_id], [list_link], [main_village], [total_voter_count]
                    FROM {mssql_details['table_name']} WHERE ac_no = ?
                """ if ac_no != 'ALL' else f"SELECT * FROM {mssql_details['table_name']}"
            elif table_name == 'pc_master':
                sql_query = f"""
                    SELECT [pc_no], [pc_name_eng], [pc_name_mar], [ac_no], [district_id]
                    FROM {mssql_details['table_name']} WHERE ac_no = ?
                """ if ac_no != 'ALL' else f"SELECT * FROM {mssql_details['table_name']}"
            elif table_name == 'matdan_kendra_master':
                sql_query = f"""
                    SELECT [matdan_kendra_id]
                        ,[kendra_name]
                        ,[kendra_name_mar]
                        ,[area_name]
                        ,[ac_no]
                        ,[area_name_mar]
                        ,[total_voter_count]
                    FROM {mssql_details['table_name']} WHERE ac_no = ?
                """ if ac_no != 'ALL' else f"SELECT * FROM {mssql_details['table_name']}"
            elif table_name == 'sublocation_master':
                sql_query = f"""
                    SELECT  [subloc_cd]
                            ,[ac_no]
                            ,[list_no]
                            ,[sublocation_no]
                            ,[society_name]
                            ,[society_name_mar]
                            ,[city_cd]
                            ,[city]
                            ,[city_m]
                            ,[pincode]
                            ,[old_list_no]
                            ,[tahsil_no]
                           ,[subloc_id]
                    FROM {mssql_details['table_name']} WHERE ac_no = ?
                """ if ac_no != 'ALL' else f"""SELECT [subloc_cd]
                            ,[ac_no]
                            ,[list_no]
                            ,[sublocation_no]
                            ,[society_name]
                            ,[society_name_mar]
                            ,[city_cd]
                            ,[city]
                            ,[city_m]
                            ,[pincode]
                            ,[old_list_no]
                            ,[tahsil_no]
                           ,[subloc_id] FROM {mssql_details['table_name']}"""
            else:
                raise ValueError(f"Unsupported table: {table_name}")

            sql_cursor.execute(sql_query, (acno,) if acno != 'ALL' else ())
            columns = [column[0] for column in sql_cursor.description]
            return columns
        
        
        def process_batch(batch, columns, pg_cursor, pg_conn, table_name, file_idx):
            """Process and insert a batch of data into PostgreSQL via CSV."""
            # Clean the batch by removing any null characters
            cleaned_batch = [
                [value.replace('\x00', '') if isinstance(value, str) else value for value in row]
                for row in batch
            ]
            # Define the file path for the CSV file
            csv_filename = f'csv_batches/batch_{file_idx}.csv'

            # Ensure the directory exists
            os.makedirs('csv_batches', exist_ok=True)

            # Write the cleaned batch data to a CSV file
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(columns)  # Write the column headers
                writer.writerows(cleaned_batch)  # Write the data rows

            logging.info(f"Batch {file_idx} written to CSV: {csv_filename}")

            # Load the CSV data into PostgreSQL using the COPY command
            try:
                with open(csv_filename, 'r', encoding='utf-8') as csvfile:
                    pg_cursor.copy_expert(
                        f"""
                        COPY {table_name} ({', '.join(columns)})
                        FROM STDIN WITH CSV HEADER
                        """,
                        csvfile
                    )
                pg_conn.commit()
                logging.info(f"Batch {file_idx} loaded into PostgreSQL")
            except Exception as e:
                logging.error(f"Error processing batch {file_idx}: {e}")
                pg_conn.rollback()
            finally:
                # Ensure the CSV file is removed after processing, regardless of success or failure
                if os.path.exists(csv_filename):
                    os.remove(csv_filename)
                    logging.info(f"CSV file {csv_filename} deleted after processing")
        try:
            # Establish connections
            mssql_conn, mssql_cursor, pg_conn, pg_cursor = establish_connections()
            # -----PUSH FULL AC (ALL)--------------------
            if acno == 'ALL':
                # Check if records already exist in PostgreSQL
                pg_cursor.execute(f"SELECT COUNT(*) FROM public.{postgres_details['table_name']}")
                if pg_cursor.fetchone()[0] > 0:
                    logging.info("Records exist. Deleting and reinserting...")
                    # Truncate the PostgreSQL table before inserting new data
                    pg_cursor.execute(f"TRUNCATE TABLE {postgres_details['table_name']}")
                    pg_conn.commit()

                # Fetch all data from SQL Server
                columns = fetch_sql_server_data(mssql_cursor, 'ALL', mssql_details['table_name'])
            # -----PUSH 1 AC-------------------
            else:
                # Check if records already exist in PostgreSQL for the specific acno
                pg_cursor.execute(f"SELECT COUNT(*) FROM public.{postgres_details['table_name']} WHERE ac_no = %s", (acno,))
                if pg_cursor.fetchone()[0] > 0:
                    logging.info(f"Records for ac_no {acno} exist. Deleting and reinserting...")
                    # Delete rows where ac_no matches the given value
                    pg_cursor.execute(f"DELETE FROM public.{postgres_details['table_name']} WHERE ac_no = %s", (acno,))
                    pg_conn.commit()

                # Fetch data for the specific acno from SQL Server
                columns = fetch_sql_server_data(mssql_cursor, acno, mssql_details['table_name'])

            # Use ThreadPoolExecutor for batch processing
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                file_idx = 0
                while True:
                    batch = mssql_cursor.fetchmany(batch_size)
                    if not batch:
                        break
                    executor.submit(process_batch, batch, columns, pg_cursor, pg_conn, postgres_details['table_name'], file_idx)
                    file_idx += 1
            logging.info("Data successfully transferred from MSSQL to PostgreSQL.")
            return Response({'status': 'success', 'message': 'Data transferred successfully'}, status=status.HTTP_200_OK)

        except Exception as e:
            logging.error(f"Error during execution: {e}")
            print(traceback.format_exc())  # Log the exact error
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            # Close the connections
            close_connections(mssql_conn, mssql_cursor, pg_conn, pg_cursor)
     

