import sys
from pathlib import Path

# Adjust import path for data functions
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.agents.chat import AgentChat
from src.config.config_logger import logger
from src.config.config_dynaconf import get_settings
from src.config.stackspot_config import get_stackspot_config

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

        # Interactive chat
        while True:
            try:
                question = input("\nPergunta: ")

                if question.lower() in ["sair", "exit", "quit"]:
                    break

                if not question.strip():
                    continue

                answer = chat.ask(question)
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
