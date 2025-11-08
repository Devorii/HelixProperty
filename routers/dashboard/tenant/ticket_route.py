import random
from typing import Optional, Union,List
from typing import Annotated
from datetime import datetime
from property_management.utilities.upload_images import send_files
from fastapi import APIRouter, BackgroundTasks, Depends, File, UploadFile, Form, Request
from property_management.reporting_system.models.request_models import CreateTicket
from property_management.reporting_system.tenants.add_ticket import add_ticket
from property_management.reporting_system.email_notifications.new_ticket_notification import Create_email_notification
from property_management.reporting_system.email_notifications.close_ticket_notification import CloseTicket_email_notification
from property_management.reporting_system.view_tickets import view_tickets
from property_management.reporting_system.tenants.close_ticket import close_ticket
from security.access_control.auth.dependencies.session_control import validate_user_account
from property_management.reporting_system.models.ticket_img_models import TicketsImgUrl
from property_management.reporting_system.tenants.add_ticket_imgs import add_ticket_imgs


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
async def create_issue_report(    
    category: str = Form(...),  # Accept individual form fields for CreateTicket
    title: str = Form(...),
    description: str = Form(...),
    author: str = Form(...),
    author_id: int = Form(...),
    property_id: str = Form(...), 
    images:List[UploadFile] = File(None), 
    request:Request=Request,
    backgroundtasks:BackgroundTasks=BackgroundTasks, 
    session:str=Depends(validate_user_account)) -> str:
    '''
    Creates ticket for tenants

    :params CreateTicket: ticket_info
    :return str
    '''
    groomed_files = List[images] if not isinstance(images, List) else images

    ticket_i = {
    'category': category,
    'title': title,
    'description': description,
    'author': author,
    'author_id': author_id,
    'property_id': property_id,
    'created_date': datetime.now().strftime('%Y-%m-%d'),
    'status': 'Open',
    'ticket_num': random.randint(10000, 99999)
    }

    current_date = datetime.now() 
    email_ls= await add_ticket(ticket_i)
      
    if groomed_files is not List[None]:
        get_image_urls=await send_files(groomed_files, ticket_i['ticket_num'], request.app.state.bucket)
        for img_url in get_image_urls:
            img_metadata=dict(
                property_id=ticket_i['property_id'],
                ticket_number=ticket_i['ticket_num'],
                images_url=img_url,
                created_on=current_date.strftime('%Y-%m-%d')
                )
            await add_ticket_imgs(img_metadata)

    artifacts=dict(
        username=ticket_i['author'], 
        email=email_ls, 
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
    email_list= await close_ticket(ticket_information)

    artifacts=dict(
    username=ticket_information['author'], 
    email=email_list, 
    ticket_num=ticket_information['ticket_num'], 
    issue=ticket_information['title'],
    date=current_date.strftime('%Y-%m-%d')
    )

    ready_email=CloseTicket_email_notification(artifacts)
    backgroundtasks.add_task(ready_email.send_mail)
    return 'Ticket Closed'


