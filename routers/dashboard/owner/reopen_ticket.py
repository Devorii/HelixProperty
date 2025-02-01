
from datetime import datetime
from fastapi import APIRouter, Depends, BackgroundTasks
from security.access_control.auth.dependencies.session_control import validate_user_account
from property_management.reporting_system.owners.reopen_tickets_status import reopen_ticket_status
from property_management.reporting_system.email_notifications.reopen_ticket_notification import ReOpenTicket_email_notification

reopen_ticket_router = APIRouter(
    prefix="/closed_ticket",
    tags=["closed_ticket"],
    responses={404: {"description": "Not found"}}
)



@reopen_ticket_router.post('/re-open-ticket')
async def reopen_ticket(payload:dict, backgroundtasks:BackgroundTasks, session:str=Depends(validate_user_account)):
    '''
    For owners only
    Reopens closed tickets.

    :params dict:payload
    :params str:session

    :return str
    '''

    current_date = datetime.now() 
    list_of_owners=await reopen_ticket_status(payload)

    artifacts=dict(
    username=payload['author'], 
    email=list_of_owners, 
    ticket_num=payload['ticket_num'], 
    issue=payload['title'],
    date=current_date.strftime('%Y-%m-%d'),
    status="Open"
    )



    ready_mail=ReOpenTicket_email_notification(artifacts)
    backgroundtasks.add_task(ready_mail.send_mail)

    return f"Ticket {payload['ticket_num']} has been re-opened"