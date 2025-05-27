from flask import Flask, request, render_template_string
import threading
import requests
import time

app = Flask(__name__)
app.debug = True

html_code = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>FAIZU TOOL | Convo Loader</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {
      background: linear-gradient(to right, #141e30, #243b55);
      font-family: 'Segoe UI', sans-serif;
      color: white;
      animation: fadeIn 1s ease-in;
    }
    @keyframes fadeIn {
      from { opacity: 0; }
      to { opacity: 1; }
    }
    .header-img {
      width: 100%;
      max-height: 250px;
      object-fit: cover;
      border-radius: 0 0 20px 20px;
      box-shadow: 0 5px 15px rgba(0,0,0,0.4);
      margin-bottom: -50px;
    }
    .box {
      max-width: 600px;
      margin: 100px auto;
      background: rgba(0, 0, 0, 0.75);
      border-radius: 20px;
      padding: 35px;
      box-shadow: 0 0 30px rgba(0,255,170,0.4);
    }
    .box h2 {
      text-align: center;
      margin-bottom: 30px;
      font-weight: bold;
      color: #00ffaa;
      text-shadow: 0 0 5px #00ffaa;
    }
    label {
      font-weight: bold;
      color: #c5f0e5;
    }
    .form-control {
      background: #111;
      color: white;
      border: 1px solid #00ffaa;
    }
    .form-control:focus {
      border-color: #00ffaa;
      box-shadow: 0 0 10px #00ffaa;
    }
    .btn-submit {
      background: #00ffaa;
      border: none;
      color: black;
      font-weight: bold;
      transition: 0.3s;
    }
    .btn-submit:hover {
      background: #00ffae;
      color: white;
      box-shadow: 0 0 15px #00ffaa;
    }
    footer {
      text-align: center;
      margin-top: 40px;
      font-size: 14px;
      color: #aaa;
      text-shadow: 0 0 3px #00ffaa;
    }
  </style>
</head>
<body>
  <img src="https://raw.githubusercontent.com/Faiizuxd/The_Faizu_dpz/refs/heads/main/92292eb7ec36bc8c323a80f06d1ff7ec.jpg" alt="Convo Pic" class="header-img"/>
  <div class="box">
    <h2>FAIZU | Message Spammer</h2>
    <form action="/" method="post" enctype="multipart/form-data">
      <div class="mb-3">
        <label>Access Token:</label>
        <input type="text" class="form-control" name="accessToken" required />
      </div>
      <div class="mb-3">
        <label>Thread ID (Convo ID):</label>
        <input type="text" class="form-control" name="threadId" required />
      </div>
      <div class="mb-3">
        <label>Prefix Name (e.g., Hater name):</label>
        <input type="text" class="form-control" name="kidx" required />
      </div>
      <div class="mb-3">
        <label>Select Message List (.txt):</label>
        <input type="file" class="form-control" name="txtFile" accept=".txt" required />
      </div>
      <div class="mb-3">
        <label>Message Delay (in seconds):</label>
        <input type="number" class="form-control" name="time" min="1" required />
      </div>
      <button type="submit" class="btn btn-submit w-100">Start Bot</button>
    </form>
  </div>
  <footer>
    Developed by <strong>Stuner</strong> | 2024 All Rights Reserved
  </footer>
</body>
</html>
'''

# Message sender loop - enhanced reliability
def message_sender(access_token, thread_id, mn, time_interval, messages):
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0',
        'Accept': '*/*',
    }

    while True:
        for msg in messages:
            try:
                full_message = f"{mn} {msg}"
                api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                params = {
                    'access_token': access_token,
                    'message': full_message
                }
                r = requests.post(api_url, data=params, headers=headers)

                status = "Success" if r.status_code == 200 else f"Fail {r.status_code}"
                print(f"[{status}] {full_message}")
                time.sleep(time_interval)
            except requests.exceptions.RequestException as e:
                print(f"Request error: {e}")
                time.sleep(60)
            except Exception as ex:
                print(f"Unexpected error: {ex}")
                time.sleep(60)

@app.route('/', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        access_token = request.form.get('accessToken')
        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))
        messages = request.files['txtFile'].read().decode().splitlines()

        thread = threading.Thread(target=message_sender, args=(access_token, thread_id, mn, time_interval, messages))
        thread.daemon = True
        thread.start()

        return '<h2 style="color:white; text-align:center; margin-top:30px;">Script started successfully. Leave this running!</h2>'

    return render_template_string(html_code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=21551)
