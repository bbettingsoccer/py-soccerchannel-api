# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import uvicorn

if __name__ == '__main__':
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000, reload=True)


