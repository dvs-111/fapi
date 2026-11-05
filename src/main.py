import uvicorn
import asyncio

"""
async def main() -> None:
# def main():
	await uvicorn.run(
		'router:router',
		host='localhost',
		port=8000,
		reload=True,
		# factory=True,
	)
# """

async def main() -> None:
	conf = uvicorn.Config(
		'router:router',
		host='localhost',
		port=8000,
		reload=True,
		# factory=True,
	)
	srv = uvicorn.Server(config=conf)
	await srv.serve()

if __name__ == '__main__':
	asyncio.run(main())
	# main()