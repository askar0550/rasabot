
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.utils import EndpointConfig

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


interpreter = RasaNLUInterpreter('models/current/nlu')
print('the interpreter has been loaded')
agent = Agent.load('models/dialogue', interpreter=interpreter, action_endpoint=EndpointConfig(url="http://127.0.0.1:5055/webhook"))
print('agent has been loaded')

mssg = agent.handle_message("tell me a joke")
print(mssg, 'mssg')
print(agent, 'Agent')
print(interpreter, 'interpreter')

#
# for ind, elm in enumerate(agent):
#     print(agent[ind], elm, ind)
#
# for ind, elm in enumerate(interpreter):
#     print(interpreter[ind], elm, ind)
