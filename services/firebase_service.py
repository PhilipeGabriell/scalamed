# services/firebase_service.py
import firebase_admin
from firebase_admin import credentials, firestore, auth

# Carregar as credenciais do arquivo JSON
cred = credentials.Certificate(r"C:\Users\phili\OneDrive\Área de Trabalho\Scalamed\services\scalamed-67a7d-firebase-adminsdk-4ao27-6416ca9ca9.json")

# Inicializar o aplicativo Firebase
firebase_admin.initialize_app(cred)

# Conectar ao Firestore
db = firestore.client()

def autenticar_usuario(email, senha):
    try:
        user = auth.get_user_by_email(email)
        return user.uid
    except firebase_admin._auth_utils.UserNotFoundError:
        print("Usuário não encontrado.")
        return None
    except Exception as e:
        print(f"Erro ao autenticar usuário: {e}")
        return None

def listar_escalas():
    try:
        escalas = db.collection('escalas').get()
        return [escala.to_dict() for escala in escalas]
    except Exception as e:
        print("Erro ao listar escalas:", e)
        return []

def solicitar_troca(turno_desejado, setor_desejado):
    try:
        dados_troca = {
            "data_solicitacao": firestore.SERVER_TIMESTAMP,
            "turno_desejado": turno_desejado,
            "setor_desejado": setor_desejado,
            "status": "pendente"
        }
        db.collection('trocas').add(dados_troca)
        return True
    except Exception as e:
        print(f"Erro ao solicitar troca: {e}")
        return False

def listar_solicitacoes_troca():
    try:
        solicitacoes = db.collection('trocas').get()
        return [{"id": solicitacao.id, **solicitacao.to_dict()} for solicitacao in solicitacoes]
    except Exception as e:
        print("Erro ao listar solicitações de troca:", e)
        return []

def atualizar_status_solicitacao(solicitacao_id, novo_status):
    try:
        db.collection('trocas').document(solicitacao_id).update({"status": novo_status})
        print(f"Solicitação {solicitacao_id} atualizada para {novo_status}")
    except Exception as e:
        print("Erro ao atualizar status da solicitação:", e)
