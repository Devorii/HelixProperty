# import random
# import openpyxl
# from fastapi import APIRouter, UploadFile, Depends
# from datetime import datetime
# from property_management.reporting_system.email_notifications.update_ticket_notification import UpdateTicket_email_notification
# from property_management.reporting_system.owners.update_tickets_status import update_ticket_status
# from property_management.reporting_system.tenants.close_ticket import close_ticket
# from security.access_control.auth.dependencies.session_control import validate_user_account
# from vendors.models.vendors_model import Vendors
# from database_ops.db_connection import get_db



# vendor_ticket_router = APIRouter(
#     prefix="/vendors",
#     tags=["admin"],
#     responses={404: {"description": "Not found"}}
# )

# @vendor_ticket_router.post('/upload')
# async def upload_vendors(file: UploadFile):
#     '''
#     upload vendors to database
#     :params file:UploadFile
#     '''
#     if not file.filename.endswith(".xlsx"):
#         return {"error": "Only .xlsx files are supported"}
    
#     contents = await file.read()

#     from io import BytesIO
#     workbook = openpyxl.load_workbook(BytesIO(contents))
#     # sheet = workbook.active  # get the first sheet

#     for sheet_name in workbook.sheetnames:  # loop through all sheets
#         sheet = workbook[sheet_name]
#         print(f"Processing sheet: {sheet_name}")
        
#         if sheet_name == 'Flooring Spreadsheet':
#             return 'done'



#         for row in sheet.iter_rows(min_row=2, values_only=True):  # skip header row
#             name = row[0]
#             number = row[1]
#             email = row[2]
#             address = row[3]
#             city = row[4]
#             province = row[5]
#             country = row[6]
#             stars = row[7]

#             if name is not None:
#                 category = {"Plumbing Spreadsheet":"001", "Electrical Spreadsheet":"004"}
#                 street_addr = str(address).split('Windsor')[0].replace(',', '')
#                 rpc = str(address).split('ON')[1:2]
#                 postal_code = rpc[0].strip() if len(rpc) > 0 else "None"

           
#                 rn=''.join([str(random.randint(0,9)) for _ in range(5)])
     
#                 try: 
#                     with get_db() as db:
#                         db.add(Vendors(
#                             name=name, 
#                             category=category[sheet_name], 
#                             street_address=street_addr, 
#                             city="Windsor", 
#                             province="ON", 
#                             country='Canada', 
#                             postal_zip=postal_code,
#                             phone=number,
#                             email='None',
#                             unique_id=rn
#                             ))
#                         db.commit()
                
#                 except Exception as e: 
#                     raise e

            


    


    # class Vendors(Base):
    # '''Vendors table model'''
    # __tablename__= "vendors"
    # idvendors=Column(Integer, primary_key=True)
    # name=Column(String)
    # category=Column(String)
    # street_address=Column(String)
    # city=Column(String)
    # province=Column(String)
    # country=Column(String)
    # postal_zip=Column(String)
    # phone=Column(String)
    # email=Column(String)
    # unique_id=Column(String)