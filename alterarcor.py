import tkinter as tk
from tkinter import filedialog, Scale, Toplevel, StringVar, Radiobutton, IntVar, DoubleVar  # Add DoubleVar
from PIL import Image, ImageTk



# Variáveis globais
imagem = None
imagem_modificada = None

# Função para abrir o arquivo de imagem
def abrir_arquivo():
    global imagem
    caminho = filedialog.askopenfilename()
    imagem = Image.open(caminho)

    # Exibir a imagem original
    imagem_tk = ImageTk.PhotoImage(imagem)
    imagem_label.config(image=imagem_tk)
    imagem_label.image = imagem_tk

# Função para aplicar a substituição de cor
# Função para identificar se a imagem é RGB ou RGBA
def identificar_canais():
    if imagem:
        if imagem.mode == "RGBA":
            return True
        elif imagem.mode == "RGB":
            return False

# Função para acrescentar valores ao canal A
def abrir_janela_acrescentar_alpha():
    janela_acrescentar_alpha = Toplevel(root)
    janela_acrescentar_alpha.title("Acrescentar Valor ao Canal A")

    # Slider para adicionar valor ao canal A
    slider_alpha = Scale(janela_acrescentar_alpha, from_=0.0, to=1.0, resolution=0.01, orient=tk.HORIZONTAL, length=200, label="Adicionar ao Canal A")
    slider_alpha.set(acresc_alpha_var.get())
    slider_alpha.pack()

    # Botão para confirmar e aplicar o valor
    botao_confirmar_alpha = tk.Button(janela_acrescentar_alpha, text="Confirmar", command=lambda: salvar_e_acrescentar_alpha(slider_alpha.get(), janela_acrescentar_alpha))
    botao_confirmar_alpha.pack()

# Função para salvar e acrescentar valor ao canal A
def salvar_e_acrescentar_alpha(acresc_alpha, janela):
    acresc_alpha_var.set(acresc_alpha)
    janela.destroy()
    aplicar_cor()  # Chamar a função para atualizar a imagem modificada após a alteração do canal A

# Criar variável para armazenar o valor de acrescentar ao canal A
def aplicar_cor():
    global imagem, imagem_modificada

    def dentro_da_faixa(pixel, r_faixa, g_faixa, b_faixa):
        r, g, b, _ = pixel
        return r_faixa[0] <= r <= r_faixa[1] and g_faixa[0] <= g <= g_faixa[1] and b_faixa[0] <= b <= b_faixa[1]

    if imagem:
        r_min_val, r_max_val = r_min.get(), r_max.get()
        g_min_val, g_max_val = g_min.get(), g_max.get()
        b_min_val, b_max_val = b_min.get(), b_max.get()
        a_val = acresc_alpha_var.get()  # Valor do canal A

        # Função para converter um pixel em um novo pixel
        def converter_pixel(pixel):
            nonlocal r_min_val, r_max_val, g_min_val, g_max_val, b_min_val, b_max_val, a_val
            if dentro_da_faixa(pixel, (r_min_val, r_max_val), (g_min_val, g_max_val), (b_min_val, b_max_val)):
                # Acrescentar os valores especificados nos canais R, G, B e A
                r, g, b, a = pixel
                r += acresc_r_var.get()
                g += acresc_g_var.get()
                b += acresc_b_var.get()
                a += a_val

                # Limitar os valores para estar no intervalo de 0 a 255 e 0.0 a 1.0
                r = max(0, min(255, int(r)))
                g = max(0, min(255, int(g)))
                b = max(0, min(255, int(b)))
                a = max(0, min(255, int(a * 255)))  # Scale float alpha to integer range (0-255)

                # Verificar a escolha da ordem dos canais
                if ordem_var.get() == "RGBA":
                    return (r, g, b, a)
                elif ordem_var.get() == "RBGA":
                    return (r, b, g, a)
                elif ordem_var.get() == "BGRA":
                    return (b, g, r, a)
                elif ordem_var.get() == "BRGA":
                    return (b, r, g, a)
                elif ordem_var.get() == "GRBA":
                    return (g, r, b, a)
                elif ordem_var.get() == "GBRA":
                    return (g, b, r, a)
            return pixel


        # Aplicar a substituição de cor à imagem
        imagem_modificada = imagem.convert("RGBA" if identificar_canais() else "RGB")
        imagem_modificada.putdata(list(map(converter_pixel, imagem.getdata())))

        # Exibir a imagem modificada
        imagem_tk = ImageTk.PhotoImage(imagem_modificada)
        imagem_label.config(image=imagem_tk)
        imagem_label.image = imagem_tk

# Função para criar um frame de faixa de valores
def create_range_frame():
    range_frame = tk.Frame(root)
    range_frame.pack()

    # Configuração para o canal R (vermelho)
    r_label = tk.Label(range_frame, text="Canal R:")
    r_label.pack(side=tk.LEFT)

    r_min_scale = Scale(range_frame, from_=0, to=255, orient=tk.HORIZONTAL, length=200, label="Min")
    r_min_scale.pack(side=tk.LEFT)

    r_max_scale = Scale(range_frame, from_=0, to=255, orient=tk.HORIZONTAL, length=200, label="Max")
    r_max_scale.pack(side=tk.LEFT)

    # Configuração para o canal G (verde)
    g_label = tk.Label(range_frame, text="Canal G:")
    g_label.pack(side=tk.LEFT)

    g_min_scale = Scale(range_frame, from_=0, to=255, orient=tk.HORIZONTAL, length=200, label="Min")
    g_min_scale.pack(side=tk.LEFT)

    g_max_scale = Scale(range_frame, from_=0, to=255, orient=tk.HORIZONTAL, length=200, label="Max")
    g_max_scale.pack(side=tk.LEFT)

    # Configuração para o canal B (azul)
    b_label = tk.Label(range_frame, text="Canal B:")
    b_label.pack(side=tk.LEFT)

    b_min_scale = Scale(range_frame, from_=0, to=255, orient=tk.HORIZONTAL, length=200, label="Min")
    b_min_scale.pack(side=tk.LEFT)

    b_max_scale = Scale(range_frame, from_=0, to=255, orient=tk.HORIZONTAL, length=200, label="Max")
    b_max_scale.pack(side=tk.LEFT)

    return r_min_scale, r_max_scale, g_min_scale, g_max_scale, b_min_scale, b_max_scale

