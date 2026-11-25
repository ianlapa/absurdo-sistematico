# Absurdo Sistemático — simulações

Perguntas da filosofia transformadas em experimentos de computador.

Esta pasta tem o código das simulações e das animações dos vídeos do canal **Absurdo Sistemático**. A ideia é simples: qualquer número que aparece num vídeo pode ser conferido aqui. Rode o modelo, mude um parâmetro e veja o que acontece.

## Episódios

| Episódio | Pergunta | Modelo | Pasta |
| --- | --- | --- | --- |
| 1 | Por que pessoas razoáveis se polarizam? | Confiança limitada (Hegselmann & Krause, 2002) | [`ep01_polarizacao`](ep01_polarizacao/) |
| 2 | E se tiver gente que nunca muda de ideia? | Confiança limitada com teimosos (Hegselmann & Krause, 2015) | [`ep02_teimosos`](ep02_teimosos/) |

## Como rodar

Você precisa de Python 3.10 ou mais novo. Todos os comandos abaixo são rodados de dentro desta pasta (`simulacoes/`).

```bash
pip install -r requirements.txt

# só o modelo: imprime os resultados citados no vídeo (rápido)
python ep01_polarizacao/modelo.py
python ep01_polarizacao/modelo.py 0.2     # experimente outra tolerância

# as animações do vídeo (precisa do ffmpeg; leva alguns minutos)
cd ep01_polarizacao
python gerar_clipes.py                    # todos os clipes, na pasta saida/
python gerar_clipes.py regra codigo       # só alguns
```

Para gerar os vídeos, instale o [ffmpeg](https://ffmpeg.org): no Mac, `brew install ffmpeg`; no Ubuntu, `sudo apt install ffmpeg`; no Windows, `winget install ffmpeg`. Os arquivos `modelo.py` não precisam dele.

## Estrutura

```
simulacoes/
├── comum/estilo.py        # cores, fontes e utilitários de animação usados por todos os episódios
├── marca/                 # logo e símbolo (não fazem parte da licença MIT, veja abaixo)
├── ep01_polarizacao/
│   ├── modelo.py          # a simulação, curta e comentada
│   ├── gerar_clipes.py    # as animações do vídeo
│   └── README.md
└── ep02_teimosos/
    ├── modelo.py
    ├── gerar_clipes.py
    └── README.md
```

Cada `modelo.py` é independente e só usa `numpy`: dá para ler de cima a baixo e entender a regra inteira.

## Sobre os modelos

São caricaturas deliberadas, no espírito de um experimento mental: tiram tudo do caminho para isolar um único fator e ver o que ele faz sozinho. Mostram o que *pode* acontecer sob certas regras, não o que acontece na sociedade real. Os vídeos discutem esses limites.

Os resultados dependem do sorteio inicial (`seed`). Os vídeos usam um sorteio fixo para que os números sejam reproduzíveis; quando um resultado vale "em geral", ele é uma média de muitas sociedades sorteadas, e o código diz quantas.

## Licença

- **Código desta pasta:** licença MIT (arquivo [`LICENSE`](LICENSE)). Use, modifique e redistribua à vontade, mantendo o aviso de copyright.
- **Marca:** o nome Absurdo Sistemático, o logo e o símbolo (pasta [`marca/`](marca/)) **não** estão incluídos na licença MIT. Todos os direitos reservados.

Se você usar o código num trabalho seu, uma menção ao canal é bem-vinda.
