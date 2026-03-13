import uvicorn
import asyncio


# async def main() -> None:
def main():
	uvicorn.run(
		'router:app',
		host='localhost',
		port=8000,
		reload=True,
		# factory=True,
	)

if __name__ == '__main__':
	# asyncio.run(main())
	main()