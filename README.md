# pausa-musica-windows

Pausa a música automaticamente quando um vídeo começa a tocar no navegador, e retoma quando o vídeo para.

Feito para o **YouTube Music Desktop App** no Windows, mas funciona com qualquer player que apareça no painel de mídia do Windows (Spotify, por exemplo).

## Como funciona

O Windows mantém uma lista dos players que estão tocando: é o painel que aparece quando você aperta as teclas de volume. O script lê essa lista a cada meio segundo:

- Se algum **navegador** (Chrome, Edge, Firefox, Brave, Opera, Vivaldi) está tocando, ele pausa os outros players.
- Quando o vídeo para, ele espera meio segundo e retoma **só a música que ele mesmo pausou**. Se você tinha pausado a música por conta própria, ela continua parada.
- A espera antes de retomar evita que a música fique pausando e voltando na troca de anúncio para vídeo.

## Requisitos

- Windows 10 ou 11
- Python 3.9+
- No YouTube Music Desktop App: **Settings → Integrations → "Enable Windows 10 media service"**, depois reinicie o app

## Instalação

```bat
git clone https://github.com/SEU-USUARIO/pausa-musica-windows.git
cd pausa-musica-windows
instalar.bat
```

Ou, sem o `.bat`:

```bat
python -m pip install -r requirements.txt
```

## Uso

```bat
python pausa_musica.py --listar   :: mostra os players que o Windows enxerga
python pausa_musica.py            :: roda o monitor (Ctrl+C para sair)
```

O `--listar` ajuda a conferir se o app de música aparece. Se não aparecer, a integração com o Windows não está ligada.

### Rodar escondido junto com o Windows

1. `Win + R` → digite `shell:startup` → Enter
2. Coloque nessa pasta um **atalho** para o `iniciar_oculto.vbs`

Para iniciar na hora sem reiniciar, dê dois cliques no `iniciar_oculto.vbs`. Para parar, finalize o processo `pythonw.exe` no Gerenciador de Tarefas.

## Configuração

No topo do `pausa_musica.py`:

| Variável | O que faz |
|---|---|
| `ID_NAVEGADOR` | Trechos de ID que contam como "vídeo". Qualquer outro player é tratado como música. |
| `INTERVALO` | Segundos entre verificações. |
| `RETOMAR_APOS` | Espera antes de retomar a música. |

## Licença

[MIT](LICENSE)
