
import random
from fastapi import APIRouter, BackgroundTasks, Depends
from datetime import datetime
from property_management.reporting_system.email_notifications.update_ticket_notification import UpdateTicket_email_notification
from property_management.reporting_system.owners.update_tickets_status import update_ticket_status
from property_management.reporting_system.tenants.close_ticket import close_ticket
from security.access_control.auth.dependencies.session_control import validate_user_account


mngm_ticket_router = APIRouter(
    prefix="/management",
    tags=["admin"],
    responses={404: {"description": "Not found"}}
)

@mngm_ticket_router.post('/update-ticket')
async def update_tickets_info(ticket_information:dict, backgroundtasks:BackgroundTasks, session:str=Depends(validate_user_account)):
    '''
    Closes selected ticket
    :params dict:ticket_information
    '''
    current_date = datetime.now() 
    management_email= await update_ticket_status(ticket_information)

    artifacts=dict(
    username=ticket_information['author'], 
    email=management_email, 
    ticket_num=ticket_information['ticket_num'], 
    issue=ticket_information['title'],
    date=current_date.strftime('%Y-%m-%d'),
    status=ticket_information['status']
    )

    ready_email=UpdateTicket_email_notification(artifacts)
    backgroundtasks.add_task(ready_email.send_mail)
    return 'status updated'