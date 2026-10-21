import os
from PIL import Image

# Configurações de pastas
PASTA_ORIGEM = "dataset"
PASTA_DESTINO = "dataset_padronizado"
TAMANHO_PADRAO = (224, 224)

# Mapeamento do nome do diretório pai para o sufixo desejado
SUFIXO_TIPO = {
    'train': 'treino',
    'val': 'valido'
}

for raiz, subpastas, arquivos in os.walk(PASTA_ORIGEM):
    # Replica a estrutura de pastas no diretório de saída
    caminho_relativo = os.path.relpath(raiz, PASTA_ORIGEM)
    pasta_saida = os.path.join(PASTA_DESTINO, caminho_relativo)
    os.makedirs(pasta_saida, exist_ok=True)

    # Identifica a categoria atual (ex: 'asa-deformada', 'normal', 'varroa')
    nome_categoria = os.path.basename(raiz)

    # Descobre se está dentro de 'train' ou 'val' verificando a pasta pai
    partes_caminho = caminho_relativo.split(os.sep)
    tipo_conjunto = partes_caminho[0] if len(partes_caminho) > 0 else ''
    sufixo = SUFIXO_TIPO.get(tipo_conjunto, '')

    # Contador para a sequência numérica
    contador = 1

    # Filtra e ordena as imagens
    imagens = [f for f in arquivos if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.webp'))]
    imagens.sort()

    for arquivo in imagens:
        caminho_origem_img = os.path.join(raiz, arquivo)
        _, extensao = os.path.splitext(arquivo)

        # Formata o nome como: {categoria}_{treino/valido}{numero}.extensao
        if nome_categoria in ['asa-deformada', 'normal', 'varroa'] and sufixo:
            novo_nome = f"{nome_categoria}_{sufixo}{contador}{extensao}"
        else:
            novo_nome = arquivo

        caminho_destino_img = os.path.join(pasta_saida, novo_nome)

        try:
            with Image.open(caminho_origem_img) as img:
                img = img.convert('RGB')
                img_resized = img.resize(TAMANHO_PADRAO, Image.Resampling.LANCZOS)
                img_resized.save(caminho_destino_img)
                contador += 1
        except Exception as e:
            print(f"Erro ao processar {caminho_origem_img}: {e}")

print("Concluído! As imagens foram redimensionadas e renomeadas no padrão sequencial.")