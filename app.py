import uvicorn


if __name__ == "__main__":

    # Start the server
    config = uvicorn.Config(app="src.main:app")
    server = uvicorn.Server(config)
    server.run()
