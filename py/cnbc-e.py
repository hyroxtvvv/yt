import requests
import re

# Temel URL'ler ve hedef URL'ler
base_url_eurostar = "http://mn-nl.mncdn.com/dogusdyg_eurostar/dogusdyg_eurostar.smil/"

url_eurostar = "https://www.eurostartv.com.tr/canli-izle"
url_cnbce = "https://www.cnbce.com/canli-yayin"

# Belirtilen web sitesinden m3u8 bağlantıları çıkarmak için fonksiyon
def get_m3u8_links(url, base_url):
    response = requests.get(url)

    if response.status_code == 200:
        site_content = response.text

        # Canlı yayın URL'sini web sitesinin yapısına göre bul
        if "eurostartv" in url:
            match = re.search(r'liveUrl = \'(.*?)\'', site_content)
        elif "cnbce" in url:
            match = re.search(r'data-stream="(.*?)"', site_content)

        if match:
            live_url = match.group(1)
            #print(f"Konum: {live_url}")

            # CNBC-E için, live_url doğrudan video URL'sidir, bu nedenle sadece onu döndür
            if "cnbce" in url:
                return live_url

            content_response = requests.get(live_url)

            if content_response.status_code == 200:
                content = content_response.text
                lines = content.split("\n")
                modified_content = ""

                for line in lines:
                    if line.startswith("chunklist"):
                        full_url = base_url + line
                        modified_content += full_url + "\n"
                    else:
                        modified_content += line + "\n"

                return modified_content
            else:
                print("İçerik alınamadı.")
        else:
            print("Canlı yayın URL'si içerikte bulunamadı.")
    else:
        print("Web sitesi içeriği alınamadı.")

# Her bir web sitesi için m3u8 bağlantıları al ve ayrı dosyalara yaz
eurostar_m3u8 = get_m3u8_links(url_eurostar, base_url_eurostar)
cnbce_m3u8 = get_m3u8_links(url_cnbce, base_url_eurostar)  # CNBC-E için temel URL gerekmiyor

with open("ch/eurostar.m3u8", "w") as f:
    f.write(eurostar_m3u8)

with open("ch/cnbce.m3u8", "w") as f:
    f.write(cnbce_m3u8)
