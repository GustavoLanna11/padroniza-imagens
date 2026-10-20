import os
from PIL import Image

# Configurações de pastas
PASTA_ORIGEM = "dataset" # Pasta mostrada no seu VS Code
PASTA_DESTINO = "dataset_padronizado" # Pasta nova que será gerada
TAMANHO_PADRAO = (224, 224) # Largura x Altura em pixels

for raiz, subpastas, arquivos in os.walk(PASTA_ORIGEM):
    # Replica a estrutura de pastas (train/val e subpastas de classes)
    caminho_relativo = os.path.relpath(raiz, PASTA_ORIGEM)
    pasta_saida = os.path.join(PASTA_DESTINO, caminho_relativo)
    os.makedirs(pasta_saida, exist_ok=True)

    for arquivo in arquivos:
        if arquivo.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.webp')):
            caminho_origem_img = os.path.join(raiz, arquivo)
            caminho_destino_img = os.path.join(pasta_saida, arquivo)

            try:
                with Image.open(caminho_origem_img) as img:
                    # Converte para RGB
                    img = img.convert('RGB')
                    
                    # Redimensiona com alta qualidade
                    img_resized = img.resize(TAMANHO_PADRAO, Image.Resampling.LANCZOS)
                    
                    # Salva no novo diretório
                    img_resized.save(caminho_destino_img)
            except Exception as e:
                print(f"Erro ao processar {caminho_origem_img}: {e}")

print("Concluído! Todas as subpastas foram processadas e salvas em 'dataset_padronizado'.")