# 📅 Gereventos
Plataforma para o controle de eventos e inscrições, oferecendo funcionalidades
de visualização, criação, edição e participação em eventos, além da administração de perfis de usuários.

<hr>

## 🏗️ Funcionalidades Principais

### 👤 Autenticação
* Login e logout de usuários.
* Cadastro de dois tipos de usuários:
  * Participante: pode visualizar eventos, se inscrever e cancelar sua inscrição.
  * Organizador: pode criar, editar, excluir e listar eventos.

### 📋 Gestão de Vagas
* Organizadores podem:
  * Criar eventos (título, descrição, data, local, capacidade máxima e banner).
  * Editar ou excluir seus próprios eventos.
* Candidatos podem:
  * Visualizar todos os eventos disponíveis.
  * Se inscrever, enviando seus dados disponíveis no perfil.

### 📎 Upload de Banners
* O arquivo do banner é armazenado no Cloudinary e mostrado na página de eventos

### 📧 Confirmação por E-mail
Após candidatura, o candidato recebe uma confirmação automática via e-mail SMTP (Gmail).

<hr>

## 🗃️ Modelos

### `User` (do Django)
### `Participante`
| Campo    | Tipo      | 
|----------|-----------|
| nome     | CharField | 
| telefone | CharField | 
| genero   | CharField |
| cidade   | CharField |
| cpf      | CharField |

### `Organizador`
| Campo    | Tipo      | 
|----------|-----------|
| nome     | CharField | 
| telefone | CharField | 
| genero   | CharField |
| cidade   | CharField |
| cnpj     | CharField |

### `Evento`
| Campo          | Tipo             | 
|----------------|------------------|
| organizador    | FK → Organizador | 
| titulo         | CharField        | 
| descricao      | CharField        |
| data           | DateTimeField    |
| local          | CharField        |
| capacidade_max | IntegerField     |
| imagem_banner  | CloudinaryField  |

### `Inscricao`
| Campo        | Tipo              | 
|--------------|-------------------|
| evento       | FK → Evento       | 
| participante | FK → Participante | 

## 🔐 Regras de Acesso
* Apenas usuários com perfil de organizador podem criar/editar/excluir eventos.
* Apenas usuários autenticados têm acesso às views de eventos.
* Mixins garantem as permissões específicas.

## 🚀 Tecnologias Utilizadas
Liste as principais tecnologias, frameworks e linguagens de programação que você usou.
Ex:
- Django 5.2
- Bootstrap 5.3
- HTML5
- CSS3
- JavaScript
- Python
- PostgreSQL (SupaBase)
- Cloudinary (Armazenamento de banners)
- SMTP Gmail (Envio de e-mails de confirmação)
- `widget tweaks` (Melhorias em formulários HTML)

## ⚙️ Variáveis de Ambiente (.env)

<pre>
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=user
DB_PASSWORD=senha
DB_HOST=host
DB_PORT=5432

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=email
EMAIL_HOST_PASSWORD=senha_app
EMAIL_USE_TLS=True

CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name

DEBUG=True
ALLOWED_HOSTS=*.onrender.com,localhost,127.0.0.1
SECRET_KEY=your-secret-key
</pre>

## 🛠️ Instalação
Como outros desenvolvedores podem instalar seu projeto para rodar localmente?

1. Clone o repositório:
   ```bash
   git clone https://github.com/RaphaBane/Gereventos_SENAC.git
   
2. Crie e ative um ambiente virtual:

   ```bash
   python -m venv venv
   venv\Scripts\activate # no Windows 
   source venv/bin/activate  # bi Linux
   
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   
4. Configure o `.env` com suas credenciais.
5. Rode as migrações:

   ```bash
   python manage.py migrate
   
6. Inicie o servidor:

   ```bash
   python manage.py runserver

7. Acesse: http://localhost:8000

## ✅ Melhorias Futuras
- Adição de mais cobertura para os testes
- Melhoria na parte visual (HTML)
- Adição de uma API de consulta de eventos e participantes.