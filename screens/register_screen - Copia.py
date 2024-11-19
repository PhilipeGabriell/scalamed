from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from services.firebase_service import cadastrar_funcionario

class RegisterScreen(Screen):
    def cadastrar_funcionario(self):
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        nome_input = TextInput(hint_text="Nome do Funcionário")
        email_input = TextInput(hint_text="Email do Funcionário")
        senha_input = TextInput(hint_text="Senha", password=True)

        btn_cadastrar = Button(text="Cadastrar", size_hint_y=None, height=40)
        btn_cancelar = Button(text="Cancelar", size_hint_y=None, height=40)

        def realizar_cadastro(instance):
            nome = nome_input.text.strip()
            email = email_input.text.strip()
            senha = senha_input.text.strip()

            if nome and email and senha:
                sucesso = cadastrar_funcionario(nome, email, senha)
                if sucesso:
                    popup.dismiss()
                    Popup(title="Sucesso", content=Label(text="Funcionário cadastrado com sucesso!"), size_hint=(0.8, 0.3)).open()
                else:
                    Popup(title="Erro", content=Label(text="Erro ao cadastrar funcionário."), size_hint=(0.8, 0.3)).open()
            else:
                Popup(title="Erro", content=Label(text="Preencha todos os campos!"), size_hint=(0.8, 0.3)).open()

        btn_cadastrar.bind(on_release=realizar_cadastro)
        btn_cancelar.bind(on_release=lambda instance: popup.dismiss())

        layout.add_widget(Label(text="Cadastrar Funcionário"))
        layout.add_widget(nome_input)
        layout.add_widget(email_input)
        layout.add_widget(senha_input)
        layout.add_widget(btn_cadastrar)
        layout.add_widget(btn_cancelar)

        popup = Popup(title="Cadastro de Funcionário", content=layout, size_hint=(0.8, 0.7))
        popup.open()
