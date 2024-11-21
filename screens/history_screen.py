from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from services.firebase_service import buscar_historico

class HistoryScreen(Screen):
    def on_pre_enter(self):
        self.exibir_historico()

    def exibir_historico(self):
        self.ids.historico_lista.clear_widgets()
        historico = buscar_historico()

        if not historico or not isinstance(historico, dict):
            mensagem = Label(
                text="Nenhum histórico encontrado.",
                size_hint_y=None,
                height=40,
                halign="center",
                valign="middle",
                color=(0, 0, 0, 1)
            )
            self.ids.historico_lista.add_widget(mensagem)
            return

        for item_id, item in historico.items():
            layout = BoxLayout(orientation="vertical", size_hint_y=None, height=120, spacing=10, padding=[10, 5, 10, 5])
            escala_info = item.get("escala_info", {})
            dia_desejado = item.get("dia_desejado", "Não especificado")
            usuario_id = item.get("usuario_id", "Desconhecido")
            status = item.get("status", "Sem status")

            escala_detalhes = (
                f"Plantão: {escala_info.get('titulo', 'Sem título')} - {escala_info.get('dia', 'Sem dia')} "
                f"às {escala_info.get('horario', 'Sem horário')}"
            )
            solicitante = f"Solicitante: {usuario_id}"
            destino_dia = f"Dia desejado: {dia_desejado}"
            status_detalhes = f"Status: {status}"

            label_escala = Label(
                text=escala_detalhes,
                size_hint_y=None,
                height=30,
                halign="left",
                valign="middle",
                text_size=(self.width - 40, None),
                color=(0, 0, 0, 1)
            )
            label_solicitante = Label(
                text=solicitante,
                size_hint_y=None,
                height=20,
                halign="left",
                valign="middle",
                text_size=(self.width - 40, None),
                color=(0, 0, 0, 1)
            )
            label_dia = Label(
                text=destino_dia,
                size_hint_y=None,
                height=20,
                halign="left",
                valign="middle",
                text_size=(self.width - 40, None),
                color=(0, 0, 0, 1)
            )
            label_status = Label(
                text=status_detalhes,
                size_hint_y=None,
                height=20,
                halign="left",
                valign="middle",
                text_size=(self.width - 40, None),
                color=(0, 0, 0, 1)
            )

            layout.add_widget(label_escala)
            layout.add_widget(label_solicitante)
            layout.add_widget(label_dia)
            layout.add_widget(label_status)

            self.ids.historico_lista.add_widget(layout)
