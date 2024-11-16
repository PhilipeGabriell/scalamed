from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from services.firebase_service import (
    autenticar_usuario,
    buscar_dias_trabalho,
    enviar_solicitacao_troca,
    buscar_ofertas_disponiveis,
    aprovar_troca_dois_usuarios,
    buscar_historico,
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
        autenticar_usuario(email, senha)
        self.manager.current = "dashboard"


class DashboardScreen(Screen):
    pass


class ScheduleScreen(Screen):
    def carregar_escalas(self):
        escalas = buscar_dias_trabalho("usuario@exemplo.com")
        self.ids.escalas_lista.text = "\n".join(escalas)


class RequestSwapScreen(Screen):
    def enviar_solicitacao(self, plantao_origem, sugestao_data):
        enviar_solicitacao_troca(plantao_origem, sugestao_data)


class ApprovalScreen(Screen):
    def carregar_aprovacoes(self):
        # Lógica para buscar aprovações pendentes
        pass


class HistoryScreen(Screen):
    def carregar_historico(self):
        historico = buscar_historico()
        self.ids.historico_lista.text = "\n".join(historico)


class OfferSwapScreen(Screen):
    def carregar_ofertas(self):
        ofertas = buscar_ofertas_disponiveis("usuario@exemplo.com")
        self.ids.ofertas_lista.text = "\n".join(ofertas)


class CalendarScreen(Screen):
    def exibir_plantao_por_dia(self, data):
        # Lógica para exibir plantões no dia selecionado
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
        sm.add_widget(OfferSwapScreen(name="offer_swap"))
        sm.add_widget(CalendarScreen(name="calendar"))
        return sm


if __name__ == "__main__":
    ScalamedApp().run()
