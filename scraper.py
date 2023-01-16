import asyncio
import urllib.request
import os
import urllib.request
import aiohttp
from tiktokapipy.async_api import AsyncTikTokAPI
from tiktokapipy.models.video import Video

class tt_scraper():
    def __init__(self, user) -> None:
        self.usertag = user

    async def save_video(self, video: Video):
        async with aiohttp.ClientSession() as session:
            async with session.get(video.video.download_addr) as resp:
                str_resp = str(resp)[16:]
                str_resp = str_resp.split(")")[0]
                return str_resp
    
    async def scrape(self):
        async with AsyncTikTokAPI(emulate_mobile=False) as api:
            user_tag = self.usertag
            user = await api.user(user_tag)
            data = {}
            all_data = []
            async for video in user.videos:
                try:
                    if video.image_post:
                        continue
                    else:
                        num_comments = video.stats.comment_count
                        num_likes = video.stats.digg_count
                        num_views = video.stats.play_count
                        num_shares = video.stats.share_count
                        vid_id = video.id
                        data[str(vid_id)] = {
                            "video_id": str(vid_id),
                            "likes": num_likes,
                            "comments": num_comments,
                            "views": num_views,
                            "shares": num_shares,
                        }
                        all_data.append(data[str(vid_id)])
                        txt_alldata = str(all_data)

                        # write kpi data into a .txt
                        with open('kpi_tiktok.txt', 'w') as f:
                            f.write(txt_alldata)

                        # download video as .mp4
                        dwn_link = await self.save_video(video)
                        directory = './videos/'
                        if not os.path.exists(directory):
                            os.mkdir(directory)
                        file_name = directory+str(vid_id)+'.mp4'
                        print(file_name)
                        urllib.request.urlretrieve(dwn_link, file_name) 
                except:
                    continue


# Call the tiktok scraper
def main():
    CHANNEL_TAG = 'redbull'
    asyncio.run(tt_scraper(CHANNEL_TAG).scrape())

main()