# Função para criar a janela de troca de ordem dos canais
def abrir_janela_trocar_ordem():
    janela_trocar = Toplevel(root)
    janela_trocar.title("Trocar Ordem dos Canais")

    opcoes = ["RGBA", "RBGA", "BGRA", "BRGA", "GRBA", "GBRA"]

    # Variável para armazenar a opção selecionada
    escolha_var = StringVar(value=ordem_var.get())

    # Criar botões de opção para as ordens dos canais
    for opcao in opcoes:
        botao_opcao = Radiobutton(janela_trocar, text=opcao, variable=escolha_var, value=opcao)
        botao_opcao.pack()

    # Botão para confirmar a escolha
    botao_confirmar = tk.Button(janela_trocar, text="Confirmar", command=lambda: salvar_e_trocar_ordem(escolha_var.get(), janela_trocar))
    botao_confirmar.pack()

# Função para salvar e trocar a ordem dos canais
def salvar_e_trocar_ordem(ordem, janela):
    ordem_var.set(ordem)
    janela.destroy()

# Função para criar a janela de acrescentar valores aos canais
def abrir_janela_acrescentar():
    janela_acrescentar = Toplevel(root)
    janela_acrescentar.title("Acrescentar Valores aos Canais")

    # Sliders para adicionar valores aos canais R, G, B
    slider_r = Scale(janela_acrescentar, from_=-255, to=255, orient=tk.HORIZONTAL, length=200, label="Adicionar ao Canal R")
    slider_r.set(acresc_r_var.get())
    slider_r.pack()

    slider_g = Scale(janela_acrescentar, from_=-255, to=255, orient=tk.HORIZONTAL, length=200, label="Adicionar ao Canal G")
    slider_g.set(acresc_g_var.get())
    slider_g.pack()

    slider_b = Scale(janela_acrescentar, from_=-255, to=255, orient=tk.HORIZONTAL, length=200, label="Adicionar ao Canal B")
    slider_b.set(acresc_b_var.get())
    slider_b.pack()

    # Botão para confirmar e aplicar os valores
    botao_confirmar = tk.Button(janela_acrescentar, text="Confirmar", command=lambda: salvar_e_acrescentar_valores(slider_r.get(), slider_g.get(), slider_b.get(), janela_acrescentar))
    botao_confirmar.pack()

# Função para salvar e acrescentar valores aos canais R, G, B
def salvar_e_acrescentar_valores(acresc_r, acresc_g, acresc_b, janela):
    acresc_r_var.set(acresc_r)
    acresc_g_var.set(acresc_g)
    acresc_b_var.set(acresc_b)
    janela.destroy()

# Função para salvar a imagem modificada
def salvar_imagem():
    global imagem_modificada
    if imagem_modificada:
        caminho = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Arquivos PNG", "*.png")])
        if caminho:
            imagem_modificada.save(caminho)

# Criar a janela principal
root = tk.Tk()
root.title("Substituição de cor")

# Criar um frame para os widgets
frame = tk.Frame(root)
frame.pack()

acresc_alpha_var = DoubleVar(value=1.0)
botao_acrescentar_alpha = tk.Button(frame, text="Acrescentar ao Canal A", command=abrir_janela_acrescentar_alpha)
botao_acrescentar_alpha.pack()
# Criar um botão para abrir o arquivo de imagem
abrir_arquivo_button = tk.Button(frame, text="Abrir arquivo", command=abrir_arquivo)
abrir_arquivo_button.pack()

# Criar um rótulo para exibir a imagem modificada
imagem_label = tk.Label(root)
imagem_label.pack()

# Criar um botão para aplicar a substituição de cor
aplicar_button = tk.Button(frame, text="Aplicar cor", command=aplicar_cor)
aplicar_button.pack()

# Criar um frame de faixa de valores
r_min, r_max, g_min, g_max, b_min, b_max = create_range_frame()

# Criar variáveis para armazenar a escolha de ordem e os valores de acrescentar
ordem_var = StringVar(value="RGBA")
acresc_r_var = IntVar(value=0)
acresc_g_var = IntVar(value=0)
acresc_b_var = IntVar(value=0)

# Criar botões "Trocar" e "Acrescentar"
botao_trocar = tk.Button(frame, text="Trocar", command=abrir_janela_trocar_ordem)
botao_trocar.pack()

botao_acrescentar = tk.Button(frame, text="Acrescentar", command=abrir_janela_acrescentar)
botao_acrescentar.pack()

# Botão para salvar a imagem
botao_salvar = tk.Button(frame, text="Salvar Imagem", command=salvar_imagem)
botao_salvar.pack()

# Iniciar o loop principal
root.mainloop()
