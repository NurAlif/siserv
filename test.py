from http.server import BaseHTTPRequestHandler, HTTPServer

# Define the server's host and port
HOST = '0.0.0.0'
PORT = 7777

# Create a custom request handler class
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. Send response status code
        self.send_response(200)

        # 2. Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # 3. Write the response body
        message = "Hello, World!"
        self.wfile.write(bytes(message, "utf8"))

# Main execution block
if __name__ == '__main__':
    # Create the server instance
    server = HTTPServer((HOST, PORT), SimpleHandler)
    print(f"Server started at http://{HOST}:{PORT}")
    print("Press Ctrl+C to stop the server.")

    try:
        # Start the server and keep it running until interrupted
        server.serve_forever()
    except KeyboardInterrupt:
        # Handle Ctrl+C to shut down gracefully
        pass

    server.server_close()
    print("\nServer stopped.")