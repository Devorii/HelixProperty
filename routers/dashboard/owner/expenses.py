
from datetime import datetime
from fastapi import APIRouter, Depends, BackgroundTasks
from security.access_control.auth.dependencies.session_control import validate_user_account
from property_management.contacts.contacts import get_tenants_information, delete_tenants_information
from models.request import expense_payload
from financials.databse_operations.expense_report import ExpensesReport



expense_router = APIRouter(
    prefix="/expense",
    tags=["expense"],
    responses={404: {"description": "Not found"}}
)



@expense_router.post('/insert-report')
async def create_comment(payload:expense_payload, backgroundtasks:BackgroundTasks, session:str=Depends(validate_user_account)):
    '''
    :params expense_payload payload

    insert expense for the property
    '''
    backgroundtasks.add_task(ExpensesReport.add_expense_report, payload)
    return dict(status_code=200, details='Expense report data is stored.')
    
@expense_router.post('/get-expense-attributes')
async def get_expense_attributes(prop_id:dict, session:str=Depends(validate_user_account)):
    '''
    Returns all of the attributes needed to create a new expense report.

    :return dict
    '''
    # return 
    # Category, vendors and currency
    return await ExpensesReport.send_attributes(prop_id['prop_id'])





@expense_router.get('/get-expense-reports')
async def get_expense_reports(session:str=Depends(validate_user_account)):
    ''' 
    Provides the expense report information. 
    '''
    return await ExpensesReport.get_expense_reports()

@expense_router.delete('/delete-expense')
async def delete_expense_reports(report_id:dict, session:str=Depends(validate_user_account)):
    '''
    :params str report_id
    Deletes reports based on provided id.
    '''
    return await ExpensesReport.delete_expense_report(report_id.get('report_id'))