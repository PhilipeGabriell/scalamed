from kivy.uix.screenmanager import Screen

class ScheduleScreen(Screen):
    def __init__(self, **kwargs):
        super(ScheduleScreen, self).__init__(**kwargs)

    def carregar_escalas(self):
        # Função para carregar escalas do funcionário
        escalas = buscar_escalas()
        print(f"Escalas carregadas: {escalas}")
