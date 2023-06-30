from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def get_visitor_ip():
    # Retrieve the visitor's IP address from the request headers
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    return f"Visitor IP: {client_ip}"

aa = get_visitor_ip()
print(aa)
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=2222)
