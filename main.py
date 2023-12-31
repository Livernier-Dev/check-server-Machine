import socket
import time
from datetime import datetime
import requests
from myserver import server_on


# ฟังก์ชันตรวจสอบสถานะของเครื่อง server
def check_server_status(ip, port):
    try:
        s = socket.create_connection((ip, port), timeout=1)
        s.close()
        return True
    except socket.error:
        return False

# ฟังก์ชันส่งข้อมูลไปยัง Discord Webhook
def send_discord_webhook(message, mention_id=None):
    webhook_url = "webhook_url"
    payload = {
        "content": message,
        "allowed_mentions": {"users": [mention_id]} if mention_id else {}
    }
    requests.post(webhook_url, json=payload)

# ตัวแปรเก็บสถานะก่อนหน้า
previous_status = {}

# ตัวอย่างการใช้งาน
server_ips = ["IP_1", "IP_2", "IP_3"]
server_port = 80  # หรือ port ที่คุณต้องการตรวจสอบ

# Discord user or role ID to mention (replace with the actual ID)
mention_id = "ID_DISCORD"

# เวลาที่รันครั้งแรก
first_run_time = datetime.now()
print(f"First run time: {first_run_time}")
send_discord_webhook(f"First run time: {first_run_time}")

while True:
  current_time = datetime.now()
  status_changed = False  # Flag to check if any status has changed

  for ip in server_ips:
    status = "online" if check_server_status(ip, server_port) else "offline"
    send_discord_webhook(f"{current_time}:  Server Machine IP: {ip} {status}")

    # ตรวจสอบการเปลี่ยนแปลง
    if ip in previous_status and previous_status[ip] != status:
      status_changed = True  # Set the flag to True

    print(
        "=========================================================================="
    )
    print(f"{current_time}: Server Machine IP: {ip} {status}")
    print(
        "=========================================================================="
    )

    # ถ้าเครื่อง server offline ให้ส่งข้อมูลไปยัง Discord Webhook พร้อมแท็ก user หรือ role
    if status == "offline":
      send_discord_webhook(f"Server Machine IP: {ip} is offline.",
                           f"<@{mention_id}>")

  # ตรวจสอบ Flag ว่ามีการเปลี่ยนแปลงหรือไม่
  if status_changed:
    # ส่งข้อมูลไปยัง Discord Webhook เมื่อมีการเปลี่ยนแปลง
    send_discord_webhook(f"{current_time} : Server status changed.")

  # อัปเดตสถานะก่อนหน้า
  previous_status = {
      ip: "online" if check_server_status(ip, server_port) else "offline"
      for ip in server_ips
  }
    
  server_on()
  # หยุดทำงาน 5 นาที
  time.sleep(300)
