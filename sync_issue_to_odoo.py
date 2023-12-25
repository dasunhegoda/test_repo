import xmlrpc.client
import os
import sys

# Odoo credentials and URL setup
url = os.getenv('ODOO_URL')
db = os.getenv('ODOO_DB')
username = os.getenv('ODOO_USERNAME')  # The username used to login to Odoo
password = os.getenv('ODOO_PASSWORD')  # The password used to login to Odoo
project_name = 'test_proj'  # The name of your project

# GitHub issue data
issue_title = sys.argv[1]  # Passed as the first argument to the script
issue_body = sys.argv[2]  # Passed as the second argument to the script

# XML-RPC endpoints
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Authenticate
uid = common.authenticate(db, username, password, {})

# Search for the project by name to get the ID
project_id = models.execute_kw(db, uid, password,
    'project.project', 'search',
    [[['name', '=', project_name]]],
    {'limit': 1})

if not project_id:
    print("Project not found")
    sys.exit(1)

# Create a task associated with the project
task_id = models.execute_kw(db, uid, password, 'project.task', 'create', [{
    'name': issue_title,
    'description': issue_body,
    'project_id': project_id[0],  # Assuming the project ID is the first in the list
}])

print(f"Task created with ID: {task_id}")
