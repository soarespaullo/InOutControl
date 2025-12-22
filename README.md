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

## 🚀 Instalação (Windows)

### 1. Clonar repositório

```
git clone https://github.com/soarespaullo/InOutControl.git
cd InOutControl
```

### 2. Criar ambiente virtual

