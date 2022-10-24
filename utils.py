from virustotal_python import Virustotal
import os.path
import os
import discord
import requests 
import uuid

API_KEY = os.environ.get('VT_API_KEY')

def vt_file(file_path):
    files = {"file": (os.path.basename(file_path),
                    open(os.path.abspath(file_path), "rb"))}
    vtotal = Virustotal(API_KEY=API_KEY, API_VERSION=2)
    resp = vtotal.request("file/scan", files=files, method="POST")
    resp = resp.json()

    permalink = resp['permalink']
    resource = resp['resource']
    scan_id = resp['scan_id']
    sha1 = resp['sha1']
    sha256 = resp['sha256']
    verbose_msg = resp['verbose_msg']

    return format_resp_data(file_path, permalink, resource, scan_id, sha1, sha256, verbose_msg)


def format_resp_data(file_path, permalink, resource, scan_id, sha1, sha256):
    sc_url= f"https://api.screenshotmachine.com?key=fdb8bf&url={permalink}&dimension=1024x768"
    img_data = requests.get(sc_url).content
    f_name = f"{str(uuid.uuid4()).upper()}.jpeg"
    

    with open(f_name, 'wb') as handler:
        handler.write(img_data)

    file = discord.File(f_name, filename=f_name)
    
    embed=discord.Embed(title=file_path, url=permalink, description="File submited for scan, click the link in the file name to open the report.", color=0x333aff)
    embed.set_thumbnail(url="https://cdn.icon-icons.com/icons2/2699/PNG/512/virustotal_logo_icon_171247.png")
    embed.set_image(url=f"attachment://{f_name}")
    embed.add_field(name="Resource:", value=resource, inline=False)
    embed.add_field(name="Scan ID:", value=scan_id, inline=False)
    embed.add_field(name="SHA1:", value=sha1, inline=False)
    embed.add_field(name="SHA256:", value=sha256, inline=False)
    embed.set_footer(text="Results provided by VirusTotal")

    return embed, file, f_name