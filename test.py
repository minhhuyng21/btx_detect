import threading
import time

def wait_five_seconds():
  """Simulates a wait of 5 seconds in a separate thread."""
  print("Starting 5-second wait in separate thread...")
  sec = 0
  while sec < 5:
    time.sleep(1)
    sec += 1
    print(sec)
  print("Waited for 5 seconds (in separate thread)!")

# Create and start the thread
wait_thread = threading.Thread(target=wait_five_seconds)
wait_thread.start()

# Main program continues execution
print("Main program continues while waiting...")
# You can add other code to be executed here
for i in range(5):
  time.sleep(1)
  print('a')
# Wait for the thread to finish (optional)
wait_thread.join()  # This line will pause the main program until the wait_thread finishes

print('1'.encode())