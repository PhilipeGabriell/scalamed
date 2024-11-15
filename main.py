# main.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from services.firebase_service import (
    autenticar_usuario,
    listar_escalas,
    solicitar_troca,
    listar_solicitacoes_troca,
    atualizar_status_solicitacao
)

# Carregar arquivos .kv para definir o layout das telas
Builder.load_file("screens/login_screen.kv")
Builder.load_file("screens/dashboard_screen.kv")
Builder.load_file("screens/schedule_screen.kv")
Builder.load_file("screens/request_swap_screen.kv")
Builder.load_file("screens/approve_requests_screen.kv")

class LoginScreen(Screen):
    def fazer_login(self, email, senha):
        try:
            uid = autenticar_usuario(email, senha)
            if uid:
                self.manager.current = "dashboard"
                self.ids.mensagem.text = ""
            else:
                self.ids.mensagem.text = "Erro: Credenciais inválidas."
        except Exception as e:
            print(f"Erro ao tentar fazer login: {e}")
            self.ids.mensagem.text = "Erro ao fazer login. Verifique o console."

class DashboardScreen(Screen):
    pass

class ScheduleScreen(Screen):
    def on_enter(self):
        self.ids.escala_box.clear_widgets()
        escalas = listar_escalas()
        for escala in escalas:
            self.ids.escala_box.add_widget(
                Label(text=f"Data: {escala['data']} - Turno: {escala['turno']} - Setor: {escala['setor']}")
            )

class RequestSwapScreen(Screen):
    def enviar_solicitacao(self, turno_desejado, setor_desejado):
        try:
            resultado = solicitar_troca(turno_desejado, setor_desejado)
            if resultado:
                self.ids.mensagem.text = "Solicitação de troca enviada com sucesso."
            else:
                self.ids.mensagem.text = "Erro ao enviar a solicitação."
        except Exception as e:
            print(f"Erro ao enviar solicitação de troca: {e}")
            self.ids.mensagem.text = "Erro ao enviar solicitação. Verifique o console."

class ApproveRequestsScreen(Screen):
    def on_enter(self):
        self.ids.requests_box.clear_widgets()
        solicitacoes = listar_solicitacoes_troca()
        for solicitacao in solicitacoes:
            box = BoxLayout(orientation='horizontal', spacing=10)
            box.add_widget(Label(text=f"Turno: {solicitacao['turno_desejado']} - Setor: {solicitacao['setor_desejado']} - Status: {solicitacao['status']}"))
            box.add_widget(Button(text="Aprovar", on_release=lambda x, id=solicitacao['id']: self.aprovar_solicitacao(id)))
            box.add_widget(Button(text="Rejeitar", on_release=lambda x, id=solicitacao['id']: self.rejeitar_solicitacao(id)))
            self.ids.requests_box.add_widget(box)

    def aprovar_solicitacao(self, solicitacao_id):
        atualizar_status_solicitacao(solicitacao_id, "aprovado")
        self.on_enter()

    def rejeitar_solicitacao(self, solicitacao_id):
        atualizar_status_solicitacao(solicitacao_id, "rejeitado")
        self.on_enter()

class ScreenManagement(ScreenManager):
    pass

class ScalamedApp(App):
    def build(self):
        sm = ScreenManagement()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(DashboardScreen(name="dashboard"))
        sm.add_widget(ScheduleScreen(name="schedule"))
        sm.add_widget(RequestSwapScreen(name="request_swap"))
        sm.add_widget(ApproveRequestsScreen(name="approve_requests"))
        return sm

if __name__ == "__main__":
    ScalamedApp().run()
