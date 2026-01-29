import sys
from pathlib import Path

# Adjust the path to import from src directory
base_dir = Path(__file__).parents[1]
sys.path.insert(0, str(base_dir))

from src.agents.chat import AgentChat
from src.models.chat_session import ChatSession


def main(agent_id: str = None,
         realm: str = None, 
         client_id: str = None,
         client_secret: str = None):
    
    """Run chat example with file upload."""
    
    try:
        print("StackSpot Chat com Upload de Arquivos")
        print("------------------------------------")
        print("Carregando configurações...")

        # Initialize chat session
        session = ChatSession()

        # Initialize chat with agent
        chat = AgentChat(
            agent_id=agent_id,
            realm=realm,
            client_id=client_id,
            client_secret=client_secret
        )

        print("\nChat iniciado! Digite 'sair' para encerrar.")
        print("Comandos especiais:")
        print("  - 'upload': Faz upload de arquivos")
        print("  - 'limpar': Limpa o histórico da conversa")
        print("  - 'contexto': Mostra o contexto atual")

        # Interactive chat with file upload
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

                files = []
                if question.lower() == "upload":
                    print("\nUpload de arquivos")
                    print("Digite os caminhos dos arquivos (um por linha)")
                    print("Digite uma linha vazia para finalizar")

                    while True:
                        file_path = input("Arquivo: ").strip()
                        if not file_path:
                            break

                        path = Path(file_path)
                        if not path.exists():
                            print(f"Arquivo não encontrado: {file_path}")
                            continue

                        files.append(path)
                        print(f"Arquivo adicionado: {path.name}")

                    if not files:
                        print("Nenhum arquivo foi adicionado.")
                        continue

                    question = input("\nQual sua pergunta sobre os arquivos? ")

                # Add user message to session
                session.add_message("user", question)

                # Get answer with context and files
                answer = chat.ask(
                    question=question,
                    context=session.get_context(),
                    streaming=False,
                    use_stackspot_docs=True,
                    return_ks_in_response=False,
                    files=files if files else None,
                )

                # Add assistant response to session
                session.add_message("assistant", answer)
                print(f"\nResposta: {answer}")

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
    
    agent_id = "01K8F6PDXR3RQKFKBQTJ8D1Z7Y"
    realm = "stackspot-freemium"
    client_id = "5ebf7401-29fc-494c-b7e4-ec59f2518077"
    client_secret = "7ty3d1ef3bhbj6k6Dq5Ez14xa7x6vCSK6xKkVSYkaDCbEQ788ut2C4CPq5Pg6i9p"
    
    main(agent_id=agent_id,
         realm=realm, 
         client_id=client_id, 
         client_secret=client_secret)
