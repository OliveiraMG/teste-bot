import os
from slack import WebClient
from slackeventsapi import SlackEventAdapter

# Inicializar o cliente Slack
slack_token = os.environ["SLACK_API_TOKEN"]
slack_client = WebClient(slack_token)

# Inicializar o adaptador de eventos do Slack
slack_events_adapter = SlackEventAdapter(os.environ["SLACK_SIGNING_SECRET"], "/slack/events")

# Perguntas e respostas pré-definidas
questions = {
    "1": "Qual é a sua cor favorita?",
    "2": "Qual é o seu animal favorito?",
    "3": "Qual é a sua comida favorita?",
    "4": "Qual é o seu hobby favorito?",
    "5": "Qual é a sua música favorita?"
}

answers = {
    "1": "Minha cor favorita é azul.",
    "2": "Meu animal favorito é o leão.",
    "3": "Minha comida favorita é pizza.",
    "4": "Meu hobby favorito é jogar videogame.",
    "5": "Minha música favorita é 'Bohemian Rhapsody' do Queen."
}

# Função para manipular mensagens recebidas
@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    user = message.get("user")
    text = message.get("text")
    channel = message["channel"]

    # Verificar se a mensagem foi enviada por um usuário e não pelo próprio bot
    if user is not None and user != slack_client.api_call("auth.test")["user_id"]:
        # Enviar as perguntas para o usuário
        if text.lower() == "perguntas":
            question_list = "\n".join([f"{num}. {question}" for num, question in questions.items()])
            slack_client.chat_postMessage(channel=channel, text=question_list)
        # Responder à mensagem do usuário com base no número fornecido
        elif text.strip() in answers.keys():
            response = answers[text.strip()]
            slack_client.chat_postMessage(channel=channel, text=response)
        else:
            slack_client.chat_postMessage(channel=channel, text="Desculpe, não entendi sua mensagem.")

# Executar o servidor do adaptador de eventos em segundo plano
slack_events_adapter.start(port=3000)
