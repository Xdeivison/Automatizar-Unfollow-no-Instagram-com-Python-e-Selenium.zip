# Instagram Unfollow Bot

Este script em Python utiliza Selenium para automatizar o processo de identificar e deixar de seguir usuários no Instagram que não te seguem de volta.

## Funcionalidades

- Abre o navegador Chrome ou Edge.
- Realiza o login na sua conta do Instagram.
- Coleta suas listas de "seguidores" e "seguindo".
- Compara as duas listas para encontrar quem você segue, mas não te segue de volta.
- Permite deixar de seguir essas pessoas (requer ativação manual no código).
- Inclui pausas (sleeps) para simular comportamento humano e evitar detecção.
- Registra logs detalhados das ações.

## Pré-requisitos

- Python 3.x instalado.
- Conexão com a internet.
- Navegador Google Chrome ou Microsoft Edge instalado.

## Instalação

1. Clone este repositório (ou baixe os arquivos `instagram_unfollow.py` e `.env`):

   ```bash
   # Exemplo, se fosse um repositório
   # git clone <URL_DO_REPOSITORIO>
   # cd instagram-unfollow-bot
   ```

2. Instale as dependências Python:

   ```bash
   pip install selenium webdriver-manager python-dotenv
   ```

## Configuração

1. Renomeie o arquivo `.env.example` para `.env` (se você baixou o projeto, o arquivo `.env` já deve estar presente).

2. Edite o arquivo `.env` e preencha suas credenciais do Instagram:

   ```
   INSTAGRAM_USERNAME="seu_usuario_do_instagram"
   INSTAGRAM_PASSWORD="sua_senha_do_instagram"
   ```

   **ATENÇÃO:** Mantenha suas credenciais seguras e nunca as compartilhe publicamente.

## Como Usar

1. Certifique-se de que o arquivo `.env` está configurado corretamente.

2. Abra o arquivo `instagram_unfollow.py`.

3. **Para ativar a funcionalidade de unfollow**, localize a seguinte linha no final do script e descomente-a (remova o `#`):

   ```python
   # unfollower.unfollow_users(not_following_back)
   ```

   Após descomentar, a linha deve ficar assim:

   ```python
   unfollower.unfollow_users(not_following_back)
   ```

   **Recomendação:** Execute o script primeiro sem descomentar esta linha para ver a lista de usuários que seriam deixados de seguir, sem realmente realizar a ação.

4. Execute o script a partir do terminal:

   ```bash
   python instagram_unfollow.py
   ```

O navegador será aberto, o login será tentado, as listas serão coletadas e os logs serão exibidos no terminal.

## Observações Importantes

- O Instagram frequentemente atualiza sua interface, o que pode quebrar os seletores (XPath, etc.) usados no script. Se o script parar de funcionar, pode ser necessário atualizar os seletores.
- Use este script com responsabilidade. O uso excessivo ou comportamento não natural pode levar a bloqueios temporários ou permanentes da sua conta do Instagram.
- Este script é fornecido como está, sem garantias. Use por sua conta e risco.


