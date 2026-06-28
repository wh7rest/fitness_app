from auth.login import LoginWindow
from ui.main_window import MainWindow

if __name__ == "__main__":
    login = LoginWindow()
    login.run()

    if login.is_authenticated:
        app = MainWindow(login.current_user)
        app.run()
