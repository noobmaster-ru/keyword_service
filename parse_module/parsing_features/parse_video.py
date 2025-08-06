import subprocess
import asyncio

from parse_module.parsing_features.tools import Tools


class ParseVideo:
    def __init__(self):
        pass

    async def parse_video(self, articles: dict):
        tasks = []
        for index, key in enumerate(articles):
            tasks.append(self._parse_video(articles[key]))
        await asyncio.gather(*tasks)

    async def _parse_video(self, article: dict):
        try:
            nm_id = int(article["nm_id"])
            basket, vol_value = Tools.build_basket_for_video(nm_id)
            m3u8_url = f"https://videonme-basket-{basket}.wbbasket.ru/vol{vol_value}/part{nm_id // 10000}/{nm_id}/hls/1440p/index.m3u8"
            try:
                # можно покопаться , чтобы большие видео обрабатывать нормально
                subprocess.run(
                    [
                        "ffmpeg",
                        "-i",
                        m3u8_url,
                        "-c",
                        "copy",
                        "-crf",
                        "30",
                        "-t",
                        "20",  # время обрезки
                        "-bsf:a",
                        "aac_adtstoasc",
                        f".data/video_{nm_id}.mp4",
                    ],
                    check=True,
                )
                article["link_to_video"] = m3u8_url
            except subprocess.CalledProcessError as e:
                print(f"Error during conversion: {e}")
                article["link_to_video"] = ""
        except Exception as e:
            print(f"❌ Error downloading photo for {article.get('nm_id')}: {e}")
