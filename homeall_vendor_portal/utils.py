import frappe

@frappe.whitelist( allow_guest=True )
def login(usr, pwd):
    import base64
    # from frappe.core.doctype.user.user import generate_keys
    try:
        login_manager = frappe.auth.LoginManager()
        login_manager.authenticate(user=usr, pwd=pwd)
        login_manager.post_login()
    except frappe.exceptions.AuthenticationError:
        frappe.clear_messages()
        frappe.throw("Usename and password incorrect.")
        


    api_generate = generate_keys(frappe.session.user)
    user = frappe.get_doc('User', frappe.session.user)
    byte_data = str({
        "success_key":1,
        "message":"Authentication success",
        "sid":frappe.session.sid,
        "api_key":user.api_key,
        "api_secret":api_generate,
        "username":user.username,
        "full_name":user.full_name,
        "role_profile":user.role_profile_name,
        "photo":user.user_image,
        "email":user.email
    }).encode('utf-8')
    base64_encoded = base64.b64encode(byte_data)    
    encoded_string = base64_encoded.decode('utf-8')
    frappe.response["message"] = encoded_string
    frappe.response["token"] = base64.b64encode(str("{}:{}".format(user.api_key,api_generate)).encode("utf-8")).decode('utf-8')
    
    frappe.response["user"] = {
        "username":user.username,
        "full_name":user.full_name,
        "role_profile":user.role_profile_name,
        "photo":user.user_image,
        "email":user.email
    }


def generate_keys(user):
	"""
	generate api key and api secret
 
	:param user: str
	"""
	# frappe.only_for("System Manager")
	user_details = frappe.get_doc("User", user)
	api_secret = frappe.generate_hash(length=15)
	# if api key is not set generate api key
	if not user_details.api_key:
		api_key = frappe.generate_hash(length=15)
		user_details.api_key = api_key
	user_details.api_secret = api_secret
	user_details.save(ignore_permissions=True)

	return api_secret
