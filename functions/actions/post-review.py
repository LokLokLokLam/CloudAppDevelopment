"""IBM Cloud Function that gets all reviews for a dealership
Returns:
    List: List of reviews for the given dealership
"""
import sys
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests


def main(param_dict):
    """Main Function
    Args:
        param_dict (Dict): input paramater
    Returns:
        _type_: _description_ TODO
    """
    param_dict["COUCH_USERNAME"] = "57d360a5-45ae-43cb-a197-808795e4f84f-bluemix"
    param_dict["IAM_API_KEY"] = "coUgxtDGP0Uy7_tCvtZMa2vWfDA5lYWPKtlgq-0W6Rzu"
    try:
        client = Cloudant.iam(
            account_name=param_dict["COUCH_USERNAME"],
            api_key=param_dict["IAM_API_KEY"],
            connect=True,
        )
        print(f"Databases: {client.all_dbs()}")
    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}
    
    db_reviews = client['reviews']
    
    a_doc = {}
    a_doc["id"] = param_dict["id"]
    a_doc["name"] = param_dict["name"]
    a_doc["dealership"] = param_dict["dealership"]
    a_doc["review"] = param_dict["review"]
    a_doc["purchase"] = param_dict["purchase"]
    a_doc["another"] = param_dict["another"]
    a_doc["purchase_date"] = param_dict["purchase_date"]
    a_doc["car_make"] = param_dict["car_make"]
    a_doc["car_model"] = param_dict["car_model"]
    a_doc["car_year"] = param_dict["car_year"]
    
    create_doc = db_reviews.create_document(a_doc)
            

    return {"result": create_doc.exists()}