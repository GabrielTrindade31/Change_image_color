from PIL import Image
import os

# Verifica se o arquivo existe
caminho = "vs_code_python\.vscode\control.png"
if os.path.exists(caminho):
    print("O arquivo existe!")
else:
    print("O arquivo não existe!")

# Abre a imagem
imagem = Image.open(caminho)

# Obtém os pixels da imagem
pixels = imagem.load()

# Percorre todos os pixels da imagem
for x in range(imagem.width):
    for y in range(imagem.height):
        # Verifica se o pixel está na gama de cores desejada
        if ((pixels[x, y][2] > 150) and (pixels[x, y][1] > 40 ) and (pixels[x, y][0] >= 0) and (pixels[x, y][2] < 253) and (pixels[x, y][1] < 165 ) and (pixels[x, y][0] < 132)):
            # Troca a cor do pixel para verde
            cor_atual = pixels[x, y]
            # Cria uma nova tupla com os valores atualizados trocando o valor do azul com o verde
            vermelho = pixels[x, y][0]
            azul = pixels[x, y][2]
            verde = pixels[x, y][1]
            nova_cor = (vermelho - 80 , verde - 185, azul - 210)

            # Atribui a nova cor ao pixel
            pixels[x, y] = nova_cor

# Salva a nova imagem
imagem.save("vs_code_python\.vscode\imagemova.png")
