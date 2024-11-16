from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from services.firebase_service import (
    autenticar_usuario,
    buscar_escalas,
    enviar_solicitacao_troca,
    aprovar_troca,
    visualizar_historico,
    oferecer_troca,
    buscar_calendario_plantao,
)

# Carregar arquivos KV
Builder.load_file("screens/login_screen.kv")
Builder.load_file("screens/dashboard_screen.kv")
Builder.load_file("screens/schedule_screen.kv")
Builder.load_file("screens/request_swap_screen.kv")
Builder.load_file("screens/approval_screen.kv")
Builder.load_file("screens/history_screen.kv")
Builder.load_file("screens/offer_swap_screen.kv")
Builder.load_file("screens/calendar_screen.kv")

# Telas do aplicativo
class LoginScreen(Screen):
    def fazer_login(self, email, senha):
        if autenticar_usuario(email, senha):
            self.manager.current = "dashboard"
        else:
            self.ids.login_status.text = "Login falhou. Verifique suas credenciais."

class DashboardScreen(Screen):
    pass

class ScheduleScreen(Screen):
    def carregar_escalas(self):
        escalas = buscar_escalas()
        self.ids.escalas_lista.text = "\n".join(escalas)

class RequestSwapScreen(Screen):
    def enviar_solicitacao(self, data, turno):
        enviar_solicitacao_troca(data, turno)

class ApprovalScreen(Screen):
    def carregar_aprovacoes(self):
        aprovacoes = aprovar_troca()
        self.ids.aprovacoes_lista.text = "\n".join(aprovacoes)

class HistoryScreen(Screen):
    def carregar_historico(self):
        historico = visualizar_historico()
        self.ids.historico_lista.text = "\n".join(historico)

class OfferSwapScreen(Screen):
    def oferecer_troca(self, data, turno):
        oferecer_troca(data, turno)

class CalendarScreen(Screen):
    def carregar_calendario(self):
        calendario = buscar_calendario_plantao()
        # Exibir os dados do calendário
        self.ids.calendario_lista.text = "\n".join(
            f"{data}: {info}" for data, info in calendario.items()
        )

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
        sm.add_widget(OfferSwapScreen(name="offer_swap"))
        sm.add_widget(CalendarScreen(name="calendar"))
        return sm

if __name__ == "__main__":
    ScalamedApp().run()
