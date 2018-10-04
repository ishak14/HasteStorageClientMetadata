from __future__ import print_function
from pymongo import MongoClient
from os.path import expanduser
from .storage import OsSwiftStorage
import json

OS_SWIFT_STORAGE = 'os_swift'
TRASH = 'trash'
INTERESTINGNESS_DEFAULT = 1.0

class HasteStorageClientMeta:
    
	def __init__(self,
                project_id,
                config=None,
				project=None,
                storage_policy=None,
                default_storage=OS_SWIFT_STORAGE):
        
        	if config is None:
            		try:
                		config = self.__read_config_file()
            		except:
                		raise ValueError('If config is None, provide a configuration file.')

        	if default_storage is None:
            		raise ValueError("default_storage_location cannot be None - did you mean 'trash'?")

        	self.project_id = project_id
			self.project = project
        	self.default_storage = default_storage

        	self.os_swift_storage = OsSwiftStorage(config[OS_SWIFT_STORAGE])

        	self.mongo_client = MongoClient(config['haste_metadata_server']['connection_string'])
        	self.mongo_collection = self.mongo_client.streams['strm_' + self.project_id]

        	# ensure indices (idempotent)
        	self.mongo_collection.create_index('substream_id')
        	self.mongo_collection.create_index('timestamp')
        	self.mongo_collection.create_index('location')
	@staticmethod
	def __read_config_file():
		with open(expanduser('~/.haste/haste_storage_client_config.json')) as fh:
			haste_storage_client_config = json.load(fh)
		return haste_storage_client_config

	def save(self,
             timestamp,
             substream_id,
			 proejct
             ):

      
		blob_id = 'strm_' + self.project_id + '_ts_' + str(timestamp)
		document = {'timestamp': timestamp,
                        'substream_id': substream_id,
                        'description': description,
                        'machineNumber': machineNumber,
                        'institute': institute}
        
		result = self.mongo_collection.insert(document)
		return document    

	def __read_config_file():
		with open(expanduser('~/.haste/haste_storage_client_config.json')) as fh:
			haste_storage_client_config = json.load(fh)
		return haste_storage_client_config

	def close(self):
		self.mongo_client.close()
		self.os_swift_storage.close()

	def __save_blob(self, blob_id, blob_bytes, interestingness):
		storage_platforms = []
		if self.storage_policy is not None:
			for min_interestingness, max_interestingness, storage in self.storage_policy:
				if min_interestingness <= interestingness <= max_interestingness and (storage not in storage_platforms):
					self.__save_blob_to_platform(blob_bytes, blob_id, storage)
					storage_platforms.append(storage)

		if len(storage_platforms) == 0 and self.default_storage != TRASH:
			self.__save_blob_to_platform(blob_bytes, blob_id, self.default_storage)
			storage_platforms.append(self.default_storage)

		return storage_platforms

	def __save_blob_to_platform(self, blob_bytes, blob_id, storage_platform):
		if storage_platform == OS_SWIFT_STORAGE:
			self.os_swift_storage.save_blob(blob_bytes, blob_id)
		elif storage_platform == TRASH:
			raise ValueError('trash cannot be specified in a storage policy, only as a default')
		else:
			raise ValueError('unknown storage platform')
