#fins de teste 
import asyncio
from serviceEye import ServiceEye

async def main():
    SE = ServiceEye()
    SE.add_url("youtbe.com")
    await SE.runner()

if __name__ == "__main__":
    asyncio.run(main())



