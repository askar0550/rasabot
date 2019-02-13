# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

"""
This sample shows how to create a simple EchoBot with state.
"""


from aiohttp import web
from botbuilder.schema import (Activity, ActivityTypes)
from botbuilder.core import (BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext,
                             ConversationState, MemoryStorage, UserState)

from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.utils import EndpointConfig

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# RASA loader
interpreter = RasaNLUInterpreter('models/current/nlu')
print('the interpreter has been loaded')

agent = Agent.load('models/dialogue', interpreter=interpreter, action_endpoint=EndpointConfig(url="http://127.0.0.1:5055/webhook"))
print('agent has been loaded')




APP_ID = ''
APP_PASSWORD = ''
PORT = 9000
HOST = 'localhost'
SETTINGS = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
ADAPTER = BotFrameworkAdapter(SETTINGS)

# Create MemoryStorage, UserState and ConversationState
MEMORY = MemoryStorage()
# Commented out user_state because it's not being used.
# user_state = UserState(memory)
CONVERSATION_STATE = ConversationState(MEMORY)

# Register both State middleware on the adapter.
# Commented out user_state because it's not being used.
# ADAPTER.use(user_state)
ADAPTER.use(CONVERSATION_STATE)


async def create_reply_activity(request_activity, text) -> Activity:
    '''create reply'''
    return Activity(
        type=ActivityTypes.message,
        channel_id=request_activity.channel_id,
        conversation=request_activity.conversation,
        recipient=request_activity.from_property,
        from_property=request_activity.recipient,
        text=text,
        service_url=request_activity.service_url)


async def handle_message(context: TurnContext) -> web.Response:
    '''handle message'''
    # Access the state for the conversation between the user and the bot.
    state = await CONVERSATION_STATE.get(context)

    # if hasattr(state, 'counter'):
    #     state.counter += 1
    # else:
    #     state.counter = 1
    # mssg = f'{state.counter}: You said {context.activity.text}.'
    mssg = agent.handle_message(context.activity.text)
    try:
        response = await create_reply_activity(context.activity, mssg[0]['text'])
    except IndexError:
        response = await create_reply_activity(context.activity, 'denied')
        print(mssg)
    await context.send_activity(response)
    return web.Response(status=202)


async def handle_conversation_update(context: TurnContext) -> web.Response:
    '''conversation update'''
    if context.activity.members_added[0].id != context.activity.recipient.id:
        response = await create_reply_activity(context.activity, 'Welcome to the Echo Adapter Bot!')
        await context.send_activity(response)
    return web.Response(status=200)


async def unhandled_activity() -> web.Response:
    '''not found'''
    return web.Response(status=404)


async def request_handler(context: TurnContext) -> web.Response:
    '''request handler'''
    if context.activity.type == 'message':
        return await handle_message(context)
    if context.activity.type == 'conversationUpdate':
        return await handle_conversation_update(context)
    return await unhandled_activity()


async def messages(req: web.Request) -> web.Response:
    '''messages'''
    body = await req.json()
    activity = Activity().deserialize(body)
    auth_header = req.headers['Authorization'] if 'Authorization' in req.headers else ''
    try:
        return await ADAPTER.process_activity(activity, auth_header, request_handler)
    except Exception as e_x:
        raise e_x


APP = web.Application()
APP.router.add_post('/', messages)

try:
    print('stuff')
    web.run_app(APP, host=HOST, port=PORT)
except Exception as e_x:
    raise e_x
