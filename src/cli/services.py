from langchain_ollama import ChatOllama
import os
import sys
import argparse
import signal
from typing import Optional, Dict, List, Any
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.text import Text
from rich.live import Live
from rich.spinner import Spinner
from src.vectorstore.services import VectorStoreService
from src.embedding.services import EmbeddingService
from src.cli.chat.services import ChatService

class SignalHandler:
    def __init__(self, message: str = "\n👋 Fermeture..."):
        self.message = message
        self._cleanup_callback = None

    def register_cleanup(self, callback):
        self._cleanup_callback = callback

    def setup(self):
        signal.signal(signal.SIGINT, self._handle_signal)

    def _handle_signal(self, signum, frame):
        print(self.message)
        if self._cleanup_callback:
            self._cleanup_callback()
        sys.exit(0)

class CliService:
    # Commandes disponibles
    COMMANDS: Dict[str, str] = {
        "/quit": "Quitter le chat (alias: /q, /exit)",
        "/clear": "Effacer l'historique de conversation",
        "/index-database": "Indexer les documents",
        "/chat": "Commencer une conversation",
        "/help": "Afficher cette aide (alias: /?)",
    }

    def __init__(self, chatService: ChatService, session_id: Optional[str] = None, debug: bool = False):
        self.session_id = session_id
        self.debug = debug
        self.console = Console()
        self.chatService = chatService
        self._is_running = False
        self._signal_handler = SignalHandler(
            message="\n👋 Fermeture du chat..."
        )

    def print_banner(self):
        """Affiche la bannière de bienvenue."""
        banner = """
    ╔═══════════════════════════════════════════════╗
    ║           🤖 RAG Chat Assistant               ║
    ║                                               ║
    ║  Posez vos questions, je cherche dans        ║
    ║  les documents pour vous répondre.           ║
    ║                                               ║
    ║  Tapez /help pour voir les commandes         ║
    ║  Ctrl+C pour quitter proprement              ║
    ╚═══════════════════════════════════════════════╝
        """
        self.console.print(banner, style="cyan")

    def print_help(self):
        """Affiche l'aide."""
        help_text = "**Commandes disponibles:**\n\n"
      
        for command, description in self.COMMANDS.items():
            help_text += f"**{command}**: {description}\n"
        self.console.print(Panel(Markdown(help_text), title="Aide", subtitle="RAG Chat Assistant", border_style="blue"))

    def handle_command(self, command: str):
        cmd = command.lower().strip()

        """Gère les commandes."""

        # Quitter
        if cmd in ("/quit", "/q", "/exit"):
            return False
        
        # Aide
        if cmd in ("/help", "/?"):
            self.print_help()
            return True

        else:
            self.console.print(
                f"❓ Commande inconnue: {command}. Tapez /help pour l'aide.",
                style="yellow"
            )
        return True

    def user_input(self):
        """
        Récupère l'entrée utilisateur.
        
        Returns:
            Le texte entré, ou None si EOF
        """
        try:
            self.console.print()
            user_input = self.console.input("[bold cyan]Vous:[/] ")
            return user_input.strip()
        except EOFError:
            # Ctrl+D
            return None
        except KeyboardInterrupt:
            # Ctrl+C - sera géré par le signal handler
            raise

    def _process_question(self, query: str):
        """
        Traite une question de l'utilisateur.
        
        Args:
            query (str): La question de l'utilisateur
        
        """
        # Afficher un spinner pendant la génération
        with Live(
                Spinner("dots", text="Réflexion..."),
                console=self.console,
                transient=True
        ):
            try:
                answer = self.chatService.ollama_answer(query)
                self.console.print()
                self.console.print("[bold cyan]Assistant:[/]", style="blue")
                self.console.print(Panel(
                    Markdown(answer or "Désolé, je n'ai pas pu générer de réponse."),
                    border_style="green",
                    padding=(1, 2)
                ))
            except EOFError:
                return None
            except KeyboardInterrupt:
                raise
            except Exception as e:
                self.console.print(f"[bold red]Erreur:[/] {str(e)}")

    def _cleanup(self):
        """Nettoyage avant fermeture."""
        pass

    def run(self)->None:
        """
        Lance la boucle principale du chat. 
        Cette méthode bloque jusqu'à ce que l'utilisateur quitte.
        """
        # Configurer la gestion des signaux
        self._signal_handler.register_cleanup(self._cleanup)
        self._signal_handler.setup()
        
        self.print_banner()
        
        try:
            self.console.print(
                "✨ Prêt! Posez votre question ou tapez /help",
                style="bold green"
            )
            
            self._is_running = True
            while self._is_running:
                u_input = self.user_input()
                if u_input is None:
                    break
                
                if not u_input:
                    continue
                    
                if u_input.startswith("/"):
                    if not self.handle_command(u_input):
                        break
                else:
                    self._process_question(u_input)
                    
        except KeyboardInterrupt:
            self.console.print("\nAu revoir!", style="red")
        finally:
            self._is_running = False

async def setup_demo_dataset():
    # Helper to print since we're outside CliService
    console = Console()
    
    # 1. Load documents
    from src.documents_loader.mocks.document_content_mock import DEMO_DOCUMENTS
    from src.text_splitter.services import TextSplitterService
    docs = DEMO_DOCUMENTS

    # 2. Split documents
    chunks = TextSplitterService().split_text(docs)

    # 3. Create embeddings and store in Chroma
    embedings = EmbeddingService().ollama_embeddings()
    vectorstore = VectorStoreService().chroma_vectorstore(embedings)

    # 4. Add chunks to vectorstore
    vectorstore.add_documents(chunks)

    console.print("Base de données indexée avec succès.", style="green")

async def drop_database():
    console = Console()
    vectorstore = VectorStoreService().chroma_vectorstore(None) # Assuming it can load existing
    vectorstore.delete_all()
    console.print("Base de données supprimée avec succès.", style="green")