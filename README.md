# Flask-Web-DATA-Learn-
"Flask-Web-DATA(Learn)" name of a Flask web application project focused on learning about data handling and management

# Web Application Security Middleware

This middleware provides functionality for enforcing rate limiting, IP blacklisting, and other security measures in Flask web applications.

# Flowchart 

+-----------------+
|   Start Point   |
+--------+--------+
         |
         V
    +----+----+
    |   Imports |        -------------> FLASK, TIME, collections, apscheduler, random, string, os
    +-----------+
         |
         V
 +-------+---------+
 | Flask Setup     |
 +-------+---------+
 |   - Functionality: Set up Flask application
 |   > from flask import Flask, render_template, request, abort
 |   > import time
 |   > from collections import defaultdict
 |   > from apscheduler.schedulers.background import BackgroundScheduler
 |   > import atexit
 |   > import random
 |   > import string
 |   > import os
 +-------+---------+
         |
         V
 +-------+---------+
 | Random Password |
 |   Generation    |
 +-------+---------+
 |   - Functionality: Generate random passwords for admin access
 |   > def generate_random_password(length=8):
 |   >     chars = string.ascii_letters + string.digits + string.punctuation
 |   >     return ''.join(random.choice(chars) for _ in range(length))
 |   > admin_password = generate_random_password()
 +-------+---------+
         |
         V
 +-------+---------+
 | Admin Password  |
 |   Generation    |
 +-------+---------+
 |   - Functionality: Generate and store a random admin password
 |   > admin_password = generate_random_password()
 +-------+---------+
         |
         V
 +-------+---------+
 | IP Address      |
 |   Retrieval     |
 +-------+---------+
 |   - Functionality: Retrieve user's public IP address (dummy in local environment)
 |   > def get_ip_address():
 |   >     try:
 |   >         return "127.0.0.1"  # In local environment, return dummy IP
 |   >     except Exception as e:
 |   >         print("Error getting IP address:", e)
 |   >         return None
 +-------+---------+
         |
         V
 +-------+---------+
 | Abnormal        |
 |   Activity      |
 |   Handling      |
 +-------+---------+
 |   - Functionality: Handle abnormal activity, ban IP addresses if necessary
 |   > def handle_abnormal_activity(ip):
 |   >     ban_expiration = time.time() + BAN_DURATION
 |   >     ip_blacklist[ip] = ban_expiration
 |   >     with open("ipblocked.txt", "a") as file:
 |   >         file.write(ip + "\n")
 |   >     print(f"IP address {ip} has been banned until {time.ctime(ban_expiration)}")
 +-------+---------+
         |
         V
 +-------+---------+
 | Middleware for  |
 |   Rate Limiting |
 |   and IP        |
 |   Blacklisting  |
 +-------+---------+
 |   - Functionality: Enforce rate limiting and IP blacklisting to prevent DDOS attacks
 |   > @app.before_request
 |   > def protect_against_ddos():
 |   >     ip = request.remote_addr
 |   >     current_time = time.time()
 |   >     if ip in ip_blacklist:
 |   >         if current_time < ip_blacklist[ip]:
 |   >             return abort(403)
 |   >         else:
 |   >             del ip_blacklist[ip]
 |   >     ip_access_counts[ip] += 1
 |   >     ip_last_access[ip] = current_time
 |   >     if ip_access_counts[ip] > RATE_LIMIT:
 |   >         handle_abnormal_activity(ip)
 |   >         return abort(429)
 +-------+---------+
         |
         V
 +-------+---------+
 | File Operations |
 |   for IP        |
 |   Blacklist     |
 +-------+---------+
 |   - Functionality: Read and write blocked IP addresses to a file
 |   > def block_blocked_ips():
 |   >     try:
 |   >         with open("ipblocked.txt", "r") as file:
 |   >             blocked_ips = file.readlines()
 |   >             for ip in blocked_ips:
 |   >                 ip = ip.strip()
 |   >                 ip_blacklist[ip] = time.time() + BAN_DURATION
 |   >     except FileNotFoundError:
 |   >         pass
 +-------+---------+
         |
         V
 +-------+---------+
 | Periodic Cleanup|
 |   and IP        |
 |   Blocking      |
 +-------+---------+
 |   - Functionality: Periodic cleanup of IP access counts and blocking of IPs
 |   > scheduler.add_job(clear_ip_access_counts, 'interval', seconds=SCHEDULE_INTERVAL)
 |   > scheduler.add_job(block_blocked_ips, 'interval', seconds=10)
 |   > scheduler.start()
 |   > atexit.register(lambda: scheduler.shutdown())
 +-------+---------+
         |
         V
 +-------+---------+
 |  Application    |
 |   Startup       |
 +-------+---------+
 |   - Functionality: Start the Flask application, block IPs from ipblocked.txt
 |   > block_blocked_ips()
 |   > app.run(debug=True)
 +-------+---------+
         |
         V
+--------+--------+


