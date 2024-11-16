<ScheduleScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10

        Label:
            text: "Escalas Disponíveis"
            font_size: 24

        ScrollView:
            size_hint: (1, 0.8)
            GridLayout:
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                spacing: 10

                Label:
                    text: "Data: 20/11/2024 | Setor: UTI | Profissionais: João, Maria"
                Label:
                    text: "Data: 21/11/2024 | Setor: Emergência | Profissionais: Ana, Pedro"

        Button:
            text: "Voltar ao Menu Principal"
            size_hint: (1, 0.1)
            on_press: app.root.current = 'dashboard'
