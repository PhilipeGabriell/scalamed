# test_firebase.py
from services.firebase_service import (
    teste_conexao,
    cadastrar_profissional,
    buscar_profissional,
    cadastrar_escala,
    listar_escalas,
    solicitar_troca,
    atualizar_status_troca
)

# Teste de conexão com o Firestore
print("=== Teste de Conexão ===")
teste_conexao()
print("\n")

# Teste de cadastro de um novo profissional
print("=== Teste de Cadastro de Profissional ===")
dados_profissional = {
    "nome": "João da Silva",
    "especialidade": "Enfermeiro",
    "registro": "123456",
    "email": "joao.silva@exemplo.com",
    "senha": "senhaSegura",
    "setor_atual": "Emergência",
    "turnos": ["manhã", "tarde"]
}
uid = cadastrar_profissional(dados_profissional)
print(f"UID do novo profissional: {uid}")
print("\n")

# Teste de busca de profissional pelo UID
print("=== Teste de Busca de Profissional ===")
profissional = buscar_profissional(uid)
print(f"Dados do profissional: {profissional}")
print("\n")

# Teste de cadastro de uma nova escala
print("=== Teste de Cadastro de Escala ===")
dados_escala = {
    "data": "2024-11-15",
    "turno": "manhã",
    "especialidade_necessaria": "Enfermeiro",
    "numero_profissionais": 3,
    "profissionais_designados": [],
    "setor": "UTI"
}
escala_id = cadastrar_escala(dados_escala)
print(f"ID da nova escala: {escala_id}")
print("\n")

# Teste de listagem de escalas
print("=== Teste de Listagem de Escalas ===")
escalas = listar_escalas()
print(f"Escalas encontradas: {escalas}")
print("\n")

# Teste de solicitação de troca
print("=== Teste de Solicitação de Troca ===")
dados_troca = {
    "data_solicitacao": "2024-11-10",
    "id_solicitante": uid,
    "id_colega": "outro_uid",  # Substitua por um UID válido se desejar
    "turno_atual": "manhã",
    "setor_atual": "Emergência",
    "turno_desejado": "tarde",
    "setor_desejado": "UTI",
    "status": "pendente",
    "especialidade": "Enfermeiro"
}
troca_id = solicitar_troca(dados_troca)
print(f"ID da solicitação de troca: {troca_id}")
print("\n")

# Teste de atualização do status de troca
print("=== Teste de Atualização de Status da Troca ===")
atualizar_status_troca(troca_id, "aprovado")
print(f"Status da troca {troca_id} atualizado para 'aprovado'")
print("\n")
