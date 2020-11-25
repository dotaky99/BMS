
def format_timestamp(timestamp):
	if timestamp is None:
		return 'N/A'

	return timestamp.strftime('%Y-%m-%d %H:%M:%S')

def format_source(source_str, source_tag):
	if source_str is None or len(source_str) == 0:
		return ''

	if source_tag is None or len(source_tag) == 0:
		return source_str

	return '{} ({})'.format(source_str, source_tag)