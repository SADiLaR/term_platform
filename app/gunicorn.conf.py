# Send output from the web app to the error log:
capture_output = True
errorlog = "-"

keepalive = 30
max_requests = 1000000
max_requests_jitter = 1000
graceful_timeout = 5
preload_app = True

workers = 4
threads = 3
