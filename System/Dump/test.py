import sys, os 
import json

if __name__ == '__main__':
	sys.path.append(os.path.join(os.path.dirname(__file__), '..\Representation'))

	from Objects.mongoencoder import encode_model, decode_model
	from Objects.value import Value

	message = "{\"date\":\"2013-09-10T16:51:40.985000\", \"valueType\": \"Luninini\", \"id\": \"522f31fce776ca12181a7d7a", \"value\": \"220.0\", \"comments\": []}"
	value = decode_model(json.load(message), 'Value')

	print str(value)


