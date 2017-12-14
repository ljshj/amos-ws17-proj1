from __future__ import unicode_literals


nlu_model_path = 'models/nlu/default/current'
dialogue_path = '/models/dialogue'

topic_switching_intent_prefix = 'inform'

current_dialogue = None


def load_interpreter():
    from rasa_nlu.config import RasaNLUConfig
    from rasa_nlu.model import Metadata, Interpreter

    # where `model_directory points to the folder the model is persisted in
    interpreter = Interpreter.load(nlu_model_path, RasaNLUConfig('nlu_model_config.json'))

    return interpreter


def load_agents(topics):
    from rasa_core.agent import Agent

    agents = {}

    for topic in topics:
        agent = Agent.load(topic + dialogue_path)
        agents[topic] = agent

    return agents


def run(interpreter, agents):
    # parse user input
    nlu_jsonResponse = interpreter.parse('What will the weather be in Berlin?')

    entities = []

    if len(nlu_jsonResponse['entities']) > 0:

        for e in nlu_jsonResponse['entities']:
            entity = e['entity'] + '=' + e['value']
            entities.append(entity)

    global current_dialogue

    for topic in agents:
        if topic_switching_intent_prefix == nlu_jsonResponse['intent']['name']:
            current_dialogue = topic

    # handle user input
    print agents[current_dialogue].handle_message('_' + nlu_jsonResponse['intent']['name'] + '[' + ','.join(map(str, entities)) + ']')

if __name__ == '__main__':
    interpreter = load_interpreter()
    topics = ['weather']
    agents = load_agents(topics)

    run(interpreter,agents)