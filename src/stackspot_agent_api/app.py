from pathlib import Path
from pprint import pprint
from typing import List, Union

from ..agents.chat import AgentChat
from ..models.chat_session import ChatSession


def chat(
    agent_id: str = None,
    realm: str = None,
    client_id: str = None,
    client_secret: str = None,
    question: str = "",
    files: List[Union[str, Path]] = None,
):

    # Iniciando as variáveis
    session = None
    response = None
    message = None

    try:
        print("StackSpot Chat")
        print("-------------")
        print("Carregando configurações...")

        # Initialize chat session
        session = ChatSession()

        # Initialize chat with agent
        chat = AgentChat(
            agent_id=agent_id, realm=realm, client_id=client_id, client_secret=client_secret
        )

        for msg in session.messages:
            print(f"{msg.role}: {msg.content}")

        # Add user message to session
        session.add_message("user", question)

        # Get answer with context
        response = chat.ask(
            question=question,
            context=session.get_context(),
            streaming=False,
            use_stackspot_docs=True,
            return_ks_in_response=False,
            files=files if files else None,
        )

        # Get message from response
        message = response.get("message", "")

        # Add assistant response to session
        session.add_message("assistant", message)

        return {"session": session, "response": response, "message": message}

    except Exception as e:
        print(f"Erro: {e}")
        print("Erro ao processar pergunta. Tente novamente.")

        return {"session": session, "response": response, "message": message}
