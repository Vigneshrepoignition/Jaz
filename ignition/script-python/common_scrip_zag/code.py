import datetime

def datetime_remove_t(data):
	parsed_timestamp = datetime.datetime.strptime(data, "%Y-%m-%dT%H:%M:%S")
	desired_format = "%Y-%m-%d %H:%M:%S"
	formatted_timestamp = parsed_timestamp.strftime(desired_format)
	return formatted_timestamp