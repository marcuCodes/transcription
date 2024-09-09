from tkinter import *
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip
from PIL import Image, ImageTk
import whisper, threading
from docx import Document

video_file_path = ""
transcribing = False

def btn_clicked():
    global video_file_path
    global transcribing
    if not transcribing:
        filename = filedialog.askopenfilename(title='Selecione o vídeo que deseja transcrever', filetypes=[("Video Files", "*.mp4;*.avi;*.mov")])
        if filename == "":
            messagebox.showerror('Arquivo a ser transcrito', 'Defina o arquivo a ser transcrito!')
            img_label.place_forget()
        elif filename:
                confirmacao_arquivo = messagebox.askquestion('Confirmação arquivo', f'Tem certeza que deseja transcrever o seguinte arquivo: "{filename}"?')
                video_file_path = filename

                if confirmacao_arquivo == 'yes':
                    try:
                        clip = VideoFileClip(filename)
                        frame = clip.get_frame(0)
                        frame_image = Image.fromarray(frame)
                        frame_image = frame_image.resize((b1.winfo_width(), b1.winfo_height()))
                        frame_photo = ImageTk.PhotoImage(frame_image)
                        img_label.config(image=frame_photo)
                        img_label.image = frame_photo
                        img_label.place(x=b1.winfo_x(), y=b1.winfo_y())
                        b0.config(state='normal')
                        b0.place(
                        x=244, y=489,
                        width=211,
                        height=52)
                    except Exception as e:
                        pass
                else:
                    messagebox.showerror('Arquivo a ser transcrito', 'Defina o arquivo a ser transcrito!')
                    img_label.place_forget()

def img_label_clicked(event):
    btn_clicked()

def transcribe_video(video_path):
    modelo = whisper.load_model("small")
    resposta = modelo.transcribe(video_path, fp16=False)
    texto = resposta["text"]
    return texto

def remove_amara_subtitle(text):
    return text.replace("Legendas pela comunidade de Amara.org", "").strip()

def process_transcription():
    global video_file_path
    global transcribing
    if video_file_path and not transcribing:
        transcribing = True
        b0.place_forget()
        b0.config(state="disabled")
        b1.config(state="disabled")
        transcribing_label.place(x=200, y=569.1)
        threading.Thread(target=transcribe_and_save).start()

def transcribe_and_save():
    global video_file_path
    global transcribing
    transcribed_text = transcribe_video(video_file_path)
    transcribed_text = remove_amara_subtitle(transcribed_text)
    transcribing_label.place_forget()
    messagebox.showinfo('Transcrição concluída!', 'Concluída a transcrição do vídeo. Agora, selecione onde salvar o arquivo com a transcrição e nomeie o mesmo.')
    output_file_path = filedialog.asksaveasfilename(title='Onde salvar a transcrição do vídeo?', defaultextension=".docx", filetypes=[("Documentos do Word", "*.docx")])
            
    if output_file_path:
        output_file = output_file_path
        doc = Document()
        doc.add_paragraph(transcribed_text)
        doc.save(output_file)
        messagebox.showinfo('Destino do arquivo', f"A transcrição do vídeo foi salva com sucesso em: '{output_file}'")
        b0.config(state="normal")
        b1.config(state="normal")
        transcribing = False
        img_label.place_forget()
    else:                   
        b0.config(state="normal")
        b1.config(state="normal")
        transcribing = False
        img_label.place_forget()

window = Tk()

largura_janela = 700
altura_janela = 700

largura_tela = window.winfo_screenwidth()
altura_tela = window.winfo_screenheight()

pos_x = (largura_tela - largura_janela) // 2
pos_y = (altura_tela - altura_janela) // 2

window.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

window.title('Transcrição de Vídeos')

icone_transcricao = Image.open('icon_record_preto.png')
photo_transcricao = ImageTk.PhotoImage(icone_transcricao)
window.wm_iconphoto(False, photo_transcricao)

window.geometry("700x700")
window.configure(bg="#ffffff")
canvas = Canvas(
    window,
    bg="#ffffff",
    height=altura_janela,
    width=largura_janela,
    bd=0,
    highlightthickness=0,
    relief="ridge")
canvas.place(x=0, y=0)

background_img = PhotoImage(file="background.png")
background = canvas.create_image(
    largura_janela / 2, altura_janela / 2,
    image=background_img)

img0 = PhotoImage(file="img0.png")
b0 = Button(
    image=img0,
    borderwidth=0,
    highlightthickness=0,
    command=process_transcription,
    relief="flat",
    cursor='hand2',
    state='disabled')

img1 = PhotoImage(file="img1.png")
b1 = Button(
    image=img1,
    borderwidth=0,
    highlightthickness=0,
    command=btn_clicked,
    relief="flat",
    cursor='hand2')

b1.place(
    x=47, y=193,
    width=606,
    height=248)

img_label = Label(window)
img_label.place(x=-1000, y=-1000)
img_label.bind("<Button-1>", img_label_clicked)

transcribing_img = PhotoImage(file="transcrevendo.png")
transcribing_label = Label(window, image=transcribing_img, bg="#ffffff")
transcribing_label.image = transcribing_img

window.resizable(False, False)
window.mainloop()