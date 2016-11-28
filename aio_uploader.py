import argparse
import asyncio
import aioftp


async def upload(host, port, login, password):
    async with aioftp.ClientSession(host, port, login, password) as client:
        #await client.change_directory(path="tools.hde.nl/menc/site")
        #await client.make_directory("PowerView_programmer")
        #await client.stream.write("MKD Powerview®_programmer".encode('iso-8859-9'))
        await client.command("MKD Powerview®_programmer")
        #await client.make_directory("Powerview®_programmer")
        #await client.stream.write(b"MKD Powerview\xAE_programmer\n")
        #await client.upload_stream("c:/temp/pdf/guides/PowerView® programmer/PowerView® programmer.pdf")
        #await client.upload("/home/admin-s/pdf/guides/PowerView® programmer/PowerView® programmer.pdf")
        #print(await client.command(command='LIST'))



parser = argparse.ArgumentParser()
parser.add_argument("ftp_address")
# parser.add_argument("ftp_folder")
parser.add_argument("user")
parser.add_argument("passwd")
#parser.add_argument("pdf_source_folder")

if __name__ == "__main__":
    print("test\n".encode())
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    tasks = (upload(args.ftp_address, 21, args.user, args.passwd),)
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
