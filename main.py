import customtkinter as ctk
from datetime import datetime
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

socket_client = socket(AF_INET, SOCK_STREAM)
socket_client.connect(('7.tcp.eu.ngrok.io', 17497))

# Налаштування теми
ctk.set_appearance_mode("System")  # Light / Dark / System
ctk.set_default_color_theme("blue")

# Головне вікно
app = ctk.CTk()
app.geometry("650x520")
app.title("LogiTalk")


# ======= Реєстрація =======

def start_chat():
    username = username_entry.get().strip()
    if username:
        global current_user
        current_user = username
        register_frame.pack_forget()
        chat_label.configure(text=f"Користувач: {username}")
        chat_frame.pack(fill="both", expand=True)
        send_system_message(f"Привіт, {username}! 👋")


register_frame = ctk.CTkFrame(app)
register_frame.pack(fill="both", expand=True)

username_label = ctk.CTkLabel(register_frame, text="Введіть ім’я користувача:")
username_label.pack(pady=10)

username_entry = ctk.CTkEntry(register_frame, placeholder_text="Ваше ім’я")
username_entry.pack(pady=10)

login_button = ctk.CTkButton(register_frame, text="Увійти", command=start_chat)
login_button.pack(pady=10)

# ======= Чат-вікно =======

chat_frame = ctk.CTkFrame(app)

# Ліве меню
side_menu = ctk.CTkFrame(chat_frame, width=120)
side_menu.pack(side="left", fill="y", padx=5, pady=5)


# Кнопка очищення чату
def clear_chat():
    chat_box.configure(state="normal")
    chat_box.delete("1.0", "end")
    chat_box.configure(state="disabled")


clear_button = ctk.CTkButton(side_menu, text="Очистити", command=clear_chat)
clear_button.pack(pady=10)


# Перемикач теми
def toggle_theme():
    mode = ctk.get_appearance_mode()
    if mode == "Light":
        ctk.set_appearance_mode("Dark")
    else:
        ctk.set_appearance_mode("Light")


theme_button = ctk.CTkButton(side_menu, text="Змінити тему", command=toggle_theme)
theme_button.pack(pady=10)

# Вивід імені
chat_label = ctk.CTkLabel(chat_frame, text="Користувач: ")
chat_label.pack(pady=5)

# Поле для чату
chat_box = ctk.CTkTextbox(chat_frame, width=450, height=300)
chat_box.pack(pady=10)
chat_box.insert("end", "👋 Ласкаво просимо до LogiTalk!\n")
chat_box.configure(state="disabled")

# Поле для введення
message_entry = ctk.CTkEntry(chat_frame, width=400, placeholder_text="Введіть повідомлення...")
message_entry.pack(pady=5)


# Функція надсилання
def send_message():
    message = message_entry.get().strip()
    if message:
        now = datetime.now().strftime("%H:%M")
        chat_box.configure(state="normal")
        chat_box.insert("end", f"[{now}] {current_user}: {message}\n")
        chat_box.configure(state="disabled")
        message_entry.delete(0, "end")
        try:
            socket_client.send(message.encode())
        except:
            pass


# Кнопка Надіслати
send_button = ctk.CTkButton(chat_frame, text="Надіслати", command=send_message)
send_button.pack(pady=5)


# Системне повідомлення (без автора)
def send_system_message(text):
    now = datetime.now().strftime("%H:%M")
    chat_box.configure(state="normal")
    chat_box.insert("end", f"[{now}] 🟢 {text}\n")
    chat_box.configure(state="disabled")


# Запуск
current_user = "Користувач"
name = 'Марко'
socket_client.send(name.encode())


def recv_message():
    while True:
        try:
            msg = socket_client.recv(1024).decode()
            if msg:
                send_system_message(msg)
        except:
            pass


Thread(target=recv_message, daemon=True).start()
app.mainloop()
