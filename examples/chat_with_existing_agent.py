import os
import sys
from getpass import getpass
from pathlib import Path

# Adjust import path for data functions
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.agents.chat import AgentChat
from src.config.config_dynaconf import settings
from src.config.config_logger import logger
from src.config.stackspot_config import get_settings


def get_auth_info() -> dict:
    """Get authentication information from settings and environment."""

    # Try to get from environment or settings
    auth_info = {
        "client_id": settings.get("stackspot_client_id"),
        "client_secret": settings.get("stackspot_client_secret"),
        "realm": settings.get("stackspot_realm"),
        "agent_id": settings.get("stackspot.agent_id"),
    }

    # Validar dados obrigatórios do settings.toml
    missing = []

    if not auth_info["realm"]:
        missing.append("realm")
    if not auth_info["client_id"]:
        missing.append("client_id")
    if not auth_info["client_secret"]:
        missing.append("client_secret")
    if not auth_info["agent_id"]:
        missing.append("agent_id")

    if missing:
        print("\nConfigurações ausentes no settings.toml ou variáveis de ambiente:")
        for item in missing:
            print(f"- {item}")

    return auth_info


def main():
    """Run chat example."""
    try:
        print("StackSpot Chat")
        print("-------------")
        print("Carregando configurações...")

        # Get authentication info from settings
        auth_info = get_auth_info()

        # Initialize chat with agent
        chat = AgentChat(
            agent_id=auth_info["agent_id"],
            realm=auth_info["realm"],
            client_id=auth_info["client_id"],
            client_secret=auth_info["client_secret"],
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
