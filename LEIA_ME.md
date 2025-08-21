# Discord Bot

Este projeto é um bot para Discord que permite aos usuários interagir com ele através de comandos e gerenciar a reprodução de música em canais de voz.

## Arquivos

- src/Bot.py: Contém o código principal do bot. Inicializa o bot, define comandos para interagir com os usuários e gerencia a reprodução de música em canais de voz. Inclui classes e funções para gerenciar sessões de música, extrair informações do YouTube e lidar com respostas de comandos.

- .env: Arquivo utilizado para armazenar variáveis de ambiente, incluindo o DISCORD_TOKEN, necessário para autenticação do bot com a API do Discord.

- requirements.txt: Lista as dependências Python necessárias para o projeto, incluindo bibliotecas como discord.py, yt-dlp, python-dotenv e PyNaCl (necessário para áudio/voz).

## Instruções de Configuração

1. Clonar o repositório:
   ```
   git clone <repository-url>
   cd discord-bot
   ```

2. Criar um ambiente virtual (opcional, mas recomendado):
   ```
   python -m venv venv
   source venv/bin/activate  # No Windows use `venv\Scripts\activate`
   ```

3. Instalar dependências:
   ```
   pip install -r requirements.txt
   ```

4. Configurar variáveis de ambiente:
   Crie um arquivo .env na raiz do projeto e adicione seu token do Discord:
   ```
   DISCORD_TOKEN=seu_token_aqui
   ```

5. Executar o bot:
   ```
   python src/Bot.py
   ```

## Uso

- Utilize o prefixo & para interagir com o bot.
- Comandos disponíveis:
  - &fenrir: Apresenta o bot.
  - &hi: Envia uma mensagem de bom dia com GIF embutido.
  - &join: Faz o bot entrar no canal de voz do usuário.
  - &leave: Faz o bot sair do canal de voz.
  - &play <url>: Toca uma música ou playlist do YouTube.
  - &pause: Pausa a música atual.
  - &resume: Retoma a música pausada.
  - &skip: Pula a música atual.
  - &back: Volta para a música anterior.
  - &queue: Exibe a música atual e a fila.

## Contribuição

Sinta-se à vontade para enviar issues ou pull requests para melhorias ou correções de bugs.

## Observações

- Certifique-se de que o FFmpeg esteja instalado e adicionado ao PATH do sistema, caso contrário o bot não conseguirá tocar áudio.
- O PyNaCl é necessário para funcionalidades de áudio/voz, então garanta que ele esteja instalado via requirements.txt.

