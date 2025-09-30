"""
Module Name: expense report.py
Description: handles the expense report data injection and viewing.

Author: Decory Herbert
Version: 1.0.x
Date Created: 2023-08-29
Last Modified: 2024-12-12


Dependencies:
    - sqlalchemy >= 2.0.27
"""
import string
import random
from fastapi import HTTPException
from database_ops.db_connection import get_db
from financials.models.expense_table import ExpenseReports, ExpenseItems
from financials.models.requests.requests_models import ItemsModel
from models.category import Categories
from vendors.models.vendors_model import Vendors
from typing import List, Dict
from sqlalchemy import select, delete
from vendors.models.vendors_model import Vendors
from property_management.models.properties_table import Properties



class ExpensesReport():

    @staticmethod
    async def delete_expense_report(report_id:str) -> str:
        '''
        Removes expense report based on id.
        '''
        try: 
            with get_db() as db:
                delete_items=delete(ExpenseItems).where(ExpenseItems.report_id==report_id)
                delete_report=delete(ExpenseReports).where(ExpenseReports.unique_id==report_id)
                db.execute(delete_items)
                db.execute(delete_report)
                db.commit()

            return "Report has been removed."
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"There was a problem deleting reports - {e}")


    @staticmethod
    async def get_expense_reports() -> List[Dict]:
        '''
        Gets the expense report from the database.
        '''

        try:
            with get_db() as db:
                items_query = db.query(ExpenseItems).all()
                reports_query = db.query(ExpenseReports).all()

                
                items_by_report = {}

                for row in items_query:
                    item_dict = dict(
                        items_id=row.items_id,
                        item=row.item,
                        description=row.description,
                        quantity=row.quantity,
                        price=row.price,
                        amount=row.amount,
                        report_id=row.report_id,
                    )
                    items_by_report.setdefault(row.report_id, []).append(item_dict)

                output=[]
                for row in reports_query:
                    vendors = db.query(Vendors).filter(Vendors.unique_id==row.vendor_id).first()
                    categories_name = db.query(Categories.name).filter(Categories.unique_id==row.category_id).first()
                    report_dict={
                    "expense_id": row.expense_id,
                    "category_id": str(categories_name[0]),
                    "vendor_id": str(vendors.name),
                    "vendor_street_addess": vendors.street_address,
                    "vendor_city": vendors.city,
                    "vendor_province": vendors.province,
                    "vendor_country": vendors.country,
                    "vendor_postal_code": vendors.postal_zip,
                    "vendor_phone": vendors.phone,
                    "vendor_email": vendors.email,
                    "currency": row.currency,
                    "due_date": row.due_date,
                    "po_so": row.po_so,
                    "bill_num": row.bill_num,
                    "unit_id": row.unit_id,
                    "total": row.total,
                    "subtotal": row.subtotal,
                    "tax": row.tax,
                    "total_paid": row.total_paid,
                    "amount_due": row.amount_due,
                    "unique_id": row.unique_id,
                    "items": items_by_report.get(str(row.unique_id), []),
                    }
                    output.append(report_dict)


            return output 
        except Exception as e: 
            raise HTTPException(status_code=500, detail=e)


    @staticmethod
    async def inject_items(items:List[ItemsModel], report_id:int):
            try: 
                for item in items:
                    with get_db() as db:
                        new_data=ExpenseItems(
                            item=item['item'],
                            description=item['description'],
                            quantity=int(item['quantity']),
                            price=str(item['price']),
                            amount=str(item['amount']),
                            report_id=str(report_id)

                        )
                        db.add(new_data)
                        db.commit()
                return "Item added successfully."
            except Exception as e: 
                raise HTTPException(status_code=500, detail=f"failed to add expense data - {e}")

    
    @staticmethod
    async def add_expense_report(data:dict) -> dict:
        ''' 
        Stores expense information in our database.
        '''
 
        unique_id=random.randint(10000, 99999)

        groomed_data=dict(
            category_id=data.category,
            vendor_id=data.vendor,
            currency=data.currency,
            due_date=data.dueDate,
            po_so=data.posoNumber,
            bill_num=data.billNumber,
            unit_id=data.propID,
            total=data.calculations["total"],
            subtotal=data.calculations["subtotal"],
            tax=data.calculations["taxPercent"],
            total_paid=data.calculations["totalPaid"],
            amount_due=data.calculations["amountDue"],
            unique_id=unique_id
        )

        await ExpensesReport.inject_items(data.items, unique_id)
        try: 
            with get_db() as db:
                db.add(ExpenseReports(**groomed_data))
                db.commit()
            return dict(status_code=200, details='Report successfully submitted.')
        except Exception as e: 
            raise HTTPException(status_code=400, detail=f"failed to add expense data - {e}")

    @staticmethod
    async def send_attributes(property_id:str) -> dict: 
        '''
        returns dict
        '''

       
        try: 
            with get_db() as db:
                get_property_location=db.query(Properties.city).filter(Properties.property_code==property_id).first()
                print(get_property_location)
                get_vendors=db.query(Vendors).filter(Vendors.city==string.capwords(get_property_location[0])).all()
                get_categories=db.query(Categories).all()


                output=[]
                map_category_pos=dict()
                categories=dict()

                for row in get_categories:
                    categories[row.unique_id] = {
                        "id": row.unique_id,
                        "name": row.name,
                        "vendors": []
                    }

                # attach vendors to their category
                for vendor in get_vendors:
                    if vendor.category not in map_category_pos:
                        categories[vendor.category]['vendors'].append({
                            "id": vendor.unique_id,
                            "name": vendor.name
                        })
                        output.append(categories[vendor.category])
                        map_category_pos[vendor.category]=len(map_category_pos)
                    else: 
                        output[map_category_pos[vendor.category]]['vendors'].append({
                            "id": vendor.unique_id,
                            "name": vendor.name
                        })
                
            return dict(status_code=200, categories=output, currency={"id":'416', "iso":'CAN'})
        except Exception as e: 
            raise HTTPException(status_code=400, detail=f"failed to add expense data - {e}")
        pass 
