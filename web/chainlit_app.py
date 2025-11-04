import chainlit as cl
import sys
import asyncio
from pathlib import Path

# Adjust import path for data functions
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.agents.chat import AgentChat
from src.config.stackspot_config import get_stackspot_config
from src.models.chat_session import ChatSession
from src.config.config_logger import logger
from src.config.config_dynaconf import get_settings

# Initialize session and configurations
session = ChatSession()
settings = get_settings()
stackspot_config = get_stackspot_config()

@cl.on_chat_start
async def start():
    """Initialize the chat session."""
    cl.Message(content="""# 🏦 Bem-vindo ao ObrasBudgetGuard - Itaú Unibanco

    Sou o assistente especializado em análise de orçamentos de obras para agências bancárias do Itaú Unibanco.
    Posso ajudar você a revisar orçamentos, analisar composições, conferir preços e tirar dúvidas sobre padrões de obras.
    
    Comandos disponíveis:
    - `/limpar` - Limpa o histórico da conversa
    - `/contexto` - Mostra conversas anteriores
    - `/ajuda` - Mostra esta mensagem
    - `/upload` - Abre o seletor de arquivos
    """).send()

async def process_uploaded_files(files) -> list[Path]:
    """Process uploaded files and return their paths."""
    if not files:
        logger.info("No files received in process_uploaded_files")
        return []
        
    file_paths = []
    uploads_dir = Path("uploads")
    uploads_dir.mkdir(parents=True, exist_ok=True)
    
    for file in files:
        try:
            logger.info(f"Processing file: {file.name}")
            
            # Tenta obter o conteúdo do arquivo
            try:
                content = await file.get_content()
                if content is None:
                    logger.warning(f"File {file.name} content is None")
                    continue
                    
                if len(content) == 0:
                    logger.warning(f"File {file.name} is empty")
                    continue
                    
                logger.info(f"File {file.name} size: {len(content)} bytes")
                
            except Exception as e:
                logger.error(f"Error reading content from file {file.name}: {str(e)}")
                continue
            
            # Salva o arquivo
            temp_path = uploads_dir / file.name
            try:
                with open(temp_path, "wb") as f:
                    f.write(content)
                    
                if temp_path.exists() and temp_path.stat().st_size > 0:
                    file_paths.append(temp_path)
                    logger.info(f"Successfully saved file: {temp_path}")
                else:
                    logger.warning(f"File was not created or is empty: {temp_path}")
                    if temp_path.exists():
                        temp_path.unlink()
                        
            except Exception as e:
                logger.error(f"Error saving file {file.name}: {str(e)}")
                if temp_path.exists():
                    temp_path.unlink()
                continue
            
        except Exception as e:
            logger.error(f"Error processing file {file.name}: {str(e)}")
    
    logger.info(f"Successfully processed {len(file_paths)} files")
    return file_paths

@cl.on_message
async def main(message: cl.Message):
    """Process each message."""
    try:
        # Handle special commands
        if message.content.startswith('/'):
            cmd = message.content[1:].lower()
            
            if cmd == "limpar":
                session.clear()
                await cl.Message(content="✨ Histórico limpo!").send()
                return
                
            if cmd == "contexto":
                context = "\n\n".join([
                    f"**{msg.role}**: {msg.content}" 
                    for msg in session.messages
                ])
                await cl.Message(content=f"### Histórico\n\n{context}").send()
                return
                
            if cmd == "ajuda":
                await start()
                return
                
            if cmd == "upload":
                await cl.Message(content="📁 Selecione os arquivos para upload:").send()
                files = await cl.AskFileMessage(
                    content="Arraste os arquivos ou clique para selecionar",
                    accept=["text/*", ".pdf", ".csv", ".xlsx", ".json"],
                    max_files=5,
                    max_size_mb=20
                ).send()
                
                if not files:
                    await cl.Message(content="❌ Nenhum arquivo foi selecionado.", author="system").send()
                    return
                    
                await cl.Message(content=f"✅ {len(files)} arquivo(s) recebido(s). Processando...").send()
                message.files = files  # Permite processamento no fluxo normal
                return
                
        # Check for file uploads
        files = []
        if message.files:
            logger.info(f"Received upload request with {len(message.files)} files")
            try:
                # Process the files
                files = await process_uploaded_files(message.files)
                
                if not files:
                    await cl.Message(
                        content="⚠️ Não foi possível processar os arquivos. Verifique se os arquivos não estão vazios ou corrompidos.", 
                        author="system"
                    ).send()
                    return
                
                # Lista os arquivos processados
                files_list = "\n".join(f"- {p.name}" for p in files)
                await cl.Message(
                    content=f"✅ {len(files)} arquivo(s) processado(s) com sucesso:\n{files_list}",
                    author="system"
                ).send()
                
            except Exception as e:
                logger.error(f"Error processing files: {str(e)}")
                await cl.Message(
                    content=f"❌ Erro no processamento dos arquivos: {str(e)}\nPor favor, tente novamente.", 
                    author="system"
                ).send()
                return

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

        # Add user message to session
        session.add_message("user", message.content)

        # Get response with progress indicator
        with cl.Step("Processando..."):
            response = chat.ask(
                question=message.content,
                context=session.get_context(),
                streaming=False,
                use_stackspot_docs=True,
                return_ks_in_response=False,
                files=files if files else None
            )
            
            # Cleanup temporary files
            if files:
                for file_path in files:
                    try:
                        file_path.unlink()
                    except Exception as e:
                        logger.warning(f"Failed to delete temporary file {file_path}: {e}")

        # Add response to session and send
        session.add_message("assistant", response)
        await cl.Message(content=response).send()

    except Exception as e:
        logger.error(f"Error: {e}")
        await cl.Message(
            content=f"❌ Erro: {str(e)}", 
            author="system"
        ).send()