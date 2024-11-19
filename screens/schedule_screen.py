from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.label import Label
from services.firebase_service import salvar_escala, buscar_escalas, alterar_escala, deletar_escala

class ScheduleScreen(Screen):
    def on_pre_enter(self):
        usuario_id = MDApp.get_running_app().usuario_id  # Suporte ao usuário logado
        escalas = buscar_escalas(usuario_id)
        self.exibir_escalas(escalas)

    def exibir_escalas(self, escalas):
        self.ids.escalas_lista.clear_widgets()  # Limpar widgets antigos

        if not escalas or not isinstance(escalas, dict):
            # Exibir mensagem padrão caso não haja escalas
            mensagem = Label(
                text="Nenhuma escala cadastrada.",
                size_hint_y=None,
                height=40,
                halign="center",
                valign="middle"
            )
            self.ids.escalas_lista.add_widget(mensagem)
            return

        # Criar layout para cada escala
        for escala_id, esc in escalas.items():
            layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=40)
            label = Label(
                text=f"{esc['titulo']} - {esc['dia']} às {esc['horario']} "
                     f"{'(Repetir: ' + esc.get('repetir', '') + ')' if esc.get('repetir') else ''}",
                size_hint_x=0.6,
                halign="left",
                valign="middle"
            )
            label.bind(size=label.setter('text_size'))  # Ajustar quebra de linha

            btn_edit = Button(text="Editar", size_hint_x=0.2)
            btn_delete = Button(text="Deletar", size_hint_x=0.2)

            # Bind dos botões com os métodos de edição e exclusão
            btn_edit.bind(on_release=lambda instance, eid=escala_id: self.alterar_escala(eid, esc))
            btn_delete.bind(on_release=lambda instance, eid=escala_id: self.deletar_escala(eid))

            # Adicionar widgets ao layout
            layout.add_widget(label)
            layout.add_widget(btn_edit)
            layout.add_widget(btn_delete)

            # Adicionar o layout ao container principal
            self.ids.escalas_lista.add_widget(layout)

    def cadastrar_escala(self):
        self._abrir_popup_escala()

    def alterar_escala(self, escala_id, escala):
        self._abrir_popup_escala(escala_id=escala_id, escala=escala)

    def deletar_escala(self, escala_id):
        def confirmar_delecao(instance):
            usuario_id = MDApp.get_running_app().usuario_id
            deletar_escala(usuario_id, escala_id)
            self.on_pre_enter()
            popup.dismiss()

        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        label = Label(text="Deseja realmente excluir esta escala?")
        btn_confirm = Button(text="Sim", size_hint_y=None, height=40)
        btn_cancel = Button(text="Cancelar", size_hint_y=None, height=40)

        btn_confirm.bind(on_release=confirmar_delecao)
        btn_cancel.bind(on_release=lambda instance: popup.dismiss())

        layout.add_widget(label)
        layout.add_widget(btn_confirm)
        layout.add_widget(btn_cancel)

        popup = Popup(title="Confirmar Exclusão", content=layout, size_hint=(0.8, 0.4))
        popup.open()

    def _abrir_popup_escala(self, escala_id=None, escala=None):
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        titulo_input = TextInput(hint_text="Título/Descrição", text=escala.get("titulo", "") if escala else "")
        dia_input = TextInput(hint_text="Dia (ex: Segunda-feira)", text=escala.get("dia", "") if escala else "")
        horario_input = TextInput(hint_text="Horário (ex: 08:00-12:00)", text=escala.get("horario", "") if escala else "")
        repetir_spinner = Spinner(
            text=escala.get("repetir", "Sem Repetição") if escala else "Sem Repetição",
            values=["Sem Repetição", "Diariamente", "Semanalmente", "Mensalmente"],
        )

        btn_save = Button(text="Salvar", size_hint_y=None, height=40)
        btn_cancel = Button(text="Cancelar", size_hint_y=None, height=40)

        def salvar_alteracoes(instance):
            usuario_id = MDApp.get_running_app().usuario_id
            escala_data = {
                "titulo": titulo_input.text.strip(),
                "dia": dia_input.text.strip(),
                "horario": horario_input.text.strip(),
                "repetir": repetir_spinner.text if repetir_spinner.text != "Sem Repetição" else None,
            }
            if all(escala_data.values()):
                if escala_id:
                    alterar_escala(usuario_id, escala_id, escala_data)
                else:
                    salvar_escala(usuario_id, escala_data)
                self.on_pre_enter()
                popup.dismiss()

        btn_save.bind(on_release=salvar_alteracoes)
        btn_cancel.bind(on_release=lambda instance: popup.dismiss())

        layout.add_widget(Label(text="Cadastrar Nova Escala" if not escala_id else "Alterar Escala"))
        layout.add_widget(titulo_input)
        layout.add_widget(dia_input)
        layout.add_widget(horario_input)
        layout.add_widget(repetir_spinner)
        layout.add_widget(btn_save)
        layout.add_widget(btn_cancel)

        popup = Popup(title="Cadastrar/Alterar Escala", content=layout, size_hint=(0.8, 0.7))
        popup.open()
