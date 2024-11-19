from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivymd.app import MDApp
from services.firebase_service import buscar_ofertas, solicitar_troca


class OfferSwapScreen(Screen):
    def on_pre_enter(self):
        # Exibir o histórico de ofertas ao carregar a tela
        self.exibir_ofertas()

    def exibir_ofertas(self):
        self.ids.ofertas_lista.clear_widgets()
        ofertas = buscar_ofertas()

        if not ofertas or not isinstance(ofertas, dict):
            mensagem = Label(
                text="Nenhuma oferta de troca disponível.",
                size_hint_y=None,
                height=40,
                halign="center",
                valign="middle"
            )
            self.ids.ofertas_lista.add_widget(mensagem)
            return

        for oferta_id, oferta in ofertas.items():
            layout = BoxLayout(orientation="vertical", size_hint_y=None, height=140, spacing=10, padding=[10, 5, 10, 5])
            
            escala_info = oferta.get("escala_info", {})
            dia_desejado = oferta.get("dia_desejado", "Não especificado")
            usuario_id = oferta.get("usuario_id", "Desconhecido")

            escala_detalhes = (
                f"Plantão: {escala_info.get('titulo', 'Sem título')} - {escala_info.get('dia', 'Sem dia')} "
                f"às {escala_info.get('horario', 'Sem horário')}"
            )
            usuario_solicitante = f"Solicitante: {usuario_id}"
            destino_dia = f"Dia desejado: {dia_desejado}"

            # Ajustando Labels com alinhamento e quebra de linha
            label_escala = Label(
                text=escala_detalhes,
                size_hint_y=None,
                height=40,
                halign="left",
                valign="middle",
                text_size=(self.width - 40, None)  # Largura ajustada para evitar cortes
            )
            label_escala.bind(size=label_escala.setter('text_size'))

            label_origem = Label(
                text=usuario_solicitante,
                size_hint_y=None,
                height=20,
                halign="left",
                valign="middle",
                text_size=(self.width - 40, None)
            )
            label_origem.bind(size=label_origem.setter('text_size'))

            label_dia = Label(
                text=destino_dia,
                size_hint_y=None,
                height=20,
                halign="left",
                valign="middle",
                text_size=(self.width - 40, None)
            )
            label_dia.bind(size=label_dia.setter('text_size'))

            btn_solicitar = Button(text="Solicitar Troca", size_hint_y=None, height=40)
            btn_solicitar.bind(on_release=lambda instance, oid=oferta_id, oferta=oferta: self.solicitar_troca(oid, oferta))

            layout.add_widget(label_escala)
            layout.add_widget(label_origem)
            layout.add_widget(label_dia)
            layout.add_widget(btn_solicitar)

            self.ids.ofertas_lista.add_widget(layout)

    def solicitar_troca(self, oferta_id, oferta):
        usuario_id = MDApp.get_running_app().usuario_id
        if solicitar_troca(usuario_id, oferta_id, oferta):
            popup = Popup(title="Sucesso", content=Label(text="Solicitação enviada para aprovação."), size_hint=(0.8, 0.3))
            popup.open()
        else:
            popup = Popup(title="Erro", content=Label(text="Erro ao enviar solicitação."), size_hint=(0.8, 0.3))
            popup.open()
