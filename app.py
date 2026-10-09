from datetime import datetime

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo

# ============================================================
# CONFIGURAÇÃO DO CLIENTE ZERO (Rio Branco - Acre)
# ============================================================
configuracao_cliente_acre = {
    "nome_loja": "Comércio do Silva",
    "fuso_horario": "America/Rio_Branco",  # Fuso oficial do Acre
    "abertura": 3,  # 08:00 AM
    "fechamento": 18,  # 18:00 (06:00 PM)
    "dias_uteis": [0, 1, 2, 3, 4, 5, 6, 7]  # Segunda a Sexta
}


def responder_mensagem_cliente(mensagem_recebida: str, dados_cliente: dict) -> str:
    try:
        # 1. Carrega o fuso do Acre e verifica o horário
        fuso_nome = dados_cliente.get("fuso_horario", "America/Rio_Branco")
        try:
            agora = datetime.now(ZoneInfo(fuso_nome))
        except Exception:
            agora = datetime.now()

        abertura = dados_cliente.get("abertura", 8)
        fechamento = dados_cliente.get("fechamento", 18)
        dias_uteis = dados_cliente.get("dias_uteis", [0, 1, 2, 3, 4])

        is_open = (agora.weekday() in dias_uteis) and (abertura <= agora.hour < fechamento)

        nome = dados_cliente.get("nome_loja", "nossa loja")

        # 2. Resposta quando está ABERTO
        if is_open:
            return f"Seja bem-vindo à {nome}! 👋\n\nAgradecemos seu contato. Um de nossos atendentes irá te responder em breve!"

        # 3. Resposta quando está FECHADO
        else:
            return (
                f"Olá! No momento estamos fora do nosso horário de atendimento.\n"
                f"Nosso horário de funcionamento é de Segunda a Sexta, das {abertura}:00h às {fechamento}:00h.\n"
                f"Deixe sua mensagem e responderemos assim que abrirmos!"
            )

    except Exception as erro:
        print(f"[ERRO NO SISTEMA]: {erro}")
        return "Obrigado pelo contato! Já iremos te atender."


# ============================================================
# TRAVA DO TERMINAL PARA O PROGRAMA NÃO FECHAR SOZINHO
# ============================================================
print("--- CHATBOT RIO BRANCO INICIADO (Digite 'sair' para encerrar) ---")

while True:
    mensagem = input("\n> ")
    if mensagem.lower() == "sair":
        print("Programa encerrado.")
        break

    resposta = responder_mensagem_cliente(mensagem, configuracao_cliente_acre)
    print(f"\n[Bot Responde]:\n{resposta}")
