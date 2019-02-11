from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter

# RASA loader
interpreter = RasaNLUInterpreter('models/current/nlu')
print('the interpreter has been loaded')

agent = Agent.load('models/dialogue', interpreter=interpreter)
print('the agent is ready')

mssg = agent.handle_message('tell me a joke')



print(mssg)
