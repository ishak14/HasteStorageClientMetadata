import time
import datetime
import pymongo
import pytest

from haste_storage_client.core import HasteStorageClient, OS_SWIFT_STORAGE, TRASH
from haste_storage_client.interestingness_model import RestInterestingnessModel



# Test that we can instantiate OK, and we get an timeout connecting to the DB server.
# This basically tests if the source parses OK.
def instantiate():
    haste_storage_client_config = {
        'haste_metadata_server': {
            # See: https://docs.mongodb.com/manual/reference/connection-string/
            'connection_string': 'mongodb://username:password@mongodb.thisdomaindoesnotexist.com/streams'
        },
        'os_swift': {
            # See: https://docs.openstack.org/keystoneauth/latest/
            #   api/keystoneauth1.identity.v3.html#module-keystoneauth1.identity.v3.password
            'username': 'xxxxx',
            'password': 'xxxx',
            'project_name': 'xxxxx',
            'user_domain_name': 'xxxx',
            'auth_url': 'xxxxx',
            'project_domain_name': 'xxxx'
        }
    }

    # Identifies both the experiment, and the session (ie. unique each time the stream starts),
    # for example, this would be a good format - this needs to be generated at the stream edge.
    initials = 'anna_exampleson'
    stream_id = datetime.datetime.today().strftime('%Y_%m_%d__%H_%M_%S') + '_exp1_' + initials

    print('stream ID is: %s' % stream_id)

    # Optionally, specify REST server with interesting model:
    interestingness_model = RestInterestingnessModel('http://thisdomaindoesnotexist.com:5000/model/api/v0.1/evaluate')


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


def test_instantiate():
    with pytest.raises(pymongo.errors.ServerSelectionTimeoutError):
        instantiate()