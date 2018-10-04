import time
import datetime
from haste_storage_client.core import HasteStorageClient, OS_SWIFT_STORAGE, TRASH
from haste_storage_client.interestingness_model import RestInterestingnessModel


haste_storage_client_config = {
    'haste_metadata_server': {
        # See: https://docs.mongodb.com/manual/reference/connection-string/
        'connection_string': 'mongodb://130.239.81.77:27017'
    },
        'os_swift': {                                                                                                                       strm_2018_10_02__12_31_53_exp1_Tony_Wang
        # See: https://docs.openstack.org/keystoneauth/latest/                                                                          strm_2018_10_02__12_32_12_exp1_Tony_Wang
        #   api/keystoneauth1.identity.v3.html#module-keystoneauth1.identity.v3.password                                                replicaset:PRIMARY> upsert(self, doc, namespace, timestamp):
        'username': 's9298',                                                                                                            ...
        'password': '***',                                                                                                       ... '
        'project_name': 'SNIC 2018/',                                                                                                   2018-10-02T12:33:35.117+0000 E QUERY    [js] SyntaxError: missing ; before statement @(shell):1:39
        'user_domain_name': 'snic',                                                                                                     replicaset:PRIMARY>
        'auth_url': 'xxxxx',                                                                                                            replicaset:PRIMARY> upsert(self, doc, namespace, timestamp):  '
        'project_domain_name': 'xxxx'                                                                                                   2018-10-02T12:33:38.944+0000 E QUERY    [js] SyntaxError: missing ; before statement @(shell):1:39
    }
}

# Identifies both the experiment, and the session (ie. unique each time the stream starts),
# for example, this would be a good format - this needs to be generated at the stream edge.
initials = 'anna_exampleson'
stream_id = datetime.datetime.today().strftime('%Y_%m_%d__%H_%M_%S') + '_exp1_' + initials

print('stream ID is: %s' % stream_id)

# Optionally, specify REST server with interesting model:
interestingness_model = RestInterestingnessModel('http://localhost:5000/model/api/v0.1/evaluate')


client = HasteStorageClient(stream_id,
                            config=haste_storage_client_config,
                            interestingness_model=interestingness_model,
                            storage_policy=[(0.5, 1.0, OS_SWIFT_STORAGE)],  # map 0.5<=interestingness<=1.0 to OS swift.
                            default_storage=TRASH)  # discard blobs which don't match the policy above.

blob_bytes = b'this is a binary blob eg. image data.'
timestamp_cloud_edge = time.time()
substream_id = 'B13'  # Group by microscopy well ID.

client.save(timestamp_cloud_edge,
            (12.34, 56.78),
            substream_id,
            blob_bytes,
            {'image_height_pixels': 300,  # bag of extracted features here
             'image_width_pixels': 300,
             'number_of_green_pixels': 1234})

client.close()
