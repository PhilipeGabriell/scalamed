from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivymd.app import MDApp
from services.firebase_service import salvar_oferta, buscar_escalas

class RequestSwapScreen(Screen):
    def on_pre_enter(self):
        usuario_id = MDApp.get_running_app().usuario_id
        self.escalas = buscar_escalas(usuario_id)
    
    def add_offer(self):
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        
        if not self.escalas or not isinstance(self.escalas, dict):
            popup = Popup(title="Aviso", content=Label(text="Você não tem escalas para oferecer."), size_hint=(0.8, 0.3))
            popup.open()
            return
        
        escalas_options = []
        escala_ids = []
        for escala_id, esc in self.escalas.items():
            escala_str = f"{esc['titulo']} - {esc['dia']} às {esc['horario']}"
            escalas_options.append(escala_str)
            escala_ids.append(escala_id)
        
        escala_spinner = Spinner(
            text="Selecione uma escala",
            values=escalas_options,
            size_hint_y=None,
            height=44
        )
        
        dia_desejado_input = TextInput(hint_text="Dia desejado para troca", size_hint_y=None, height=44)
        
        btn_submit = Button(text="Adicionar Oferta", size_hint_y=None, height=50)
        btn_cancel = Button(text="Cancelar", size_hint_y=None, height=50)
        
        def submit_offer(instance):
            if escala_spinner.text == "Selecione uma escala":
                error_popup = Popup(title="Aviso", content=Label(text="Por favor, selecione uma escala."), size_hint=(0.8, 0.3))
                error_popup.open()
                return

            selected_index = escala_spinner.values.index(escala_spinner.text)
            escala_id = escala_ids[selected_index]
            escala = self.escalas[escala_id]
            dia_desejado = dia_desejado_input.text.strip()
            if dia_desejado:
                usuario_id = MDApp.get_running_app().usuario_id
                oferta = {
                    "escala_id": escala_id,
                    "escala_info": escala,
                    "dia_desejado": dia_desejado,
                    "usuario_id": usuario_id
                }
                if salvar_oferta(oferta):
                    popup.dismiss()
                    success_popup = Popup(title="Sucesso", content=Label(text="Oferta adicionada com sucesso!"), size_hint=(0.8, 0.3))
                    success_popup.open()
                else:
                    error_popup = Popup(title="Erro", content=Label(text="Erro ao adicionar oferta."), size_hint=(0.8, 0.3))
                    error_popup.open()
            else:
                error_popup = Popup(title="Aviso", content=Label(text="Por favor, insira o dia desejado para troca."), size_hint=(0.8, 0.3))
                error_popup.open()
        
        btn_submit.bind(on_release=submit_offer)
        btn_cancel.bind(on_release=lambda instance: popup.dismiss())
        
        layout.add_widget(Label(text="Adicionar Oferta de Troca"))
        layout.add_widget(escala_spinner)
        layout.add_widget(dia_desejado_input)
        layout.add_widget(btn_submit)
        layout.add_widget(btn_cancel)
        
        popup = Popup(title="Adicionar Oferta", content=layout, size_hint=(0.8, 0.7))
        popup.open()
