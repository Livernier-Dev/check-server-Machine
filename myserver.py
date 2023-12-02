from flask import Flask
from threading import Thread

app = Flask('')


@app.route('/')
def home():
  return "Server is running!"


def run():
  try:
    app.run(host='0.0.0.0', port=8080)
  except Exception as e:
    print(f"An error occurred: {str(e)}")


_thread = None


def server_on():
  global _thread
  if _thread is None or not _thread.is_alive():
    _thread = Thread(target=run)
    _thread.start()
