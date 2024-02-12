import os
import streamlit as st
import base64
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from telegram import Bot

load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ.get('YOUR_TELEGRAM_BOT_TOKEN')
bot = Bot(token=TELEGRAM_BOT_TOKEN)
CHAT_ID = os.environ.get('YOUR_CHAT_ID')
# Função para converter a imagem para Base64
def get_image_base64(filename):
    # Construa o caminho do arquivo relativo ao script
    current_dir = os.path.dirname(__file__)
    filepath = os.path.join(current_dir, 'resources', 'imagens', filename)

    with open(filepath, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return f"data:image/jpeg;base64,{encoded_string}"

# Use o nome do arquivo relativo ao invés do caminho absoluto
image_base64 = get_image_base64("Pai2.jpg")
# Inserir CSS customizado para usar a imagem de fundo
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("{image_base64}");
        background-size: cover;
        background-attachment: fixed;
        background-repeat: no-repeat;
        background-position: center center;
    }}
    .stApp::before {{
        content: "";
        position: fixed;
        left: 0;
        right: 0;
        top: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.8); /* Ajuste a opacidade do fade escuro aqui */
        z-index: 0;
    }}
    </style>
    """, unsafe_allow_html=True)

def enviar_email(nome, email, mensagem):
    remetente_email = os.environ.get("EMAIL_USER")
    remetente_senha = os.environ.get("EMAIL_PASSWORD")
    destinatario_email = os.environ.get("EMAIL_TARGET")

    msg = MIMEMultipart()
    msg['From'] = remetente_email
    msg['To'] = destinatario_email
    msg['Subject'] = "Nova Mensagem de Contato"

    corpo = f"Nome: {nome}\nEmail: {email}\nMensagem: {mensagem}"
    msg.attach(MIMEText(corpo, 'plain'))

    try:
        # Usando o servidor SMTP do Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remetente_email, remetente_senha)
        server.sendmail(remetente_email, destinatario_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"Erro ao enviar e-mail: {e}")
        return False

# Criação do menu lateral com as seções
def aulas_virtuais():
    st.write("""
    As aulas virtuais oferecem flexibilidade e comodidade, permitindo que você participe de qualquer lugar. Utilizamos o ZOOM para nossas sessões ao vivo, criando um ambiente interativo onde você pode esclarecer dúvidas em tempo real.
    """)

def grupo_telegram():
    st.write("""
    O grupo exclusivo no Telegram é uma ferramenta chave para o seu desenvolvimento contínuo. Aqui, você receberá mensagens motivacionais, exercícios diários e poderá interagir com outros mentoriados, criando uma comunidade de suporte mútuo.
    """)

def encontros_presenciais():
    st.write("""
    Os encontros presenciais, embora menos frequentes, são uma oportunidade incrível para networking, aprendizado intensivo e feedback em tempo real. Estes são cuidadosamente planejados para garantir o máximo valor para todos os participantes.
    """)

def desenvolvimento_pessoal():
    st.write("""
    O foco no desenvolvimento pessoal é fundamental. Nosso objetivo é ajudar você a se tornar a melhor versão de si mesmo, através de técnicas comprovadas de autoconhecimento, disciplina e crescimento contínuo.
    """)

def sucesso_empresarial():
    st.write("""
    Ajudar empresas a terem sucesso é uma das nossas paixões. Através de nossas mentorias, fornecemos insights, estratégias e ações práticas que podem transformar positivamente a trajetória de sua empresa no mercado.
    """)

def metodo_mentoria_sacrificio():
    st.write("""
    Nosso programa é baseado em três pilares: método, mentoria e sacrifício. Combinamos técnicas eficazes, orientação personalizada e a compreensão de que o crescimento exige esforço e dedicação. Estamos aqui para guiá-lo nessa jornada.
    """)


    st.write("""
    Nosso programa é baseado em três pilares: método, mentoria e sacrifício. Combinamos técnicas eficazes, orientação personalizada e a compreensão de que o crescimento exige esforço e dedicação. Estamos aqui para guiá-lo nessa jornada.
    """)

def get_last_messages(chat_id, limit=5):
    updates = bot.get_updates()  # Obter todas as atualizações
    messages = [upd.message for upd in updates if upd.message.chat.id == int(chat_id)]
    return messages[-limit:]  # Retornar as últimas 'limit' mensagens


menu = st.sidebar.radio(
    "Menu",
    ("Sobre a Mentoria", "Depoimentos", "Contatos", "Rádio")
)

# Definição do conteúdo de cada seção
if menu == "Sobre a Mentoria":
    st.header("Sobre a Mentoria")
    st.write("Conheça mentoria (acesse o menu na lateral superior para mais informações)")
    with st.expander("Aulas Virtuais"):
            aulas_virtuais()
        
    with st.expander("Grupo no Telegram"):
            grupo_telegram()
        
    with st.expander("Encontros Presenciais"):
            encontros_presenciais()
    st.write("Qual o objetivo?")
        
    with st.expander("Desenvolvimento Pessoal"):
            desenvolvimento_pessoal()
        
    with st.expander("Sucesso Empresarial"):
            sucesso_empresarial()
        
    with st.expander("Método, Mentoria e Sacrifício"):
            metodo_mentoria_sacrificio()

elif menu == "Comunidade":
    # Interface do Streamlit
    st.title('Últimas Mensagens do Telegram de nossa comunidade aberta')

    if st.button('Atualizar Mensagens'):
        last_messages = get_last_messages(CHAT_ID, 5)
        for msg in last_messages:
            st.write(f"{msg.date}: {msg.text}")

    st.write('Clique no botão acima para atualizar as mensagens.')

elif menu == "Empresas Parceiras":
    st.header("Placeholder 2")
    st.write("Conteúdo em desenvolvimento.")

elif menu == "Depoimentos":
    st.header("Depoimentos")
    # Adicione aqui sua descrição para a seção de depoimentos
    st.write("Veja o que as pessoas estão dizendo sobre nossa mentoria.")
    # Inserindo o vídeo de depoimentos
    st.video('https://youtu.be/Flz4tVwtmm8')

if menu == "Contatos":
    st.header("Contatos")
    # Criando o formulário no Streamlit
    with st.form("form_contato", clear_on_submit=True):
        st.write("Preencha o formulário abaixo para entrar em contato conosco:")
        nome = st.text_input("Nome")
        email = st.text_input("Email")
        mensagem = st.text_area("Mensagem")
        submit_button = st.form_submit_button("Enviar")

        # Quando o formulário for enviado
        if submit_button:
            # Aqui você chamaria enviar_email(nome, email, mensagem) e trata o retorno
            enviado = enviar_email(nome, email, mensagem)  # substitua isso pela sua lógica real de envio
            if enviado:
                st.success("Mensagem enviada com sucesso!")
            else:
                st.error("Falha ao enviar a mensagem.")

elif menu == "Rádio":
    st.header("Reprodução de Áudios")
    # Função auxiliar para obter o caminho absoluto dos recursos
    def get_resource_path(relative_path):
        current_dir = os.path.dirname(__file__)
        return os.path.join(current_dir, relative_path)

    # Estrutura dos temas com caminhos relativos
    temas = {
        "Sucesso": "resources/audios/Sucesso",
        "Vida": "resources/audios/Vida",
        # Adicione mais temas conforme necessário
    }

    # Menu para escolher o tema do áudio
    tema_selecionado = st.sidebar.selectbox("Escolha um tema", list(temas.keys()))

    # Listar arquivos de áudio do tema selecionado
    caminho_tema = get_resource_path(temas[tema_selecionado])
    try:
        arquivos_audio = os.listdir(caminho_tema)
    except FileNotFoundError:
        st.error("Diretório não encontrado. Por favor, verifique o caminho do tema.")
        arquivos_audio = []

    if arquivos_audio:
        # Menu para escolher um áudio para tocar
        audio_selecionado = st.sidebar.selectbox("Escolha um áudio", arquivos_audio)

        # Reproduzir o áudio selecionado
        caminho_completo_audio = os.path.join(caminho_tema, audio_selecionado)
        with open(caminho_completo_audio, "rb") as audio_file:
            audio_bytes = audio_file.read()

        st.audio(audio_bytes, format="audio/wav", start_time=0)
    else:
        st.write("Nenhum arquivo de áudio encontrado para o tema selecionado.")
