# 🎨 Art Poster Bot

Benvenuti in **Art Poster Bot**, un progetto Python che automatizza la pubblicazione di post su X (precedentemente noto come Twitter) con immagini di opere d'arte e hashtag creativi. Questo bot utilizza Selenium per navigare su WikiArt, scaricare immagini e pubblicarle su X, evitando duplicati grazie a un database su GitHub.

## 📋 Sommario

- [Introduzione](#introduzione)
- [Prerequisiti](#prerequisiti)
- [Installazione](#installazione)
- [Configurazione](#configurazione)
- [Utilizzo](#utilizzo)
- [Struttura del Progetto](#struttura-del-progetto)
- [Contributi](#contributi)
- [Licenza](#licenza)

## Introduzione

**Art Poster Bot** è progettato per gli amanti dell'arte che desiderano condividere automaticamente opere d'arte su X. Il bot:

1. Naviga su WikiArt.
2. Scarica immagini di opere d'arte.
3. Pubblica le immagini su X con hashtag creativi.
4. Evita duplicati aggiornando un database su GitHub.

## Prerequisiti

Assicurati di avere i seguenti strumenti installati:

- Python 3.8+
- pip
- Un account su X con chiavi API
- Un account GitHub con un repository per il database

## Installazione

1. Clona il repository:

    ```sh
    git clone https://github.com/tuo-username/art-poster-bot.git
    cd art-poster-bot
    ```

2. Installa le dipendenze:

    ```sh
    pip install -r requirements.txt
    ```

## Configurazione

1. Crea un file `.env` nella radice del progetto e aggiungi le tue chiavi e token:

    ```env
    CONSUMER_KEY=your_consumer_key
    CONSUMER_SECRET=your_consumer_secret
    ACCESS_TOKEN=your_access_token
    ACCESS_TOKEN_SECRET=your_access_token_secret
    GITHUB_TOKEN=your_github_token
    ```

2. Configura il repository GitHub per il database:

    - Crea un file `db2.txt` nel tuo repository GitHub.

## Utilizzo

1. Esegui il bot:

    ```sh
    python main.py
    ```

2. Il bot navigherà su WikiArt, scaricherà un'immagine, creerà un post su X e aggiornerà il database su GitHub.

## Struttura del Progetto

```plaintext
.
├── .gitignore
├── [main.py]
├── Procfile
├── [requirements.txt]
└── [runtime.txt]