from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from services.firebase_service import (
    buscar_aprovacoes,
    atualizar_status_solicitacao,
    adicionar_nova_escala,
    remover_escala,
    mover_para_historico,
    buscar_nome_usuario,
)

class ApprovalsPendingScreen(Screen):
    def on_pre_enter(self):
        self.exibir_aprovacoes()

    def exibir_aprovacoes(self):
        self.ids.aprovacoes_lista.clear_widgets()
        aprovacoes = buscar_aprovacoes()

        if not aprovacoes or not isinstance(aprovacoes, dict):
            mensagem = Label(
                text="Nenhuma aprovação pendente.",
                size_hint_y=None,
                height=40,
                halign="center",
                valign="middle",
                color=(0, 0, 0, 1)
            )
            self.ids.aprovacoes_lista.add_widget(mensagem)
            return

        for aprovacao_id, aprovacao in aprovacoes.items():
            layout = BoxLayout(orientation="vertical", size_hint_y=None, height=180, spacing=10, padding=10)
            
            escala_info = aprovacao.get("escala_info", {})
            dia_desejado = aprovacao.get("dia_desejado", "Não especificado")
            solicitante_id = aprovacao.get("usuario_id")
            ofertante_id = aprovacao.get("oferta_usuario_id")

            nome_solicitante = buscar_nome_usuario(solicitante_id)
            nome_ofertante = buscar_nome_usuario(ofertante_id)

            escala_detalhes = (
                f"Plantão: {escala_info.get('titulo', 'Sem título')} - {escala_info.get('dia', 'Sem dia')} "
                f"às {escala_info.get('horario', 'Sem horário')}"
            )
            detalhes_solicitante = f"Solicitante: {nome_solicitante}"
            detalhes_ofertante = f"Ofertante: {nome_ofertante}"
            destino_dia = f"Dia desejado: {dia_desejado}"

            label_escala = Label(
                text=escala_detalhes,
                size_hint_y=None,
                height=40,
                halign="left",
                valign="middle",
                text_size=(self.width - 40, None),
                color=(0, 0, 0, 1)o
            )
            label_solicitante = Label(
                text=detalhes_solicitante,
                size_hint_y=None,
                height=20,
                halign="left",
                valign="middle",
                text_size=(self.width - 40, None),
                color=(0, 0, 0, 1)
            )
            label_ofertante = Label(
                text=detalhes_ofertante,
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

            btn_aprovar = Button(text="Aprovar", size_hint_y=None, height=40, background_normal='', background_color=(0.3, 0.5, 1, 1), color=(1, 1, 1, 1))
            btn_aprovar.bind(on_release=lambda instance, aid=aprovacao_id, ainfo=aprovacao: self.aprovar_solicitacao(aid, ainfo))

            btn_rejeitar = Button(text="Rejeitar", size_hint_y=None, height=40, background_normal='', background_color=(1, 0, 0, 1), color=(1, 1, 1, 1))
            btn_rejeitar.bind(on_release=lambda instance, aid=aprovacao_id, ainfo=aprovacao: self.rejeitar_solicitacao(aid, ainfo))

            layout.add_widget(label_escala)
            layout.add_widget(label_solicitante)
            layout.add_widget(label_ofertante)
            layout.add_widget(label_dia)
            layout.add_widget(btn_aprovar)
            layout.add_widget(btn_rejeitar)

            self.ids.aprovacoes_lista.add_widget(layout)

    def aprovar_solicitacao(self, aprovacao_id, aprovacao):
        ofertante_id = aprovacao.get("oferta_usuario_id")
        solicitante_id = aprovacao.get("usuario_id")
        escala_id = aprovacao.get("escala_id")
        nova_escala = aprovacao.get("escala_info", {})
        dia_desejado = aprovacao.get("dia_desejado", "Não especificado")

        nova_escala["dia"] = dia_desejado

        if (
            adicionar_nova_escala(solicitante_id, nova_escala)
            and remover_escala(ofertante_id, escala_id)
        ):
            mover_para_historico(aprovacao_id, "Aprovada", aprovacao)
            popup = Popup(title="Sucesso", content=Label(text="Solicitação aprovada!"), size_hint=(0.8, 0.3))
            popup.open()
            self.on_pre_enter()
        else:
            popup = Popup(title="Erro", content=Label(text="Erro ao aprovar solicitação."), size_hint=(0.8, 0.3))
            popup.open()

    def rejeitar_solicitacao(self, aprovacao_id, aprovacao):
        if mover_para_historico(aprovacao_id, "Rejeitada", aprovacao):
            popup = Popup(title="Sucesso", content=Label(text="Solicitação rejeitada!"), size_hint=(0.8, 0.3))
            popup.open()
            self.on_pre_enter()
        else:
            popup = Popup(title="Erro", content=Label(text="Erro ao rejeitar solicitação."), size_hint=(0.8, 0.3))
            popup.open()
