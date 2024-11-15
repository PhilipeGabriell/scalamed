BoxLayout:
    orientation: 'vertical'

    Label:
        text: 'Escalas de Trabalho'
        font_size: '24sp'
        size_hint_y: None
        height: dp(50)

    ScrollView:
        size_hint: (1, None)
        size: (self.width, self.height - dp(50))
        GridLayout:
            id: escalas_layout
            cols: 1
            size_hint_y: None
            height: self.minimum_height

<Button>:
    size_hint_y: None
    height: dp(40)