+--------+--------+
 |   Output Examples   |
 +--------+--------+
         |
         V
 +-------+---------+
 |   Error Handling  |
 +-------+---------+
 |   - Example: Error message if there's an issue getting the IP address
 |   > "Error getting IP address: <error_message>"
 +-------+---------+
         |
         V
 +-------+---------+
 |   Request Handling  |
 +-------+---------+
 |   - Example: Abort request if IP is blacklisted or rate limit exceeded
 |   > HTTP 403 Forbidden (if IP is blacklisted)
 |   > HTTP 429 Too Many Requests (if rate limit exceeded)
 +-------+---------+
         |
         V
 +-------+---------+
 |   Admin Permission  |
 +-------+---------+
 |   - Example: Prompt for admin permission and enter admin password
 |   > "INFORMATION OF USER TRYING TO ACCESS:"
 |   > "Name: <name>"
 |   > "Mail: <mail>"
 |   > "Passwords: <passwords>"
 |   > "IP Address: <ip_address>"
 |   > "admin >> joined, granted? (Y/N): "
 |   > "Enter admin password: "
 +-------+---------+
         |
         V
 +-------+---------+
 |   Client Information |
 +-------+---------+
 |   - Example: Display client information after admin permission granted
 |   > "Received name: <name>"
 |   > "Received email: <mail>"
 |   > "Received pass: <passwords>"
 |   > "Saved client information to file."
 |   > Render template with client details.
 +-------+---------+
         |
         V
+--------+--------+

# Explanation Code

1. from flask import Flask, render_template, request, abort
   - This line imports necessary modules from the Flask framework, including Flask itself for creating the web application, render_template for rendering HTML templates, request for handling HTTP requests, and abort for aborting requests with error codes.

2. import time
   - This line imports the time module, which is used for time-related functions such as calculating timestamps.

3. from collections import defaultdict
   - This line imports defaultdict from the collections module, which is a specialized dictionary that provides a default value for keys that have not been set.

4. from apscheduler.schedulers.background import BackgroundScheduler
   - This line imports the BackgroundScheduler class from the apscheduler module, which is used for scheduling tasks to run in the background.

5. import atexit
   - This line imports the atexit module, which is used to register cleanup functions that are called when the program exits.

6. import random
   - This line imports the random module, which is used for generating random numbers and selecting random elements.

7. import string
   - This line imports the string module, which provides a collection of string constants and helper functions.

8. import os
   - This line imports the os module, which provides functions for interacting with the operating system, such as file operations and environment variables.

9. # Secret key for session management
   app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
   - This line sets a secret key for session management in the Flask application. The secret key is used to securely sign session cookies and other security-related functions.

10. # Define rate limiting parameters
    RATE_LIMIT = 10  # Maximum requests per minute per IP address
    RATE_LIMIT_PERIOD = 60  # Rate limit period in seconds (1 minute)
    - These lines define parameters for rate limiting requests. RATE_LIMIT specifies the maximum number of requests allowed per minute per IP address, and RATE_LIMIT_PERIOD specifies the duration of the rate limiting period in seconds.

11. # Define IP blacklist parameters
    BAN_DURATION = 3600  # Ban duration in seconds (1 hour)
    - This line defines the duration in seconds for which an IP address will be banned when it triggers abnormal activity. In this case, it's set to 1 hour.

12. # Maintain dictionaries to track access counts and blacklisted IPs
    ip_access_counts = defaultdict(int)
    ip_blacklist = {}
    ip_last_access = defaultdict(float)  # Dictionary to store last access time for each IP
    - These lines define dictionaries to keep track of access counts for each IP address, maintain a list of blacklisted IP addresses, and store the last access time for each IP.

13. # Function to generate a random password
    def generate_random_password(length=8):
        chars = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(chars) for _ in range(length))
    - This function generates a random password of the specified length using a combination of letters, digits, and punctuation characters.

14. # Generate a random admin password
    admin_password = generate_random_password()
    - This line generates a random admin password using the generate_random_password function defined earlier.

15. # Function to get user's public IP address
    def get_ip_address():
        try:
            # In a local environment, we cannot fetch the public IP address
            # Returning a dummy IP address for demonstration purposes
            return "127.0.0.1"
        except Exception as e:
            print("Error getting IP address:", e)
            return None
    - This function attempts to retrieve the user's public IP address. In a local environment, it returns a dummy IP address for demonstration purposes.

16. # Function to handle abnormal activity from an IP address
    def handle_abnormal_activity(ip):
        ban_expiration = time.time() + BAN_DURATION
        ip_blacklist[ip] = ban_expiration
        # Store blocked IP address in a file
        with open("ipblocked.txt", "a") as file:
            file.write(ip + "\n")
        print(f"IP address {ip} has been banned until {time.ctime(ban_expiration)}")
    - This function handles abnormal activity from an IP address by adding it to the blacklist for a specified duration (BAN_DURATION) and logging the ban in a file.

