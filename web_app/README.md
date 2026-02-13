# Lingua Web App - Commands Guide

This guide provides the necessary commands to start, stop, and troubleshoot the Lingua Web Application.

## 1. Prerequisites

Ensure you have the required Python packages installed. If you haven't installed them yet, run:

```bash
pip install flask opencv-python mediapipe SpeechRecognition pydub matplotlib
```

## 2. Starting the Application

To start the web application, run the following command from the **root directory** of the project (`ml_sih_isl-main`):

```bash
python3 web_app/app.py
```

Once the server starts, you will see output indicating it is running on `http://127.0.0.1:5001`. Open this URL in your web browser.

## 3. Stopping the Application

To stop the application, simply go to the terminal where it is running and press:

**`Ctrl + C`**

This will terminate the process.

## 4. Troubleshooting: "Address already in use"

If you try to start the app and get an error saying `Address already in use` or `Port 5001 is in use`, it means the previous instance wasn't closed properly.

To fix this, follow these steps:

1.  **Find the process ID (PID)** using port 5001:
    ```bash
    lsof -i :5001
    ```
    You will see output like this:
    ```
    COMMAND   PID   USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
    python3 12345   user   6u  IPv4 0x...      0t0  TCP localhost:5001 (LISTEN)
    ```

2.  **Kill the process** using the PID (replace `12345` with the actual PID from the previous step):
    ```bash
    kill -9 12345
    ```

3.  **Restart the app**:
    ```bash
    python3 web_app/app.py
    ```
