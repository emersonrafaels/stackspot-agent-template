"""Example of chatting with an existing agent using file upload."""
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
    """Run chat example with file upload."""
    try:
        print("StackSpot Chat com Upload de Arquivos")
        print("------------------------------------")
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
                    files=files if files else None
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