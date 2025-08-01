from datetime import datetime

def log_progress(message):
    now = datetime.now()  # Obtener la fecha y hora actual
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")  # Formatear como texto
    with open("log_file.txt", "a") as f:
        f.write(f"{timestamp} - {message}\n")