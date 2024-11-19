import firebase_admin
from firebase_admin import credentials, db, auth

# Firebase configuration
cred = credentials.Certificate(r"C:\Users\phili\OneDrive\Área de Trabalho\Scalamed\services\scalamed-67a7d-firebase-adminsdk-4ao27-579621fb1c.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://scalamed-67a7d-default-rtdb.firebaseio.com"
})

# Functionality to authenticate users
def autenticar_usuario(email, senha):
    try:
        user = auth.get_user_by_email(email)
        # Simulated password verification (Admin SDK doesn't directly verify passwords)
        if user:
            return user.uid
        return None
    except Exception as e:
        print(f"Erro ao autenticar usuário: {e}")
        return None

# Functionality to manage schedules
def salvar_escala(usuario_id, escala):
    try:
        ref = db.reference(f"usuarios/{usuario_id}/escalas")
        ref.push(escala)
        return True
    except Exception as e:
        print(f"Erro ao salvar escala: {e}")
        return False

def buscar_escalas(usuario_id):
    try:
        ref = db.reference(f"usuarios/{usuario_id}/escalas")
        result = ref.get()
        return result if isinstance(result, dict) else {}
    except Exception as e:
        print(f"Erro ao buscar escalas: {e}")
        return {}

def alterar_escala(usuario_id, escala_id, escala):
    try:
        ref = db.reference(f"usuarios/{usuario_id}/escalas/{escala_id}")
        ref.update(escala)
        return True
    except Exception as e:
        print(f"Erro ao alterar escala: {e}")
        return False

def deletar_escala(usuario_id, escala_id):
    try:
        ref = db.reference(f"usuarios/{usuario_id}/escalas/{escala_id}")
        ref.delete()
        return True
    except Exception as e:
        print(f"Erro ao deletar escala: {e}")
        return False
def salvar_oferta(oferta):
    try:
        ref = db.reference("ofertas")
        ref.push(oferta)
        return True
    except Exception as e:
        print(f"Erro ao salvar oferta: {e}")
        return False
def buscar_ofertas():
    try:
        ref = db.reference("ofertas")
        ofertas = ref.get()
        return ofertas if isinstance(ofertas, dict) else {}
    except Exception as e:
        print(f"Erro ao buscar ofertas: {e}")
        return {}
def solicitar_troca(usuario_id, oferta_id, oferta):
    try:
        ref = db.reference("aprovacoes_pendentes")
        solicitacao = {
            "usuario_id": usuario_id,
            "oferta_id": oferta_id,
            "escala_info": oferta.get("escala_info", {}),
            "dia_desejado": oferta.get("dia_desejado", "Não especificado"),
            "status": "Pendente"
        }
        ref.push(solicitacao)
        return True
    except Exception as e:
        print(f"Erro ao solicitar troca: {e}")
        return False
def buscar_aprovacoes():
    try:
        ref = db.reference("aprovacoes_pendentes")
        aprovacoes = ref.get()
        return aprovacoes if isinstance(aprovacoes, dict) else {}
    except Exception as e:
        print(f"Erro ao buscar aprovações: {e}")
        return {}
def atualizar_status_solicitacao(aprovacao_id, status):
    try:
        ref = db.reference(f"aprovacoes_pendentes/{aprovacao_id}")
        ref.update({"status": status})
        return True
    except Exception as e:
        print(f"Erro ao atualizar status da solicitação: {e}")
        return False


def adicionar_nova_escala(usuario_id, escala):
    """
    Adiciona uma nova escala ao usuário no banco de dados.
    """
    try:
        ref = db.reference(f"usuarios/{usuario_id}/escalas")
        ref.push(escala)  # Adiciona a escala sem duplicar horários
        return True
    except Exception as e:
        print(f"Erro ao adicionar nova escala: {e}")
        return False

def buscar_nome_usuario(usuario_id):
    """
    Busca o nome do usuário a partir do seu ID.
    """
    try:
        ref = db.reference(f"usuarios/{usuario_id}/nome")
        nome = ref.get()
        return nome if nome else "Usuário Desconhecido"
    except Exception as e:
        print(f"Erro ao buscar nome do usuário: {e}")
        return "Usuário Desconhecido"

def remover_escala(usuario_id, escala_id):
    """
    Remove um plantão do usuário ofertante.
    """
    try:
        ref = db.reference(f"usuarios/{usuario_id}/escalas/{escala_id}")
        ref.delete()
        return True
    except Exception as e:
        print(f"Erro ao remover escala: {e}")
        return False
def buscar_historico():
    """
    Busca o histórico de aprovações e rejeições.
    """
    try:
        ref = db.reference("historico")
        return ref.get()
    except Exception as e:
        print(f"Erro ao buscar histórico: {e}")
        return {}
def mover_para_historico(aprovacao_id, status, aprovacao):
    """
    Move a solicitação aprovada ou rejeitada para o histórico.
    """
    try:
        aprovacao["status"] = status
        historico_ref = db.reference("historico")
        historico_ref.push(aprovacao)  # Adiciona ao histórico
        ref = db.reference(f"aprovacoes_pendentes/{aprovacao_id}")
        ref.delete()  # Remove das pendentes
        return True
    except Exception as e:
        print(f"Erro ao mover para histórico: {e}")
        return False
def cadastrar_funcionario(nome, email, senha):
    """
    Cadastra um novo funcionário no Firebase Authentication e no banco de dados.
    """
    try:
        user = auth.create_user(email=email, password=senha)
        usuario_id = user.uid

        ref = db.reference(f"usuarios/{usuario_id}")
        ref.set({
            "nome": nome,
            "email": email,
            "tipo": "funcionario" 
        })
        return True
    except Exception as e:
        print(f"Erro ao cadastrar funcionário: {e}")
        return False