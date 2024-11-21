from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from services.firebase_service import cadastrar_funcionario

class RegisterScreen(Screen):
    def on_pre_enter(self):
        """Configura o fundo da tela para o padrão do sistema."""
        self.update_background()  # Atualiza o fundo da tela

    def update_background(self):
        """Configura o fundo da tela."""
        from kivy.graphics import Color, Rectangle

        with self.canvas.before:
            # Remove qualquer objeto anterior no canvas
            Color(0.6, 0.9, 0.6, 1)  # Verde claro
            self.rect = Rectangle(size=self.size, pos=self.pos)
        
        # Atualiza a posição e o tamanho do fundo ao redimensionar
        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        """Atualiza o fundo quando a tela for redimensionada."""
        self.rect.pos = self.pos
        self.rect.size = self.size

    def realizar_cadastro(self):
        nome = self.ids.nome_input.text.strip()
        email = self.ids.email_input.text.strip()
        senha = self.ids.senha_input.text.strip()

        if nome and email and senha:
            sucesso = cadastrar_funcionario(nome, email, senha)
            if sucesso:
                self.manager.current = 'login'  # Voltar para a tela de login após cadastro
            else:
                self.show_popup("Erro", "Erro ao cadastrar funcionário.")
        else:
            self.show_popup("Erro", "Preencha todos os campos!")

    def show_popup(self, title, message):
        """Exibe um popup simples com título e mensagem."""
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.3))
        popup.open()
