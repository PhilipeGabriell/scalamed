<ScheduleScreen>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: "Minhas Escalas"
        Button:
            text: "Voltar ao Menu Principal"
            on_press: app.root.current = 'dashboard'
