# Assistant de Chat RAG (Retrieval-Augmented Generation)

Ce projet est la preuve de concept d'un assistant de chat utilisant le concept de **RAG** (Retrieval-Augmented Generation). Il permet de poser des questions sur des documents locaux en utilisant des modèles de langage (LLM) via **Ollama**, avec une base de données vectorielle **ChromaDB** pour la recherche de contexte.

## 🚀 Fonctionnalités

- **Recherche Sémantique** : Utilise des embeddings pour trouver les passages les plus pertinents dans vos documents.
- **Réponses Contextuelles** : L'IA répond en se basant uniquement sur les informations fournies (évite les hallucinations).
- **Interface CLI Riche** : Une interface en ligne de commande élégante grâce à `rich` (panneaux, spinners, markdown).
- **Persistance** : Stockage des embeddings dans une base ChromaDB locale.
- **Gestion de l'historique** : Supporte l'historique de conversation via la gestion de session.

## 🛠️ Prérequis

Avant de commencer, assurez-vous d'avoir installé :
1. [Python 3.10+](https://www.python.org/)
2. [Ollama](https://ollama.com/) (pour faire tourner les modèles localement)

## 📦 Installation

1. **Cloner le dépôt** :
   ```bash
   git clone <url-du-depot>
   cd rag-poc-history-chroma
   ```

2. **Créer un environnement virtuel** :
   ```bash
   python -m venv venv
   # Sur Windows
   .\venv\Scripts\activate
   # Sur macOS/Linux
   source venv/bin/activate
   ```

3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

4. **Installer le modèle Ollama** :
   Ce projet utilise par défaut `llama3.2`. Téléchargez-le avec :
   ```bash
   ollama pull llama3.2
   ```

## ⚙️ Configuration

Créez un fichier `.env` à la racine du projet (optionnel si vous utilisez les valeurs par défaut) :
```env
# Exemple de configuration
OLLAMA_BASE_URL=http://localhost:11434
```

## 🎮 Utilisation

Pour lancer l'assistant de chat :

```bash
python main.py
```

### Commandes disponibles dans le chat :
- `/help` : Affiche l'aide
- `/quit` ou `/exit` : Quitte l'application
- `/clear` : Efface l'historique de la conversation actuelle

## 📂 Structure du projet

- `main.py` : Point d'entrée de l'application.
- `src/cli/` : Logique de l'interface utilisateur.
- `src/vectorstore/` : Gestion de la base de données vectorielle ChromaDB.
- `src/embedding/` : Service de génération d'embeddings via Ollama.
- `src/text_splitter/` : Découpage des documents en segments.
- `src/documents_loader/` : Chargement des documents (inclut des mocks pour la démo).

## 📝 Licence

Libre d'utilisation pour vos propres projets de recherche IA.
