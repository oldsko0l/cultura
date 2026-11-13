# Atualiza a barra de progresso dos livros e o resumo do README.
# Uso: python scripts/atualizar.py

from pathlib import Path
from datetime import date

RAIZ = Path(__file__).resolve().parent.parent

INICIO = "<!-- resumo:inicio -->"
FIM = "<!-- resumo:fim -->"

# arquivo, nome no resumo, seção em andamento, seção da fila, seção dos concluídos
CATEGORIAS = [
    ("livros.md", "Livros", "Lendo agora", "Quero ler", "Lidos"),
    ("filmes.md", "Filmes", None, "Quero ver", "Vistos"),
    ("series.md", "Séries", "Assistindo", "Quero ver", "Concluídas"),
    ("documentarios.md", "Documentários", None, "Quero ver", "Vistos"),
    ("videos.md", "Vídeos", None, "Ver depois", "Vistos"),
    ("outros.md", "Outros", None, "Na fila", "Concluídos"),
]


def celulas(linha):
    return [c.strip() for c in linha.strip().strip("|").split("|")]


def eh_linha_de_dados(linha):
    if not linha.strip().startswith("|"):
        return False
    if set(linha.replace("|", "").strip()) <= set("-: "):
        return False  # linha separadora |---|---|
    return True


def ler_secoes(texto):
    """Devolve {nome da seção: [linhas da tabela, sem cabeçalho]}"""
    secoes = {}
    atual = None
    viu_cabecalho = False
    for linha in texto.splitlines():
        if linha.startswith("## "):
            atual = linha[3:].strip()
            secoes[atual] = []
            viu_cabecalho = False
        elif atual and eh_linha_de_dados(linha):
            if not viu_cabecalho:
                viu_cabecalho = True  # primeira linha da tabela é o cabeçalho
                continue
            c = celulas(linha)
            if c[0] in ("", "-"):
                continue  # marcador de tabela vazia
            secoes[atual].append(c)
    return secoes


def barra(pagina, total, tamanho=10):
    pct = min(pagina / total, 1)
    cheios = round(pct * tamanho)
    return f"`{'█' * cheios}{'░' * (tamanho - cheios)}` {round(pct * 100)}%"


def numero(texto):
    try:
        return int(texto)
    except ValueError:
        return None


def atualizar_livros():
    arquivo = RAIZ / "livros.md"
    linhas = arquivo.read_text(encoding="utf-8").splitlines()
    secao = None
    cabecalho_visto = False

    for i, linha in enumerate(linhas):
        if linha.startswith("## "):
            secao = linha[3:].strip()
            cabecalho_visto = False
            continue
        if secao != "Lendo agora" or not eh_linha_de_dados(linha):
            continue
        if not cabecalho_visto:
            cabecalho_visto = True
            continue

        c = celulas(linha)
        if c[0] in ("", "-") or len(c) < 6:
            continue
        pagina, total = numero(c[2]), numero(c[3])
        if pagina is not None and total:
            c[4] = barra(pagina, total)
            linhas[i] = "| " + " | ".join(c) + " |"

    arquivo.write_text("\n".join(linhas) + "\n", encoding="utf-8")


def montar_resumo():
    partes = []
    dados = {}
    for nome_arq, nome, andamento, fila, concluidos in CATEGORIAS:
        dados[nome_arq] = ler_secoes((RAIZ / nome_arq).read_text(encoding="utf-8"))

    # lendo agora
    partes.append("### Lendo\n")
    lendo = dados["livros.md"].get("Lendo agora", [])
    if lendo:
        for c in lendo:
            pagina, total = numero(c[2]), numero(c[3])
            linha = f"- **{c[0]}**"
            if c[1]:
                linha += f" ({c[1]})"
            if pagina is not None and total:
                linha += f": {barra(pagina, total)}, página {pagina} de {total}"
            partes.append(linha)
    else:
        partes.append("_Nenhum livro em andamento._")

    # assistindo
    partes.append("\n### Assistindo\n")
    assistindo = dados["series.md"].get("Assistindo", [])
    if assistindo:
        for c in assistindo:
            linha = f"- **{c[0]}**"
            if c[1]:
                linha += f" ({c[1]})"
            if c[2] or c[3]:
                linha += f": temporada {c[2] or '?'}, episódio {c[3] or '?'}"
            partes.append(linha)
    else:
        partes.append("_Nenhuma série em andamento._")

    # números
    partes.append("\n### Números\n")
    partes.append("| Categoria | Em andamento | Na fila | Concluídos |")
    partes.append("|---|---|---|---|")
    for nome_arq, nome, andamento, fila, concluidos in CATEGORIAS:
        s = dados[nome_arq]
        qtd_andamento = str(len(s.get(andamento, []))) if andamento else "-"
        partes.append(
            f"| [{nome}]({nome_arq}) | {qtd_andamento} | {len(s.get(fila, []))} | {len(s.get(concluidos, []))} |"
        )

    partes.append("\nAtualizado em " + date.today().strftime("%d/%m/%Y"))
    return "\n".join(partes)


def main():
    atualizar_livros()

    readme = RAIZ / "README.md"
    texto = readme.read_text(encoding="utf-8")
    if INICIO not in texto or FIM not in texto:
        print("Não achei os marcadores do resumo no README.md")
        return

    antes = texto.split(INICIO)[0]
    depois = texto.split(FIM)[1]
    readme.write_text(antes + INICIO + "\n" + montar_resumo() + "\n" + FIM + depois, encoding="utf-8")
    print("Resumo e progresso dos livros atualizados.")


if __name__ == "__main__":
    main()
