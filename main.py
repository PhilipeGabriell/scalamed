
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from screens.login_screen import LoginScreen
from screens.dashboard_screen import DashboardScreen
from screens.schedule_screen import ScheduleScreen
from services.firebase_service import autenticar_usuario
from screens.request_swap_screen import RequestSwapScreen
from screens.offer_swap_screen import OfferSwapScreen
from screens.approvals_pending_screen import ApprovalsPendingScreen
from screens.history_screen import HistoryScreen
from screens.register_screen import RegisterScreen

# Carregar arquivos KV
Builder.load_file("screens/login_screen.kv")
Builder.load_file("screens/dashboard_screen.kv")
Builder.load_file("screens/schedule_screen.kv")
Builder.load_file("screens/request_swap_screen.kv")
Builder.load_file("screens/offer_swap_screen.kv")
Builder.load_file("screens/approvals_pending_screen.kv")
Builder.load_file("screens/history_screen.kv")
Builder.load_file("screens/register_screen.kv")

class ScalamedApp(MDApp):
    usuario_id = None

class ScalamedApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"  # Cor primária
        self.theme_cls.accent_palette = "Green"  # Cor secundária
        self.theme_cls.theme_style = "Light"  # Ou "Dark" para tema escuro
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(ScheduleScreen(name="schedule"))
        sm.add_widget(DashboardScreen(name="dashboard"))
        sm.add_widget(RequestSwapScreen(name="request_swap"))
        sm.add_widget(OfferSwapScreen(name="offer_swap"))
        sm.add_widget(ApprovalsPendingScreen(name="approvals_pending"))
        sm.add_widget(HistoryScreen(name="history"))
        sm.add_widget(RegisterScreen(name="register"))
        return sm


if __name__ == "__main__":
    ScalamedApp().run()
