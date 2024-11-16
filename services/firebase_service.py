import firebase_admin
from firebase_admin import credentials, firestore, auth

# Configuração do Firebase
cred = credentials.Certificate(r"C:\Users\phili\OneDrive\Área de Trabalho\Scalamed\scalamed-clean\services\scalamed-67a7d-firebase-adminsdk-4ao27-6416ca9ca9.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def autenticar_usuario(email, senha):
    try:
        user = auth.get_user_by_email(email)
        # Simulação de autenticação
        return {"email": user.email, "uid": user.uid}
    except Exception as e:
        print(f"Erro ao autenticar usuário: {e}")
        return None

def buscar_escalas():
    try:
        escalas = db.collection("escalas").get()
        return [doc.to_dict() for doc in escalas]
    except Exception as e:
        print(f"Erro ao buscar escalas: {e}")
        return []

def enviar_solicitacao_troca(dados):
    try:
        db.collection("trocas").add(dados)
        print("Solicitação enviada com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar solicitação: {e}")

def aprovar_troca(troca_id):
    try:
        troca = db.collection("trocas").document(troca_id)
        troca.update({"status": "aprovado"})
        print("Troca aprovada!")
    except Exception as e:
        print(f"Erro ao aprovar troca: {e}")

def visualizar_historico():
    try:
        historico = db.collection("historico").get()
        return [doc.to_dict() for doc in historico]
    except Exception as e:
        print(f"Erro ao buscar histórico: {e}")
        return []
