# 📦 InOutControl — Sistema de Controle de Entradas e Saídas de Peças

O **InOutControl** é uma aplicação web desenvolvida em **Flask** para gerenciar o fluxo de **entradas e saídas de peças em estoque**.  
Ele oferece recursos de cadastro de peças e usuários, controle de movimentações, geração de relatórios em PDF, além de suporte a QR Code e código de barras para identificação rápida.

---

## ✨ Funcionalidades
- Dashboard com visão geral das movimentações
- Cadastro e gerenciamento de usuários
- Controle de peças (inclusão, edição e exclusão)
- Registro de entradas e saídas de estoque
- Upload de imagens de peças
- Relatórios em PDF com **WeasyPrint**
- Identificação por QR Code e código de barras
- Backup de dados
- Paginação para grandes volumes de registros

---

## 🖼️ Screenshots

### Dashboard
![Dashboard](screenshot/dashboard.png)

### Cadastro de Peças
![Cadastro de Peças](screenshot/pecas.png)

### Movimentação
![Movimentação](screenshot/movimentacao.png)

---

## ⚙️ Tecnologias utilizadas
- **Flask** (framework web)
- **Flask-SQLAlchemy** (ORM)
- **SQLite** (banco de dados)
- **WeasyPrint** (PDF)
- **qrcode / python-barcode / Pillow** (QR Code e código de barras)
- **Flask-Paginate** (paginação)
- **python-dotenv** (variáveis de ambiente)

---

# 🚀 Guia de Instalação — InOutControl (Windows)

## 1. Pré-requisitos

- [ ] Instalar **Python 3.10+** ([Download](https://www.python.org/downloads/))
- [ ] Verificar instalação:

```
py --version
```

- [ ] Instalar Git (opcional, para clonar repositório)
- [ ] Instalar **Microsoft Visual C++ Build Tools** (necessário para compilar pacotes como `pyminizip`):
👉 [Download oficial](https://visualstudio.microsoft.com/pt-br/visual-cpp-build-tools/?utm_source=copilot.com)  
Durante a instalação, selecione **Desktop development with C++**.

## 2. Criar ambiente virtual

No terminal (PowerShell ou CMD), dentro da pasta do projeto:

```
py -m venv venv
```

Ativar o ambiente:

```
venv\Scripts\activate
```

## 3. Atualizar ferramentas de instalação

Antes de instalar as dependências, atualize o `pip`, `setuptools` e `wheel`:

```
python -m pip install --upgrade pip setuptools wheel
```

## 4. Instalar dependências

Com o ambiente virtual ativo:

```
pip install -r requirements.txt
```

> ⚠️ O pacote `pyminizip` exige os **Build Tools** instalados para compilar corretamente.
Se a instalação falhar, verifique se o compilador MSVC foi instalado e se o ambiente está configurado.

## 5. Banco de Dados

O banco SQLite será criado automaticamente como `inoutcontrol.db` na raiz do projeto:

```
py run.py
```
O SQLAlchemy criará as tabelas.

## 6. Executar o servidor

No terminal, com o ambiente virtual ativo:

```
python app.py
```

## 7. Extras (Windows)

## 7.1 Geração de PDF com WeasyPrint

O WeasyPrint depende de bibliotecas gráficas externas (GTK, Cairo, Pango, GObject).
No Windows, siga estes passos:

1. Baixe e instale o **GTK3 Runtime**:
  👉 [Download GTK 3 Runtime](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases?utm_source=copilot.com)

2. Durante a instalação, escolha a versão **Win64**.

3. Adicione a pasta `bin` ao **PATH** do Windows:

- Pressione Win + R, digite:

```
sysdm.cpl
```

- Vá até a aba Avançado.

- Clique em Variáveis de Ambiente.

4. Editar a variável **Path**

- Na seção **Variáveis do Sistema**, encontre a variável chamada Path.

- Selecione e clique em **Editar**.

5. Adicionar o caminho do GTK

- Clique em Novo.

- Cole o caminho:

```
C:\Program Files\GTK3-Runtime Win64\bin
```
- Clique em **OK** para salvar.

6. Aplicar e reiniciar

- Feche todas as janelas com **OK**.

- Reinicie o **terminal (PowerShell ou CMD)** para que a alteração seja reconhecida.

## 7.2 Desenvolvimento

```
set FLASK_ENV=development
flask run
```

## 8. Acesse no navegador

```
http://127.0.0.1:5000
```

---

## 🧾 Licença

Este projeto é licenciado sob a licença `MIT`. Veja o arquivo [**LICENSE**](https://github.com/soarespaullo/InOutControl/blob/main/LICENSE) para mais detalhes.

---

## 👨‍💻 Autor

Feito com ❤️ por [**Paulo Soares**](https://soarespaullo.github.io/) – `Pull Requests` são bem-vindos!

- 📧 [**soarespaullo@proton.me**](mailto:soarespaullo@proton.me)

- 💬 [**@soarespaullo**](https://t.me/soarespaullo) no Telegram

- 💻 [**GitHub**](https://github.com/soarespaullo)

- 🐞 [**NotABug**](https://notabug.org/soarespaullo)

---
