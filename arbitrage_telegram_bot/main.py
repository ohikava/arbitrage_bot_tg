import os
from typing import Any, Type 
from dotenv import load_dotenv 
from http import HTTPStatus

from telegram.ext import Application, CommandHandler, CallbackContext, ExtBot, ContextTypes, TypeHandler
from contextlib import asynccontextmanager
from telegram import Update
from telegram.constants import ParseMode 
import logging 
from dataclasses import dataclass
from fastapi import FastAPI, Response, Request
from utils import format_opportunity

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
USER_ID = os.getenv("CHAT_ID")
PORT = os.getenv("PORT")
URL = os.getenv("URL")

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

@dataclass 
class Opportunity:
    """Simple dataclass to wrap a custom update type"""
    cex_bid: str
    cex_ask: str
    bid_price: str 
    ask_price: str 
    spread: str 
    symbol: str 
    liquidity: str 

class CustomContext(CallbackContext[ExtBot, dict, dict, dict]):
    """
    Custom CallbackContext class that makes `user_data` available for updates of type
    `WebhookUpdate`.
    """
    @classmethod
    def from_update(cls, update: object, application: "Application") -> "CustomContext":
        if isinstance(update, Opportunity):
            return cls(application=application, user_id=USER_ID)
        return super().from_update(update, application)
    
async def start(update: Update, context: CustomContext) -> None:
    await context.bot.send_message(text="Hello", chat_id=USER_ID)

async def webhook_update(update: Opportunity, context: CustomContext) -> None:
    msg = format_opportunity(update)
    await context.bot.send_message(text= msg, chat_id=USER_ID, parse_mode=ParseMode.HTML)

context_types = ContextTypes(context=CustomContext)

ptb = (
    Application.builder()
    .token(BOT_TOKEN)
    .updater(None)
    .context_types(context_types)
    .build()
)

ptb.add_handler(CommandHandler("start", start))
ptb.add_handler(TypeHandler(type=Opportunity, callback=webhook_update))

models = {}

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    print('Init lifespan')
    await ptb.bot.set_webhook(f"{URL}/telegram")
    async with ptb:
        await ptb.start()
        yield
        print('close lifespan')
        await ptb.stop()

app = FastAPI(lifespan=app_lifespan)

@app.post("/telegram")
async def telegram(request: Request) -> Response:
    body = await request.json()
    await ptb.update_queue.put(Update.de_json(data=body, bot = ptb.bot))
    return Response(status_code=HTTPStatus.OK)

@app.get("/healthchek")
async def healthchek(request: Request) -> Response:
    return Response(content='bot is working!', status_code=HTTPStatus.OK)


@app.post("/opportunity")
async def opportunity(request: Request) -> Response:
    try:
        body = await request.json()
        cex_bid = body['cex_bid']
        cex_ask = body['cex_ask']
        bid_price = body['bid_price']
        ask_price = body['ask_price']
        spread = body['spread']
        symbol = body['symbol']
        liquidity = body['liquidity']
    except KeyError:
        return Response(status_code=HTTPStatus.BAD_REQUEST, content="Please pass all required parameters")
    
    await ptb.update_queue.put(Opportunity(**body))
    return Response(status_code=HTTPStatus.OK)

    

        