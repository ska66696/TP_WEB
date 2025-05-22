from urllib.parse import parse_qs
import html

def application(environ, start_response):
    """
    Простое WSGI-приложение.
    Выводит GET и POST параметры.
    """
    output_lines = ["Hello from simple WSGI app!"]

    query_string = environ.get('QUERY_STRING', '')
    get_params = parse_qs(query_string)
    
    output_lines.append("\nGET Parameters:")
    if get_params:
        for key, values in get_params.items():
            for value in values:
                output_lines.append(f"- {html.escape(key)}: {html.escape(value)}")
    else:
        output_lines.append("- No GET parameters received.")

    output_lines.append("\nPOST Parameters:")
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    if request_body_size > 0:
        request_body = environ['wsgi.input'].read(request_body_size)
        post_params = parse_qs(request_body.decode('utf-8'))
        
        if post_params:
            for key, values in post_params.items():
                for value in values:
                    output_lines.append(f"- {html.escape(key)}: {html.escape(value)}")
        else:
            output_lines.append("- No POST parameters received (or could not parse body).")
    else:
        output_lines.append("- No POST parameters received (Content-Length is 0 or missing).")
    
    status = '200 OK'
    response_body = "\n".join(output_lines)
    
    response_headers = [
        ('Content-Type', 'text/plain; charset=utf-8'),
        ('Content-Length', str(len(response_body.encode('utf-8'))))
    ]
    
    start_response(status, response_headers)
    return [response_body.encode('utf-8')]

if __name__ == '__main__':
    try:
        from wsgiref.simple_server import make_server
        httpd = make_server('localhost', 8081, application)
        print("Serving on port 8081...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down...")