
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivymd.app import MDApp
from services.firebase_service import autenticar_usuario

class LoginScreen(Screen):
    def fazer_login(self, email, senha):
        try:
            usuario_id = autenticar_usuario(email, senha)
            if usuario_id:
                MDApp.get_running_app().usuario_id = usuario_id
                self.manager.current = "dashboard"
            else:
                self.exibir_erro("Usuário ou senha incorretos.")
        except Exception as e:
            self.exibir_erro(f"Erro ao realizar login: {str(e)}")

    def exibir_erro(self, mensagem):
        popup = Popup(
            title="Erro de Login",
            content=Label(text=mensagem),
            size_hint=(0.8, 0.4),
        )
        popup.open()
