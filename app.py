from datetime import datetime
from zoneinfo import ZoneInfo
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuração do cliente (Acre)
configuracao_cliente_acre = {
    "nome_loja": "Comércio do Silva",
    "fuso_horario": "America/Rio_Branco",
    "abertura": 8,   # 08:00
    "fechamento": 18, # 18:00
    "dias_uteis": [0, 1, 2, 3, 4]  # Segunda a Sexta
}

def responder_mensagem_cliente(mensagem_recebida: str, dados_cliente: dict) -> str:
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

    if is_open:
        return f"Seja bem-vindo à {nome}! Agradecemos seu contato. Um de nossos atendentes irá te responder em breve!"
    else:
        return (
            f"Olá! No momento estamos fora do nosso horário de atendimento.\n"
            f"Nosso horário de funcionamento é de Segunda a Sexta, das {abertura}:00h às {fechamento}:00h.\n"
            f"Deixe sua mensagem e responderemos assim que abrirmos!"
        )

@app.route("/", methods=["GET", "POST"])
def webhook():
    if request.method == "POST":
        dados = request.get_json(silent=True) or {}
        mensagem = dados.get("mensagem", "")
        resposta = responder_mensagem_cliente(mensagem, configuracao_cliente_acre)
        return jsonify({"resposta": resposta})
    return "Bot online e a funcionar no Render!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