17. # Middleware to enforce rate limiting and IP blacklisting
    @app.before_request
    def protect_against_ddos():
        ip = request.remote_addr
        current_time = time.time()

        # Check if the IP address is blacklisted
        if ip in ip_blacklist:
            if current_time < ip_blacklist[ip]:
                return abort(403)  # Forbidden
            else:
                del ip_blacklist[ip]  # Remove from blacklist if ban has expired

        # Update access count and last access time for the IP address
        ip_access_counts[ip] += 1
        ip_last_access[ip] = current_time

        # Check if rate limit is exceeded
        if ip_access_counts[ip] > RATE_LIMIT:
            handle_abnormal_activity(ip)
            return abort(429)  # Too Many Requests
    - This middleware function is executed before each request to enforce rate limiting and IP blacklisting. It checks if the IP address is blacklisted and if the rate limit is exceeded, aborting the request with the appropriate HTTP error code if necessary.

18. # Function to load blocked IP addresses from file and block them
    def block_blocked_ips():
        try:
            with open("ipblocked.txt", "r") as file:
                blocked_ips = file.readlines()
                for ip in blocked_ips:
                    ip = ip.strip()
                    ip_blacklist[ip] = time.time() + BAN_DURATION
        except FileNotFoundError:
            pass
    - This function loads blocked IP addresses from a file ("ipblocked.txt") and adds them to the blacklist with the specified ban duration (BAN_DURATION).

19. # Clear IP access counts periodically to avoid memory bloat
    def clear_ip_access_counts():
        current_time = time.time()
        for ip in list(ip_access_counts.keys()):
            if current_time - ip_last_access[ip] > RATE_LIMIT_PERIOD:
                del ip_access_counts[ip]
    - This function clears the IP access counts periodically to avoid memory bloat. It iterates through the IP access counts dictionary and removes entries that haven't been accessed within the rate limit period (RATE_LIMIT_PERIOD).

20. # Schedule periodic cleanup of IP access counts and blocking of blocked IPs
    SCHEDULE_INTERVAL = 300  # Cleanup every 5 minutes
    scheduler = BackgroundScheduler()
    scheduler.add_job(clear_ip_access_counts, 'interval', seconds=SCHEDULE_INTERVAL)
    scheduler.add_job(block_blocked_ips, 'interval', seconds=10)  # Check every 10 seconds
    scheduler.start()
    - These lines schedule periodic tasks using the BackgroundScheduler. It schedules the cleanup of IP access counts every 5 minutes and the blocking of blocked IPs every 10 seconds.

21. # Make sure to stop the scheduler when the application exits
    atexit.register(lambda: scheduler.shutdown())
    - This line registers a function to stop the scheduler when the application exits. It ensures that the periodic tasks are properly terminated.

# Installation

Install the middleware using pip:

```
pip install Flask apscheduler
```

Getting Started

Clone this project 

```
git clone https://github.com/GiuCoder/Flask-Web-DATA-Learn-.git
```

Install Requirements

```
pip install -r requirements.txt
```

```
python main.py
```
or 
```
python3 main.py
```

# Features
Rate limiting: Limit the number of requests per minute per IP address.
IP blacklisting: Automatically block IP addresses that exhibit abnormal activity.
Automatic cleanup: Periodically clear IP access counts and block IPs loaded from a file.

# Usage

Adjust the rate limit parameters (RATE_LIMIT and RATE_LIMIT_PERIOD) and ban duration (BAN_DURATION) as needed.
Customize the handling of abnormal activity in the handle_abnormal_activity function.
Customize file paths and names for storing blocked IP addresses (ipblocked.txt).

# Disclaimer

This middleware, including all associated files and documentation, is provided on an "as-is" basis, without any warranties, express or implied. The authors and contributors of this middleware make no representations or warranties of any kind concerning the suitability, reliability, availability, accuracy, completeness, or legality of the middleware or its documentation for any purpose.

By using this middleware, you acknowledge and agree that:

The use of this middleware is at your own risk. You are solely responsible for any damage to your computer system or loss of data that results from the use of the middleware.

The authors and contributors of this middleware shall not be liable for any direct, indirect, incidental, special, consequential, or punitive damages arising out of the use or inability to use the middleware, including but not limited to damages for loss of profits, goodwill, use, data, or other intangible losses.

The authors and contributors of this middleware do not warrant that the middleware will meet your requirements, that the operation of the middleware will be uninterrupted or error-free, or that defects in the middleware will be corrected.

Any material downloaded or otherwise obtained through the use of the middleware is accessed at your own discretion and risk, and you will be solely responsible for any damage to your computer system or loss of data that results from the download of any such material.

No advice or information, whether oral or written, obtained by you from the authors or contributors of this middleware shall create any warranty not expressly stated in this disclaimer.

The inclusion of any links to third-party websites or resources does not imply endorsement by the authors or contributors of this middleware. You acknowledge and agree that the authors and contributors are not responsible for the availability or accuracy of such websites or resources.

By using this middleware, you agree to indemnify, defend, and hold harmless the authors and contributors from and against any and all claims, liabilities, damages, losses, costs, expenses, or fees (including reasonable attorneys' fees) arising out of or relating to your use of the middleware, your violation of these terms, or your violation of any rights of a third party.

Feel free to adjust the disclaimer as needed to align with the specific terms and conditions of your middleware project. Let me know if you need further assistance!

Copyright
© 2024 Your Company Name. All rights reserved.
