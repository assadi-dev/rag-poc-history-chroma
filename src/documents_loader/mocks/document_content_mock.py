# Documents de démonstration
DEMO_DOCUMENTS = [
    {
        "page_content": """
LangChain est un framework open-source pour développer des applications 
alimentées par des modèles de langage (LLM). Il permet de créer des chaînes 
de traitement combinant des LLMs avec d'autres sources de données et outils.

Les principaux composants de LangChain sont:
- Models: Interface unifiée pour différents LLMs
- Prompts: Templates et gestion des prompts
- Chains: Combinaison de plusieurs appels
- Agents: LLMs qui décident des actions à prendre
- Memory: Gestion de la mémoire de conversation
- Retrieval: Récupération de documents pertinents
        """,
        "metadata": {"source": "langchain_intro", "topic": "langchain"}
    },
    {
        "page_content": """
Pour installer LangChain, utilisez pip:

pip install langchain langchain-community

Pour une installation complète avec tous les extras:
pip install langchain[all]

LangChain nécessite Python 3.8 ou supérieur.
        """,
        "metadata": {"source": "langchain_install", "topic": "langchain"}
    },
    {
        "page_content": """
Ollama est un outil permettant d'exécuter des LLMs localement sur votre machine.
Il supporte de nombreux modèles comme Llama, Mistral, et Gemma.

Installation d'Ollama:
- macOS/Linux: curl -fsSL https://ollama.com/install.sh | sh
- Docker: docker pull ollama/ollama

Pour télécharger un modèle: ollama pull llama3
Pour lancer un modèle: ollama run llama3
        """,
        "metadata": {"source": "ollama_intro", "topic": "ollama"}
    },
    {
        "page_content": """
pgvector est une extension PostgreSQL pour le stockage et la recherche 
de vecteurs. Elle est idéale pour les applications de recherche sémantique
et de RAG (Retrieval-Augmented Generation).

Installation:
CREATE EXTENSION vector;

Création d'une table avec vecteurs:
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding vector(768)
);

Recherche par similarité cosinus:
SELECT * FROM items 
ORDER BY embedding <=> query_vector 
LIMIT 5;
        """,
        "metadata": {"source": "pgvector_intro", "topic": "pgvector"}
    },
    {
        "page_content": """
Le RAG (Retrieval-Augmented Generation) est une technique qui combine 
la recherche d'information avec la génération de texte par un LLM.

Étapes du RAG:
1. Indexation: Les documents sont découpés en chunks et vectorisés
2. Retrieval: La question est vectorisée et on cherche les chunks similaires
3. Augmentation: Les chunks pertinents sont ajoutés au prompt
4. Génération: Le LLM génère une réponse basée sur le contexte

Avantages du RAG:
- Réponses basées sur des données actualisées
- Réduction des hallucinations
- Possibilité de citer les sources
        """,
        "metadata": {"source": "rag_concept", "topic": "rag"}
    },
    {
        "page_content": """
Python est un langage de programmation interprété, de haut niveau et 
à usage général. Créé par Guido van Rossum, Python est connu pour sa 
syntaxe claire et sa lisibilité.

Caractéristiques principales:
- Syntaxe claire et lisible
- Typage dynamique
- Gestion automatique de la mémoire
- Large bibliothèque standard
- Écosystème riche de packages (pip)

Installation: Téléchargez depuis python.org ou utilisez pyenv.
        """,
        "metadata": {"source": "python_intro", "topic": "python"}
    },
]
