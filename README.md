# **Sistema de Recomendação de Vídeos Educacionais**

Um sistema completo de recomendação de vídeos educacionais baseado em interações do usuário e suas preferências, que combina técnicas de recomendação colaborativa, baseada em conteúdo e abordagem híbrida, integrando dados da API do YouTube.

---

## **Índice**
- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Instalação e Configuração](#instalação-e-configuração)
- [Uso do Sistema](#uso-do-sistema)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Recomendações Implementadas](#recomendações-implementadas)
- [Dashboard e Visualização](#dashboard-e-visualização)
- [Contribuição](#contribuição)
- [Licença](#licença)
---

## 📖 **Sobre o Projeto**
Este sistema foi desenvolvido para recomendar vídeos educacionais do YouTube com base no histórico de interações do usuário. Ele permite explorar conteúdos relevantes utilizando diferentes técnicas de recomendação e visualizar as recomendações que o sistema gera.

O projeto é parte do **TCC** para o curso de **Sistemas de Informação** da **Faculdade Federal dos Vales do Jequitinhonha e Mucuri (UFVJM)** e foi desenvolvido com foco em aprendizado personalizado e otimização da descoberta de conteúdo.

---

## 🛠️ **Funcionalidades**
- Autenticação e gerenciamento de usuários.
- Avaliação de vídeos (curtir/não curtir) para refinar as recomendações.
- Seleção de **áreas de interesse** organizadas por categorias.
- Recomendação baseada em:
  - **Usuário (User-Based)** — encontra usuários com gostos semelhantes.
  - **Itens (Item-Based)** — encontra vídeos semelhantes ao que o usuário já assistiu.
  - **Híbrida (Fusão ou Cascata)** — combinação de user-based e item-based.
- Busca e integração com a API do YouTube.
- Filtros personalizados por duração, categoria e idioma.
- Dashboard com gráficos de similaridade e clusters de vídeos.
- Criação e gerenciamento de playlists personalizadas.

---

## 🛠️ **Tecnologias Utilizadas**
- **Backend:** Django, Django REST Framework
- **Banco de Dados:** SQLite (padrão do Django)
- **Machine Learning:** scikit-learn, pandas, NumPy
- **Visualização:** Plotly.js, t-SNE para clusters
- **Integração:** API do YouTube (Google API)

---

## ⚙️ **Instalação e Configuração**

### **Pré-requisitos:**
- Python 3.12
- Django 5.1
- SQLite
- Chave de API do YouTube

### **Passos para rodar o projeto:**

#### 🐧 **Linux**

1. **Clonar o repositório:**
```bash
git clone https://github.com/seu-usuario/sistema-recomendacao-videos.git
cd sistema-recomendacao-videos
```

2. **Criar e ativar o ambiente virtual:**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Instalar as dependências:**
```bash
pip install -r requirements.txt
```

4. **Configurar o arquivo `.env`:**  
Crie um arquivo chamado **.env** na raiz do projeto e adicione as configurações:  

```
SECRET_KEY = 'sua-chave-secreta-do-django'  
DEBUG = 'True'  
YOUTUBE_API_KEY = 'sua-chave-da-api-do-youtube'  

EMAIL_HOST = 'smtp.exemplo.com'  
EMAIL_PORT = '587'  
EMAIL_HOST_USER = 'seu-email'  
EMAIL_HOST_PASSWORD = 'sua-senha'  
EMAIL_USE_TLS = 'True'
```

> **Obs:** A configuração de e-mail é necessária para ativação de contas e recuperação de senha.

5. **Criar as pastas de mídia e avatares:**

Crie a estrutura de diretórios para armazenar imagens e avatares dos usuários:
```bash
mkdir media
mkdir media/avatars
cp caminho/default.png media/avatars/
```
6. **Aplicar migrações e iniciar o servidor:**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

7. **Criar o superusuário:**

Para acessar o painel de administração do Django e gerenciar usuários e conteúdos:
```bash
python manage.py createsuperuser
```
📂 Populando o banco de dados (opcional)

1. **Importar interesses:**

Você pode popular a base de interesses com um arquivo de texto.
```bash
python manage.py import_interests recomendador_videos/data/interesses.txt
```
2. **Preencher vídeos com base nos interesses:**

Depois de importar os interesses, preencha o banco com vídeos relacionados:
```bash
python manage.py preencher_videos
```

#### 🪟 **Windows**

1. **Instalar o GTK (se necessário para visualizações gráficas):**
- Baixe o instalador do GTK para Windows.
- Adicione o caminho da pasta `bin` do GTK às variáveis de ambiente.

2. **Clonar o repositório:**
```powershell
git clone https://github.com/seu-usuario/sistema-recomendacao-videos.git
cd sistema-recomendacao-videos
```

3. **Criar e ativar o ambiente virtual:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

4. **Instalar as dependências:**
```powershell
pip install -r requirements.txt
pip install pycairo PyGObject
```

5. **Configurar o arquivo `.env`:**
Crie o arquivo `.env` e adicione as variáveis de ambiente.

6. **Aplicar migrações e iniciar o servidor:**
```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
7. **Criar o superusuário:**

Para acessar o painel de administração do Django e gerenciar usuários e conteúdos:

```powershell
python manage.py createsuperuser
```
📂 Populando o banco de dados (opcional)

1. **Importar interesses:**

Você pode popular a base de interesses com um arquivo de texto.

```powershell
python manage.py import_interests recomendador_videos/data/interesses.txt
```
2. **Preencher vídeos com base nos interesses:**

Depois de importar os interesses, preencha o banco com vídeos relacionados:

```powershell
python manage.py preencher_videos
```
#### 🍏 **macOS**

1. **Instalar dependências adicionais:**
```bash
brew install pango
```

2. **Clonar o repositório:**
```bash
git clone https://github.com/seu-usuario/sistema-recomendacao-videos.git
cd sistema-recomendacao-videos
```

3. **Criar e ativar o ambiente virtual:**
```bash
python3 -m venv venv
source venv/bin/activate
```

4. **Instalar as dependências:**
```bash
pip install -r requirements.txt
```

5. **Configurar o arquivo `.env`:**
Crie o arquivo `.env` com as configurações de API e secret keys.

6. **Aplicar migrações e iniciar o servidor:**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Agora o sistema estará disponível em:  
🔗 `http://127.0.0.1:8000/`

---

## **Uso do Sistema**
1. **Cadastro e login:** Crie uma conta ou acesse com suas credenciais.
2. **Selecionar áreas de interesse:** Escolha os tópicos para personalizar as recomendações.
3. **Avaliação de vídeos:** Curta ou não curta vídeos para treinar o sistema.
4. **Explorar recomendações:** Acesse as diferentes abordagens de recomendação.
5. **Dashboards interativos:** Visualize as conexões e clusters de vídeos.
6. **Criação de playlists:** Organize os vídeos recomendados em playlists personalizadas.

---

## 🛡️ **Licença**   

```
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software...
```

---
