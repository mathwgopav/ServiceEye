# import os, sys
from tkinter import *
from tkinter import messagebox  # Importação do messagebox para exibir mensagens
import asyncio
import threading
import subprocess
from serviceEye import ServiceEye

# Função para rodar o loop do asyncio em uma thread separada
def run_asyncio_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

# Função para atualizar o status dos sites
def update_status_label(results):
    error_sites = [result for result in results if "erro" in result.lower() or "respondeu com o código" in result.lower()]
    if error_sites:
        status_label.config(text="Alguns sites estão fora do ar.", fg="red")
    else:
        status_label.config(text="Todos os sites cadastrados estão no ar. Confira o log", fg="green")

# Iniciar o monitoramento após apertar o botão "Ir!"
def start_monitoring(timer_value):
    try:
        timer = int(timer_value)
        async def monitor():
            while True:
                results = await serviceEye.check_services_health()
                update_status_label(results)
                await asyncio.sleep(timer)

        asyncio.run_coroutine_threadsafe(monitor(), loop)
        input_timer.delete(0, END)  # Apaga o input do timer após setá-lo
    except ValueError:
        messagebox.showerror("Erro de Entrada", "Por favor, insira um número válido para o timer.")

# Adicionar URL
def add_url():
    url = input_url.get()
    if url:
        serviceEye.add_url(url)
        messagebox.showinfo("Sucesso", f"URL '{url}' adicionada com sucesso!")
        input_url.delete(0, END)  # Apaga o input de URL após adicionar
    else:
        messagebox.showerror("Erro de Entrada", "Por favor, insira uma URL válida.")

# Abrir logs no Bloco de Notas
def open_logs_in_notepad():
    if os.path.exists(serviceEye.logpath):
        subprocess.Popen(['notepad.exe', serviceEye.logpath])
    else:
        messagebox.showinfo("Logs", "Nenhum log disponível ainda.")

# Inicializa a janela Tkinter
root = Tk()
root.title("ServiceEye")
# icon = os.path.join(sys.path[0], "./assets/favicon.ico")
# root.iconbitmap(icon)

# Definir o tamanho da janela
root.geometry("400x350")

# Centralizar a janela na tela
root.eval('tk::PlaceWindow . center')

# Inicializa a instância do ServiceEye
serviceEye = ServiceEye()

# Cria um novo loop asyncio em uma thread separada
loop = asyncio.new_event_loop()
threading.Thread(target=run_asyncio_loop, args=(loop,), daemon=True).start()

# Frame principal para centralizar os elementos
main_frame = Frame(root)
main_frame.pack(expand=True)

# Label para URL
text_url = Label(main_frame, text="Cadastre as URLs que deseja verificar o status")
text_url.grid(column=0, row=0, columnspan=2, pady=10)

# Input para URL
input_url = Entry(main_frame, width=40)
input_url.grid(column=0, row=1, padx=10, pady=5)

# Botão para adicionar URL
btn_add = Button(main_frame, text="Add", command=add_url)
btn_add.grid(column=1, row=1, padx=10, pady=5)

# Label para o timer
text_timer = Label(main_frame, text="Digite de quanto em quanto tempo quer verificar")
text_timer.grid(column=0, row=2, columnspan=2, pady=10)

# Input para o timer
input_timer = Entry(main_frame, width=40)
input_timer.grid(column=0, row=3, padx=10, pady=5)

# Botão para definir o timer
btn_set_timer = Button(main_frame, text="Ir!", command=lambda: start_monitoring(input_timer.get()))
btn_set_timer.grid(column=0, row=4, padx=10, pady=10)

# Botão para abrir logs no Bloco de Notas
btn_log = Button(main_frame, text="Log", command=open_logs_in_notepad)
btn_log.grid(column=1, row=4, padx=10, pady=10)

# Label para exibir o status dos sites
status_label = Label(main_frame, text="Aguardando iniciar...", fg="blue")
status_label.grid(column=0, row=5, columnspan=2, pady=10)

# Loop principal do Tkinter
root.mainloop()
