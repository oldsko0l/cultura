# Cultura

Registro do que eu leio, assisto e encontro de interessante: livros, filmes, séries, documentários, vídeos e o que mais aparecer. Serve para lembrar o que já vi, guardar o que quero ver e acompanhar o progresso das leituras.

## Agora

<!-- resumo:inicio -->
### Lendo

_Nenhum livro em andamento._

### Assistindo

_Nenhuma série em andamento._

### Números

| Categoria | Em andamento | Na fila | Concluídos |
|---|---|---|---|
| [Livros](livros.md) | 0 | 0 | 0 |
| [Filmes](filmes.md) | - | 0 | 0 |
| [Séries](series.md) | 0 | 0 | 0 |
| [Documentários](documentarios.md) | - | 0 | 0 |
| [Vídeos](videos.md) | - | 0 | 0 |
| [Outros](outros.md) | - | 0 | 0 |

Atualizado em 13/11/2026
<!-- resumo:fim -->

## Arquivos

| Arquivo | O que guarda |
|---|---|
| [livros.md](livros.md) | Lendo agora (com progresso), quero ler, lidos |
| [filmes.md](filmes.md) | Quero ver, vistos |
| [series.md](series.md) | Assistindo, quero ver, concluídas |
| [documentarios.md](documentarios.md) | Quero ver, vistos |
| [videos.md](videos.md) | Vídeos e aulas soltas que valeram a pena |
| [outros.md](outros.md) | Podcasts, álbuns, artigos, exposições, peças |
| [resenhas/](resenhas/) | Textos mais longos sobre algo que me marcou |

## Como registrar

- **Livro novo na fila:** adicionar uma linha em "Quero ler".
- **Comecei a ler:** mover a linha para "Lendo agora" com a página atual e o total de páginas.
- **Avancei na leitura:** trocar só o número da página.
- **Terminei:** mover para "Lidos" com a data, a nota e um comentário curto.
- O mesmo vale para séries ("Assistindo" com temporada e episódio) e para o resto.

Depois de mexer nos arquivos, rodar:

```bash
python scripts/atualizar.py
```

O script calcula a barra de progresso dos livros e atualiza o resumo desta página.

Notas de 0 a 5. Linhas com `-` na primeira coluna são só marcadores de tabela vazia: podem ser apagadas quando entrar o primeiro item.

Para uma resenha mais longa, copiar `templates/resenha.md` para `resenhas/` com o nome da obra (ex.: `resenhas/a-morte-de-ivan-ilitch.md`) e linkar na tabela.
