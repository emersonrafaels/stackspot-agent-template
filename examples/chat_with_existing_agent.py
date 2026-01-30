import sys
from pathlib import Path
from pprint import pprint

# Adjust the path to import from src directory
base_dir = Path(__file__).parents[1]
sys.path.insert(0, str(base_dir))

from src.agents.chat import AgentChat
from src.models.chat_session import ChatSession


def main(agent_id: str = None, realm: str = None, client_id: str = None, client_secret: str = None):
    """Run chat example."""

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

        print("\nChat iniciado! Digite 'sair' para encerrar.")
        print("Comandos especiais:")
        print("  - 'limpar': Limpa o histórico da conversa")
        print("  - 'contexto': Mostra o contexto atual")

        # Interactive chat with session management
        while True:
            try:
                question = input("\nPergunta: ").strip()

                if question.lower() in ["sair", "exit", "quit"]:
                    break

                if not question:
                    continue

                if question.lower() == "limpar":
                    session.clear()
                    print("Histórico limpo!")
                    continue

                if question.lower() == "contexto":
                    for msg in session.messages:
                        print(f"{msg.role}: {msg.content}")
                    continue

                # Add user message to session
                session.add_message("user", question)

                # Get answer with context
                answer = chat.ask(
                    question=question,
                    context=session.get_context(),
                    streaming=False,
                    use_stackspot_docs=True,
                    return_ks_in_response=False,
                )

                # Get message from response
                message = answer.get("message", "")

                # Add assistant response to session
                session.add_message("assistant", message)
                pprint(f"\nResposta: {answer}")
                print(f"\Mensagem: {message}")

            except KeyboardInterrupt:
                break

            except Exception as e:
                print(f"Erro: {e}")
                print("Erro ao processar pergunta. Tente novamente.")

        print("\nChat encerrado!")

    except KeyboardInterrupt:
        print("\nOperação cancelada pelo usuário.")

    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":

    agent_id = "01KFJ78NYVJSY8YS5A681Q5XT5"
    realm = "stackspot-freemium"
    client_id = "5ebf7401-29fc-494c-b7e4-ec59f2518077"
    client_secret = "7ty3d1ef3bhbj6k6Dq5Ez14xa7x6vCSK6xKkVSYkaDCbEQ788ut2C4CPq5Pg6i9p"

    main(agent_id=agent_id, realm=realm, client_id=client_id, client_secret=client_secret)
