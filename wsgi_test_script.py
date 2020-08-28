def application(environ, start_response):
	status = '200 OK'
	name = repr(environ['mod_wsgi.process_group'])
	html = '<html>\n' 
	html += '<body>\n'
	html += '<p>Hooray, mod_wsgi is working</p>\n'
	html += '<p>daemon process group (mod_wsgi.process_group) = {}\n'.format(name)
	html += '</p>'
	html += '</body>\n'
	html += '</html>\n'
	response_header = [('Content-type','text/html')]
	start_response(status, response_header)
	return [html]