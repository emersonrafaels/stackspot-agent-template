import sys
from pathlib import Path

# Adjust import path for data functions
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.agents.chat import AgentChat
from src.config.config_logger import logger
from src.config.config_dynaconf import get_settings
from src.config.stackspot_config import get_stackspot_config
from src.models.chat_session import ChatSession

# Retrieve settings instance
settings = get_settings()

def main():
    """Run chat example."""
    try:
        print("StackSpot Chat")
        print("-------------")
        print("Carregando configurações...")

        # Get configuration from settings
        stackspot_config = get_stackspot_config()
        
        # Initialize chat session
        session = ChatSession()
        
        # Initialize chat with agent
        chat = AgentChat(
            agent_id=stackspot_config.get("agent_id"),
            realm=stackspot_config.get("realm"),
            client_id=stackspot_config.get("client_id"),
            client_secret=stackspot_config.get("client_secret"),
            auth_url=stackspot_config.get("auth_url"),
            base_url=stackspot_config.get("inference_url"),
            chat_endpoint=settings.get("stackspot.inference.chat_endpoint")
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
                    return_ks_in_response=False
                )

                # Add assistant response to session
                session.add_message("assistant", answer)
                print(f"\nResposta: {answer}")

            except KeyboardInterrupt:
                break

            except Exception as e:
                logger.error(f"Erro: {e}")
                print("Erro ao processar pergunta. Tente novamente.")

        print("\nChat encerrado!")

    except KeyboardInterrupt:
        print("\nOperação cancelada pelo usuário.")

    except Exception as e:
        logger.error(f"Erro fatal: {e}")
        print(f"Erro: {e}")


if __name__ == "__main__":
    main()
