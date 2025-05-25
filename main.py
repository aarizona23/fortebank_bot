from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fortebot.model import ServiceSearch
app = FastAPI()
templates = Jinja2Templates(directory="templates")

chat_history = []

@app.get("/", response_class=HTMLResponse)
def get_chat(request: Request):
    """
    Renders the main chat page with the chat history.
    :param request:
    :return: HTMLResponse with the chat history
    """

    return templates.TemplateResponse("index.html", {
        "request": request,
        "chat_history": chat_history
    })

@app.post("/", response_class=HTMLResponse)
def post_chat(request: Request, user_message: str = Form(...)):
    """
    Handles the user's message, processes it with the ServiceSearch model,
    and updates the chat history.
    :param request:
    :param user_message:
    :return: HTMLResponse with the updated chat history
    """

    chat_history.append({"sender": "user", "message": user_message})

    searcher = ServiceSearch(user_message)
    bot_response = searcher.search()
    chat_history.append({"sender": "bot", "message": bot_response["text"], "url": bot_response["url"]})

    return templates.TemplateResponse("index.html", {
        "request": request,
        "chat_history": chat_history
    })
