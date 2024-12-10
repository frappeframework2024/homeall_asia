# Copyright (c) 2024, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document


class Vendors(Document):
	pass


@frappe.whitelist(methods="POST")
def submit_vendor():
	data = json.loads(frappe.request.data)
		
 
	data["doctype"] = "Vendors"
	vendor = frappe.db.exists("Vendors",{"odoo_vendor_id":data.get("odoo_vendor_id")})#this function return primary key
	 
	if not vendor:
		doc = frappe.get_doc(data)
		doc.insert()
	else:
		# update doc
		doc = frappe.get_doc("Vendors",vendor)
		doc.vendor_name = data.get("vendor_name")
		doc.username= data.get("username")
		doc.password= data.get("password")
		doc.save()


	frappe.db.commit()
		
	return doc

        
    
