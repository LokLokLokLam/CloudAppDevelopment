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
    
    filter_dealerId = ""
    if "dealerId" in param_dict:
        filter_dealerId = int(param_dict["dealerId"])
    db_reviews = client['reviews']
    selector = {'dealership': {'$eq': filter_dealerId}}
    docs = db_reviews.get_query_result(selector)
    t = []
    for document in docs:
        a_doc = {}
        a_doc["id"] = document["id"]
        a_doc["name"] = document["name"]
        a_doc["dealership"] = document["dealership"]
        a_doc["review"] = document["review"]
        a_doc["purchase"] = document["purchase"]
        if document["purchase"]:
            a_doc["purchase_date"] = document["purchase_date"]
            a_doc["car_make"] = document["car_make"]
            a_doc["car_model"] = document["car_model"]
            a_doc["car_year"] = document["car_year"]
        t.append(a_doc)
    return {"doc": t}