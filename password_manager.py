import customtkinter as ctk
import random
import string

# =========================
# МОДЕЛЬ ДАННЫХ
# =========================

class PasswordEntry:

    def __init__(self, site, login, password):

        self.site = site
        self.login = login
        self.password = password
        self.visible = False

# =========================
# МЕНЕДЖЕР ПАРОЛЕЙ
# =========================

class PasswordManager:

    def __init__(self):

        self.passwords = []

    def add_password(self, site, login, password):

        entry = PasswordEntry(
            site,
            login,
            password
        )

        self.passwords.append(entry)

    def search_passwords(self, text):

        text = text.lower()

        return [
            p for p in self.passwords
            if text in p.site.lower()
        ]

# =========================
# GUI
# =========================

class App(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("Password Manager")

        self.geometry("900x650")

        self.manager = PasswordManager()

        # =========================
        # ПОЛЯ ВВОДА
        # =========================

        self.site_entry = ctk.CTkEntry(
            self,
            placeholder_text="Сайт"
        )

        self.site_entry.pack(
            padx=20,
            pady=(20, 10),
            fill="x"
        )

        self.login_entry = ctk.CTkEntry(
            self,
            placeholder_text="Логин"
        )

        self.login_entry.pack(
            padx=20,
            pady=10,
            fill="x"
        )

        self.password_entry = ctk.CTkEntry(
            self,
            placeholder_text="Пароль",
            show="*"
        )

        self.password_entry.pack(
            padx=20,
            pady=10,
            fill="x"
        )

        # =========================
        # КНОПКИ
        # =========================

        self.button_frame = ctk.CTkFrame(self)

        self.button_frame.pack(
            pady=20
        )

        self.add_button = ctk.CTkButton(
            self.button_frame,
            text="Добавить",
            command=self.add_password,
            width=150
        )

        self.add_button.grid(
            row=0,
            column=0,
            padx=10
        )

        self.generate_button = ctk.CTkButton(
            self.button_frame,
            text="Сгенерировать",
            command=self.generate_password,
            width=150
        )

        self.generate_button.grid(
            row=0,
            column=1,
            padx=10
        )

        self.toggle_input_button = ctk.CTkButton(
            self.button_frame,
            text="Показать ввод",
            command=self.toggle_input_password,
            width=150
        )

        self.toggle_input_button.grid(
            row=0,
            column=2,
            padx=10
        )

        self.clear_button = ctk.CTkButton(
            self.button_frame,
            text="Очистить",
            command=self.clear_fields,
            width=150
        )

        self.clear_button.grid(
            row=0,
            column=3,
            padx=10
        )

        # =========================
        # ПОИСК
        # =========================

        self.search_entry = ctk.CTkEntry(
            self,
            placeholder_text="Поиск по сайту"
        )

        self.search_entry.pack(
            padx=20,
            pady=10,
            fill="x"
        )

        self.search_button = ctk.CTkButton(
            self,
            text="Поиск",
            command=self.search_passwords
        )

        self.search_button.pack(
            pady=10
        )

        # =========================
        # ОБЛАСТЬ СПИСКА
        # =========================

        self.scroll_frame = ctk.CTkScrollableFrame(self)

        self.scroll_frame.pack(
            padx=20,
            pady=20,
            fill="both",
            expand=True
        )

        self.input_password_visible = False

        self.show_passwords()

    
    # ДОБАВЛЕНИЕ
    # =========================

    def add_password(self):

        site = self.site_entry.get()

        login = self.login_entry.get()

        password = self.password_entry.get()

        if site and login and password:

            self.manager.add_password(
                site,
                login,
                password
            )

            self.show_passwords()

            self.clear_fields()

    # =========================
    # ОЧИСТКА
    # =========================

    def clear_fields(self):

        self.site_entry.delete(0, "end")

        self.login_entry.delete(0, "end")

        self.password_entry.delete(0, "end")

    # =========================
    # ГЕНЕРАЦИЯ
    # =========================

    def generate_password(self):

        chars = (
            string.ascii_letters +
            string.digits +
            "!@#$%^&*"
        )

        password = "".join(
            random.choice(chars)
            for _ in range(16)
        )

        self.password_entry.delete(0, "end")

        self.password_entry.insert(
            0,
            password
        )

    # =========================
    # ПОКАЗАТЬ ВВОД
    # =========================

    def toggle_input_password(self):

        self.input_password_visible = (
            not self.input_password_visible
        )

        if self.input_password_visible:

            self.password_entry.configure(show="")

            self.toggle_input_button.configure(
                text="Скрыть ввод"
            )

        else:

            self.password_entry.configure(show="*")

            self.toggle_input_button.configure(
                text="Показать ввод"
            )

    # =========================
    # ПОКАЗАТЬ / СКРЫТЬ
    # =========================

    def toggle_saved_password(self, entry):

        entry.visible = not entry.visible

        self.show_passwords()

    # =========================
    # ОТОБРАЖЕНИЕ
    # =========================

    def show_passwords(self, passwords=None):

        # очищаем старые виджеты
        for widget in self.scroll_frame.winfo_children():

            widget.destroy()

        if passwords is None:

            passwords = self.manager.passwords

        for i, entry in enumerate(passwords):

            card = ctk.CTkFrame(self.scroll_frame)

            card.pack(
                fill="x",
                padx=10,
                pady=10
            )

            site_label = ctk.CTkLabel(
                card,
                text=f"Сайт: {entry.site}",
                font=("Arial", 18)
            )

            site_label.pack(
                anchor="w",
                padx=10,
                pady=5
            )

            login_label = ctk.CTkLabel(
                card,
                text=f"Логин: {entry.login}",
                font=("Arial", 16)
            )

            login_label.pack(
                anchor="w",
                padx=10,
                pady=5
            )

            # пароль
            if entry.visible:

                password_text = entry.password

            else:

                password_text = "*" * len(entry.password)

            password_label = ctk.CTkLabel(
                card,
                text=f"Пароль: {password_text}",
                font=("Arial", 16)
            )

            password_label.pack(
                anchor="w",
                padx=10,
                pady=5
            )

            # кнопка показать/скрыть
            toggle_button = ctk.CTkButton(
                card,
                text="Скрыть" if entry.visible else "Показать",
                command=lambda e=entry:
                self.toggle_saved_password(e)
            )

            toggle_button.pack(
                padx=10,
                pady=10,
                anchor="e"
            )

    # =========================
    # ПОИСК
    # =========================

    def search_passwords(self):

        text = self.search_entry.get()

        result = self.manager.search_passwords(
        text
        )

        self.show_passwords(result)

# =========================
# ЗАПУСК
# =========================

if __name__ == "__main__":

    app = App()

    app.mainloop() 