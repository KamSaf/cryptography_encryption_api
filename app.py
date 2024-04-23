import uvicorn

if __name__ == "__main__":
    # Start the server
    uvicorn.run("src.main:app", reload=True)
