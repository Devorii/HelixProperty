
from datetime import datetime
from fastapi import APIRouter, Depends
from security.access_control.auth.dependencies.session_control import validate_user_account
from property_management.reporting_system.comment.ticket_comments import get_ticket_comments, create_ticket_comments
from property_management.reporting_system.email_notifications.reopen_ticket_notification import ReOpenTicket_email_notification

comment_router = APIRouter(
    prefix="/comment",
    tags=["comment"],
    responses={404: {"description": "Not found"}}
)



@comment_router.post('/create-comment')
async def create_comment(payload:dict, session:str=Depends(validate_user_account)):
    '''
    create comments

    :params dict:payload
    :params str:session

    :return str
    '''
    date=datetime.now()


    data=dict(
        fullname=payload['fullname'],
        initials=payload['initials'],
        property_id=payload['property_id'],
        ticket_id=payload['ticket_id'],
        created_date=date.strftime('%Y-%m-%d'),
        role=payload['role'],
        notes=payload['notes']
    )

    await create_ticket_comments(data)
    return f"{payload}"


@comment_router.post('/retrieve-comments')
async def get_comment(payload:dict, session:str=Depends(validate_user_account)):
    '''
    get comments

    :params dict:payload
    :params str:session

    :return str
    '''
    data=dict(
       property_id=payload['property_id'],
        ticket_id=payload['ticket_id'],
        )

    comments=await get_ticket_comments(data)
    return comments