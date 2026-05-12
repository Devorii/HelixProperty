

from datetime import datetime
from fastapi import HTTPException
from database_ops.db_connection import get_db
from property_management.reporting_system.models.triage_tickets import Triage_tickets
from vendors.models.vendors_model import Vendors, FavoriteVendors
from sqlalchemy import select


def format_phone_number(phone: str) -> str:
    """
    Format phone number to (XXX) XXX-XXXX format
    :param phone: Phone number string (digits only or with existing formatting)
    :return: Formatted phone number
    """
    # Remove any non-digit characters
    digits = ''.join(filter(str.isdigit, phone)) if phone else ""
    
    # Format as (XXX) XXX-XXXX if we have at least 10 digits
    if len(digits) >= 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:10]}"
    return phone


def vendor_to_geojson_feature(vendor) -> dict:
    """
    Convert a Vendors database object to GeoJSON Feature format
    :param vendor: Vendors object from database
    :return: GeoJSON Feature object
    """
    phone = vendor.phone or ""
    phone_formatted = format_phone_number(phone)
    
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [float(vendor.long), float(vendor.lat)] if vendor.long and vendor.lat else [0, 0]
        },
        "properties": {
            "id": str(vendor.unique_id),
            "name": vendor.name or "",
            "phoneFormatted": phone_formatted,
            "phone": ''.join(filter(str.isdigit, phone)),
            "address": vendor.street_address or "",
            "city": vendor.city or "",
            "country": vendor.country or "",
            "postalCode": vendor.postal_zip or "",
            "state": vendor.province or "",
            "category": vendor.category or ""
        }
    }




class Vendor:

    @staticmethod
    async def update_vendor_favorite(data:dict):
        '''
        Closes selected ticket
        :params dict:ticket_information
        '''
        current_date = datetime.now() 

        try: 
            with get_db() as db:
                create_fav_data = FavoriteVendors(
                    user_id=data.get('user_id'),
                    vendor_id=data.get('vendor_id'))
                db.add(create_fav_data)
                db.commit()

            return 'Successful vendor favorited.'
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"failed to add favourite vendor - {e}")
        

    @staticmethod
    async def get_vendors(user_id:str):
        '''
        This function responsibillity is to return all vendors from the database
        This includes information about the user's favorites vendors. 
        Returns vendors as GeoJSON Features.
        '''

        try:
            with get_db() as db:
                # First let's get all of the vendors
                get_all_vendors = select(Vendors)
                all_vendors = db.execute(get_all_vendors).scalars().all()

                # Then we collect all of the information from the favorite vendors.
                get_fav_vendors = select(FavoriteVendors).where(FavoriteVendors.user_id == user_id)
                fav_vendor_records = db.execute(get_fav_vendors).scalars().all()

                # Extract favorite vendor IDs
                favorite_vendor_ids = [fav.vendor_id for fav in fav_vendor_records]

                # Separate vendors into favorites and non-favorites
                favorite_vendor_objects = [vendor for vendor in all_vendors if str(vendor.unique_id) in favorite_vendor_ids]
                
                # Convert to GeoJSON Feature format
                favorite_vendors = [vendor_to_geojson_feature(vendor) for vendor in favorite_vendor_objects]
                all_vendors_geojson = [vendor_to_geojson_feature(vendor) for vendor in all_vendors]
       

                # Create response object
                response = {
                    'favorite_vendors': favorite_vendors,
                    'all_vendors': all_vendors_geojson
                }

                return response
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"failed to retrieve vendors - {e}")
