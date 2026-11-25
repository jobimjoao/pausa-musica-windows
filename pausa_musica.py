"""
Pausa a música (YouTube Music Desktop App) quando um vídeo toca no navegador
e retoma quando o vídeo pausa. Usa os controles de mídia do Windows.

No app: Settings > Integrations > ligar "Enable Windows 10 media service"
(e reiniciar o app).

Uso:
    python pausa_musica.py           -> roda o monitor
    python pausa_musica.py --listar  -> mostra os players que o Windows enxerga
"""
import asyncio
import sys

from winrt.windows.media.control import (
    GlobalSystemMediaTransportControlsSessionManager as Gerenciador,
    GlobalSystemMediaTransportControlsSessionPlaybackStatus as Status,
)

# ---------------- CONFIGURAÇÃO ----------------
# Sessões cujo ID contém um destes trechos contam como "vídeo" (navegador).
# Qualquer OUTRO player (o app de música, Spotify etc.) é tratado como música.
ID_NAVEGADOR = ["chrome", "msedge", "firefox", "brave", "opera", "vivaldi"]
INTERVALO = 0.5      # segundos entre verificações
RETOMAR_APOS = 0.5   # espera antes de retomar a música (evita "piscar" em anúncios)
# ----------------------------------------------


def eh_video(s):
    a = (s.source_app_user_model_id or "").lower()
    return any(t in a for t in ID_NAVEGADOR)


def tocando(s):
    try:
        return s.get_playback_info().playback_status == Status.PLAYING
    except Exception:
        return False


async def listar():
    g = await Gerenciador.request_async()
    sessoes = list(g.get_sessions())
    if not sessoes:
        print("Nenhum player encontrado.")
    for s in sessoes:
        titulo = ""
        try:
            info = await s.try_get_media_properties_async()
            titulo = f"{info.artist} - {info.title}"
        except Exception:
            pass
        tipo = "VÍDEO/NAVEGADOR" if eh_video(s) else "MÚSICA"
        print(f"[{tipo:15}] [{'tocando' if tocando(s) else 'parado':7}] "
              f"{s.source_app_user_model_id}  |  {titulo}")


async def monitorar():
    g = await Gerenciador.request_async()
    pausadas = set()        # IDs das músicas que ESTE script pausou
    sem_video_desde = None
    print("Monitorando... (Ctrl+C para sair)")

    while True:
        try:
            sessoes = list(g.get_sessions())
            video = any(tocando(s) for s in sessoes if eh_video(s))
            musicas = [s for s in sessoes if not eh_video(s)]
            agora = asyncio.get_running_loop().time()

            if video:
                sem_video_desde = None
                for m in musicas:
                    if tocando(m):
                        await m.try_pause_async()
                        pausadas.add(m.source_app_user_model_id)
                        print("Vídeo tocando -> música pausada")
            elif pausadas:
                if sem_video_desde is None:
                    sem_video_desde = agora
                elif agora - sem_video_desde >= RETOMAR_APOS:
                    for m in musicas:
                        if m.source_app_user_model_id in pausadas and not tocando(m):
                            await m.try_play_async()
                    pausadas.clear()
                    sem_video_desde = None
                    print("Vídeo parou -> música retomada")
        except Exception as e:
            print("Aviso:", e)
        await asyncio.sleep(INTERVALO)


if __name__ == "__main__":
    try:
        asyncio.run(listar() if "--listar" in sys.argv else monitorar())
    except KeyboardInterrupt:
        pass
