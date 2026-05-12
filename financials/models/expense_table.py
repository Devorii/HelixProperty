from sqlalchemy import Column, String, Integer, Date, Text
from database_ops.db_connection import Base

class ExpenseReports(Base):
    '''ExpenseReport table model'''
    __tablename__= "expenseReports"
    expense_id=Column(Integer, primary_key=True)
    category_id=Column(String(255))
    vendor_id=Column(String(255))
    currency=Column(String(255))
    due_date=Column(Date)
    po_so=Column(String(255))
    bill_num=Column(String(255))
    unit_id=Column(String(255))
    total=Column(String(255))
    subtotal=Column(String(255))
    tax=Column(String(255))
    total_paid=Column(String(255))
    amount_due=Column(String(255))
    unique_id=Column(String(255))


class ExpenseItems(Base):
    '''
    Expense items table model.
    
    This table is used to store the items from within
    a particular report with it's report id point back to 
    expenseReport table.   
    '''
    __tablename__="expense_items"
    items_id=Column(Integer, primary_key=True)
    item=Column(String(255))
    description=Column(Text)
    quantity=Column(Integer)
    price=Column(String(255))
    amount=Column(String(255))
    report_id=Column(String(255))
