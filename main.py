from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from services.firebase_service import (
    autenticar_usuario,
    buscar_escalas,
    enviar_solicitacao_troca,
    aprovar_troca,
    visualizar_historico,
)

# Carregar arquivos KV
Builder.load_file("screens/login_screen.kv")
Builder.load_file("screens/dashboard_screen.kv")
Builder.load_file("screens/schedule_screen.kv")
Builder.load_file("screens/request_swap_screen.kv")
Builder.load_file("screens/approval_screen.kv")
Builder.load_file("screens/history_screen.kv")

# Telas do aplicativo
class LoginScreen(Screen):
    pass

class DashboardScreen(Screen):
    pass

class ScheduleScreen(Screen):
    pass

class RequestSwapScreen(Screen):
    pass

class ApprovalScreen(Screen):
    pass

class HistoryScreen(Screen):
    pass

# Gerenciador de telas
class ScalamedApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(DashboardScreen(name="dashboard"))
        sm.add_widget(ScheduleScreen(name="schedule"))
        sm.add_widget(RequestSwapScreen(name="request_swap"))
        sm.add_widget(ApprovalScreen(name="approval"))
        sm.add_widget(HistoryScreen(name="history"))
        return sm

if __name__ == "__main__":
    ScalamedApp().run()
