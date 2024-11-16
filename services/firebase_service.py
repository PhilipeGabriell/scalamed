import firebase_admin
from firebase_admin import credentials, firestore, auth

# Inicialização do Firebase
cred = credentials.Certificate(r"C:\Users\phili\OneDrive\Área de Trabalho\Scalamed\scalamed-clean\services\scalamed-67a7d-firebase-adminsdk-4ao27-6416ca9ca9.json")
firebase_admin.initialize_app(cred)

# Conexão com o Firestore
db = firestore.client()

def autenticar_usuario(email, senha):
    """Autentica o usuário com email e senha."""
    try:
        user = auth.get_user_by_email(email)
        if user:
            print(f"Usuário {email} autenticado com sucesso.")
            return True
    except Exception as e:
        print(f"Erro ao autenticar usuário: {e}")
        return False

def buscar_escalas():
    """Busca as escalas dos funcionários no Firestore."""
    try:
        escalas_ref = db.collection("escalas").stream()
        escalas = [f"{doc.id}: {doc.to_dict()}" for doc in escalas_ref]
        return escalas
    except Exception as e:
        print(f"Erro ao buscar escalas: {e}")
        return []

def enviar_solicitacao_troca(data, turno, novo_turno):
    """Envia uma solicitação de troca de turno."""
    try:
        troca = {
            "data": data,
            "turno": turno,
            "novo_turno": novo_turno,
            "status": "pendente",
        }
        db.collection("solicitacoes").add(troca)
        print("Solicitação de troca enviada com sucesso.")
    except Exception as e:
        print(f"Erro ao enviar solicitação de troca: {e}")

def aprovar_troca(solicitacao_id):
    """Aprova uma troca de turno."""
    try:
        solicitacao_ref = db.collection("solicitacoes").document(solicitacao_id)
        solicitacao_ref.update({"status": "aprovado"})
        print(f"Solicitação {solicitacao_id} aprovada com sucesso.")
    except Exception as e:
        print(f"Erro ao aprovar troca: {e}")

def visualizar_historico():
    """Visualiza o histórico de trocas."""
    try:
        historico_ref = db.collection("historico").stream()
        historico = [f"{doc.id}: {doc.to_dict()}" for doc in historico_ref]
        return historico
    except Exception as e:
        print(f"Erro ao visualizar histórico: {e}")
        return []

def oferecer_troca(data, turno):
    """Oferece uma troca de turno."""
    try:
        oferta = {
            "data": data,
            "turno": turno,
            "status": "aberta",
        }
        db.collection("ofertas").add(oferta)
        print("Troca de turno oferecida com sucesso.")
    except Exception as e:
        print(f"Erro ao oferecer troca: {e}")

def buscar_calendario_plantao():
    """Busca o calendário com os plantões por data."""
    try:
        calendario_ref = db.collection("calendario").stream()
        calendario = {doc.id: doc.to_dict() for doc in calendario_ref}
        return calendario
    except Exception as e:
        print(f"Erro ao buscar calendário de plantões: {e}")
        return {}
