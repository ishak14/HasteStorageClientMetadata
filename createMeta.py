import time
import datetime
from haste_storage_client.core import HasteStorageClient, OS_SWIFT_STORAGE, TRASH
from haste_storage_client.core2 import HasteStorageClientMeta
from classes.metadata_class import Ingredient, Author, Project, Metadata, Description

haste_storage_client_config = {
    'haste_metadata_server': {
        # See: https://docs.mongodb.com/manual/reference/connection-string/
        'connection_string': 'mongodb://130.239.81.77:27017'
    },
    'os_swift': {
        # See: https://docs.openstack.org/keystoneauth/latest/
        #   api/keystoneauth1.identity.v3.html#module-keystoneauth1.identity.v3.password
        'username': 's9498',
        'password': '***',
        'project_name': 'SNIC 2018/10-31',
        'user_domain_name': 'snic',
        'auth_url': 'https://hpc2n.cloud.snic.se:5000/v3',
        'project_id': '18b42df05165487984448173891ceeee',
        'project_domain_name':  'snic'
    }
}

# Identifies both the experiment, and the session (ie. unique each time the stream starts),
# for example, this would be a good format - this needs to be generated at the stream edge.
initials = 'Tony_Wang'
stream_id = datetime.datetime.today().strftime('%Y_%m_%d__%H_%M_%S') + '_exp1_' + initials

print('stream ID is: %s' % stream_id)

# Optionally, specify REST server with interesting model:


# Project ID
#project_id = "1"


#CREATE METADATA
#Initilize 	def __init__(self,name,amount,amountType):
author_list = {["Tony Wang","Uppsala University"],["Andy Ishak", "Uppsala University"]}
ingredient_list = {["magnesium",2,"ml"],["carbon",5,"cl"]}
authors =[]
ingredients = []

for ingredient in ingredient_list:
    ingredient = Ingredient(ingredient[0],ingredient[1],ingredient[2])
    ingredients.append(ingredient)
description = Description("testing out how a cell x reacts to 2ml mercury over y time")		

for author in author_list:
	author = Author(author[0],author[1])
	authors.append(author)
		
		
		
metadata = Metadata(ingredients,description,authors)
project = Project("Cell Mercury Testing","testing what mercury in the cell x will do over time of y month", metadata)

client = HasteStorageClientMeta(
                            project_id=stream_id,
                            config=haste_storage_client_config,
                            project = project,
                            storage_policy=[(0.5, 1.0, OS_SWIFT_STORAGE)],  # map 0.5<=interestingness<=1.0 to OS swift.
                            default_storage=TRASH)  # discard blobs which don't match the policy above.

#blob_bytes = b'this is a binary blob eg. image data.'
timestamp_cloud_edge = time.time()
substream_id = 'B22'  # Group by microscopy well ID.
description = "description test!"
machineNumber = "SQ7333"
institute = "Gothenburg University"
"""
    def save(timestamp_cloud_edge,
             substream_id,
             description,
             machineNumber,
             institute
             ):
             """
client.save(timestamp_cloud_edge,
		substream_id,
        project)    

client.close()
