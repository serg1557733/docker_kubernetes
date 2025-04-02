from http.server import SimpleHTTPRequestHandler, HTTPServer
import os
import redis
from urllib.parse import urlparse

# Get Redis connection details from environment variables
REDIS_URL = os.getenv('REDIS_URL', None)  # Redis connection string
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)

# Directory to check for image files
IMAGE_DIRECTORY = os.getenv('IMAGE_DIRECTORY', '/app/images')

# Function to create a Redis connection
def create_redis_connection():
    if REDIS_URL:
        # Parse the Redis URL and extract components
        url = urlparse(REDIS_URL)
        return redis.Redis(
            host=url.hostname,
            port=url.port,
            db=int(url.path[1:]) if url.path else 0,
            username=url.username,
            password=url.password,
            ssl=url.scheme == "rediss"
        )
    else:
        # Use individual parameters
        return redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            password=REDIS_PASSWORD
        )

# Try to connect to Redis
try:
    r = create_redis_connection()
    r.ping()  # Check if the connection is successful
    redis_connected = True
except redis.ConnectionError:
    redis_connected = False
    print("Failed to connect to Redis", flush=True)

class HelloWorldHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/images/"):
            self.serve_image_file()
        elif self.path == "/":
            self.serve_html_content()
        elif self.path.startswith("/add") or self.path.startswith("/remove"):
            if redis_connected:
                if self.path.startswith("/add"):
                    self.add_key_value()
                elif self.path.startswith("/remove"):
                    self.remove_key_value()
            else:
                self.send_error(404, "Redis not connected")
        else:
            self.send_error(404, "File Not Found")

    def serve_image_file(self):
        # Get the file path from the URL
        file_path = os.path.join(IMAGE_DIRECTORY, os.path.basename(self.path))
        if os.path.exists(file_path):
            # Serve the image file
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg' if file_path.endswith('.jpg') else 'image/png')
            self.end_headers()
            with open(file_path, 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_error(404, "File Not Found")

    def serve_html_content(self):
        # Get the container name from the environment variable 'HOSTNAME'
        container_name = os.getenv('HOSTNAME', 'Unknown Container')

        # Check if running inside a Kubernetes cluster by looking for the 'KUBERNETES_SERVICE_HOST' environment variable
        kubernetes_pod_name = os.getenv('HOSTNAME') if os.getenv('KUBERNETES_SERVICE_HOST') else 'Not in Kubernetes'

        # Prepare the base HTML content
        html_content = f"""
        <html>
        <body>
            <h1>Hello, World!</h1>
            <p>Container Name: {container_name}</p>
            <p>Kubernetes Pod Name: {kubernetes_pod_name}</p>
        """

        # Check for image files in the specified directory, handling errors gracefully
        try:
            if os.path.exists(IMAGE_DIRECTORY):
                image_files = [f for f in os.listdir(IMAGE_DIRECTORY) if f.endswith(('.jpg', '.png'))]

                # If an image file is found, add it to the HTML content
                if image_files:
                    image_file = image_files[0]  # Take the first image file found
                    image_path = f"/images/{image_file}"
                    html_content += f'<img src="{image_path}" alt="Image" style="max-width: 100%; height: auto;">'
        except Exception as e:
            # Log any unexpected errors (optional)
            print(f"Error checking images: {e}", flush=True)

        # Only include Redis-related content if connected
        if redis_connected:
            html_content += f"""
            <h2>Redis Connection: Successful</h2>
            <h3>Current Key-Value Pairs:</h3>
            <ul>
            """
            for key in r.keys():
                html_content += f"<li>{key.decode('utf-8')}: {r.get(key).decode('utf-8')} <a href='/remove?key={key.decode('utf-8')}'>Remove</a></li>"
            html_content += "</ul>"

            # Form to add a new key-value pair
            html_content += """
            <h3>Add a New Key-Value Pair:</h3>
            <form action="/add" method="get">
                Key: <input type="text" name="key"><br>
                Value: <input type="text" name="value"><br>
                <input type="submit" value="Add">
            </form>
            """

        # Close the HTML tags
        html_content += """
        </body>
        </html>
        """

        # Set the response status code to 200 (OK)
        self.send_response(200)
        
        # Set the content type to HTML
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Write the HTML content
        self.wfile.write(html_content.encode('utf-8'))

    def add_key_value(self):
        if redis_connected:
            # Parse the query string to get the key and value
            query = self.path.split("?")[1]
            params = dict(qc.split("=") for qc in query.split("&"))
            key = params.get("key")
            value = params.get("value")
            
            if key and value:
                # Add the key-value pair to Redis
                r.set(key, value)
        
        # Redirect back to the main page
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    def remove_key_value(self):
        if redis_connected:
            # Parse the query string to get the key
            query = self.path.split("?")[1]
            params = dict(qc.split("=") for qc in query.split("&"))
            key = params.get("key")
            
            if key:
                # Remove the key from Redis
                r.delete(key)
        
        # Redirect back to the main page
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

# Define the server address and port
server_address = ('0.0.0.0', 8080)

# Create an HTTP server
httpd = HTTPServer(server_address, HelloWorldHandler)

# Start the server
print(f"Starting server on http://localhost:8080")
httpd.serve_forever()