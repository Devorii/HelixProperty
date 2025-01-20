import random
from fastapi import APIRouter, BackgroundTasks, Depends
from datetime import datetime
from property_management.reporting_system.models.request_models import CreateTicket
from property_management.reporting_system.tenants.add_ticket import add_ticket
from property_management.reporting_system.email_notifications.new_ticket_notification import Create_email_notification
from property_management.reporting_system.email_notifications.close_ticket_notification import CloseTicket_email_notification
from property_management.reporting_system.view_tickets import view_tickets
from property_management.reporting_system.tenants.close_ticket import close_ticket
from security.access_control.auth.dependencies.session_control import validate_user_account


ticket_router = APIRouter(
    prefix="/support",
    tags=["admin"],
    responses={404: {"description": "Not found"}}
)

@ticket_router.post('/all-tickets')
async def view_tickets_info(payload:dict, session:str=Depends(validate_user_account)):
    '''
    Shows available tickets to the users
    :params dict:property_id
    '''
    # return testing
    # id, issue, date, category, status, created_by

    return await view_tickets(payload)


@ticket_router.post('/create-ticket')
async def create_issue_report(ticket_info: CreateTicket, backgroundtasks:BackgroundTasks=BackgroundTasks, session:str=Depends(validate_user_account)) -> str:
    '''
    Creates ticket for tenants

    :params CreateTicket: ticket_info
    :return str
    '''
    current_date = datetime.now() 
    ticket_i = ticket_info.dict() 
    ticket_i['created_date'] = current_date.strftime('%Y-%m-%d') 
    ticket_i['status']='Open'
    create_hash=random.randint(10000, 99999)
    ticket_i['ticket_num']=create_hash
    owner_management_email= await add_ticket(ticket_i)

    artifacts=dict(
        username=ticket_i['author'], 
        email=owner_management_email, 
        message=ticket_i['description'], 
        ticket_num=ticket_i['ticket_num'], 
        issue=ticket_i['title'],
        date=current_date.strftime('%Y-%m-%d')
        )

    ready=Create_email_notification(artifacts)
    backgroundtasks.add_task(ready.send_mail)
    return 'Ticket created'


@ticket_router.post('/close-ticket')
async def view_tickets_info(ticket_information:dict, backgroundtasks:BackgroundTasks, session:str=Depends(validate_user_account)):
    '''
    Closes selected ticket
    :params dict:ticket_information
    '''
    current_date = datetime.now() 
    management_email= await close_ticket(ticket_information)

    artifacts=dict(
    username=ticket_information['author'], 
    email=management_email, 
    ticket_num=ticket_information['ticket_num'], 
    issue=ticket_information['title'],
    date=current_date.strftime('%Y-%m-%d')
    )

    ready_email=CloseTicket_email_notification(artifacts)
    backgroundtasks.add_task(ready_email.send_mail)
    return management_email