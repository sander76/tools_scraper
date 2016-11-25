import argparse
import asyncio
import aioftp

async def upload(host,port,login,password):
    async with aioftp.ClientSession(host,port,login,password) as client:
        await client.change_directory(path="tools.hde.nl/menc/site")
        await client.upload("home/admin-s/pdf/guides/PowerView® programmer/PowerView® programmer.pdf")


parser = argparse.ArgumentParser()
parser.add_argument("ftp_address")
#parser.add_argument("ftp_folder")
parser.add_argument("user")
parser.add_argument("passwd")
#parser.add_argument("pdf_source_folder")

if __name__=="__main__":
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    tasks = (upload(args.ftp_address,21,args.user,args.passwd),)
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

