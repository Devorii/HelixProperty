from sqlalchemy import Column, String, Integer, Date, Text
from sqlalchemy.ext.declarative import declarative_base



Base = declarative_base()

class ExpenseReports(Base):
    '''ExpenseReport table model'''
    __tablename__= "expenseReports"
    expense_id=Column(Integer, primary_key=True)
    category_id=Column(String)
    vendor_id=Column(String)
    currency=Column(String)
    due_date=Column(Date)
    po_so=Column(String)
    bill_num=Column(String)
    unit_id=Column(String)
    total=Column(String)
    subtotal=Column(String)
    tax=Column(String)
    total_paid=Column(String)
    amount_due=Column(String)
    unique_id=Column(String)


class ExpenseItems(Base):
    '''
    Expense items table model.
    
    This table is used to store the items from within
    a particular report with it's report id point back to 
    expenseReport table.   
    '''
    __tablename__="expense_items"
    items_id=Column(Integer, primary_key=True)
    item=Column(String)
    description=Column(Text)
    quantity=Column(Integer)
    price=Column(String)
    amount=Column(String)
    report_id=Column(String)
