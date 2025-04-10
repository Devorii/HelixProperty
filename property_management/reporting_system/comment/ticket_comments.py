
"""
Module Name: ticket_comment.py
Description: Adds comments to the database.

Author: Decory Herbert
Version: 1.0.x
Date Created: 2023-05-01
Last Modified: 2025-02-12


Dependencies:
    - sqlalchemy >= 2.0.27
"""
from fastapi import HTTPException
from datetime import datetime
from database_ops.db_connection import get_db
from sqlalchemy import select
from property_management.reporting_system.models.ticket_comment import Comments



async def create_ticket_comments(comment_data:dict):
    '''
    Add comments to database
    '''
    try: 
        with get_db() as db:
            db.add(Comments(**comment_data))
            db.commit()
            print('Comment created.')
            return 'Comment created.'
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"failed to add comment - {e}")
    pass


async def get_ticket_comments(query_data:dict):
    '''
    Add comments to database
    '''
    try: 
        output=[]
        with get_db() as db:
            query = select(Comments).where(Comments.property_id == query_data['property_id'], Comments.ticket_id == query_data['ticket_id'])
            tickets_comments=db.execute(query).fetchall()
            for comments in tickets_comments: 
                single_comment=dict(            
                    initials=comments[0].initials,
                    fullname=comments[0].fullname,
                    role=comments[0].role,
                    note=comments[0].notes,
                    date=comments[0].created_date.date().strftime("%Y-%m-%d")
                    )
                output.append(single_comment) 
            return output
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"failed to retrieve comment - {e}")
    pass