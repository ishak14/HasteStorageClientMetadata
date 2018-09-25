import time
import datetime
from haste_storage_client.core_meta import HasteStorageClient, OS_SWIFT_STORAGE, TRASH, HasteStorageAbstract



haste_storage_client_config = {
    'haste_metadata_server': {
        # See: https://docs.mongodb.com/manual/reference/connection-string/
        'connection_string': 'mongodb://192.168.1.14:27017'
    },
    'os_swift': {
        # See: https://docs.openstack.org/keystoneauth/latest/
        #   api/keystoneauth1.identity.v3.html#module-keystoneauth1.identity.v3.password
        'username': 's9498',
        'password': 'Fikt6UppbD',
        'project_name': 'SNIC 2018/10-31',
        'user_domain_name': 'snic',
        'auth_url': 'https://hpc2n.cloud.snic.se:5000/v3',
        'project_id': '18b42df05165487984448173891ceeee',
        'project_domain_name':  'snic'
    }
}

# Identifies both the experiment, and the session (ie. unique each time the stream starts),
# for example, this would be a good format - this needs to be generated at the stream edge.
initials = 'anna_example'
stream_id = datetime.datetime.today().strftime('%Y_%m_%d__%H_%M_%S') + '_exp1_' + initials

print('stream ID is: %s' % stream_id)

# Optionally, specify REST server with interesting model:


# Project ID
project_id = 1

client = HasteStorageClientMeta(stream_id,
                            project_id=project_id,
                            config=haste_storage_client_config,
                            description="this test was made in ...",
                            machineNumber="S4240 Panasonic",
                            institute="Uppsala University",
                            storage_policy=[(0.5, 1.0, OS_SWIFT_STORAGE)],  # map 0.5<=interestingness<=1.0 to OS swift.
                            default_storage=TRASH)  # discard blobs which don't match the policy above.

blob_bytes = b'this is a binary blob eg. image data.'
timestamp_cloud_edge = time.time()
substream_id = 'B14'  # Group by microscopy well ID.
description=""

"""
    def save(self,
             timestamp,
             location,
             substream_id,
             description,
             machineNumber,
             institute,
             blob_id
             ):
             """
client.save(timestamp_cloud_edge,
            (19.34, 5.78),
            substream_id)    

client.close()