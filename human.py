from prompt import *
from brain import Memory

zodiac_character_map = {
    'capricorn': CAPRICORN_PROMPT,
    'scorpio': SCORPIO_PROMPT,
    'aries': ARIES_PROMPT,
    'taurus': TAURUS_PROMPT,
    'gemini': GEMINI_PROMPT,
    'cancer': CANCER_PROMPT,
    'leo': LEO_PROMPT,
    'virgo': VIRGO_PROMPT,
    'libra': LIBRA_PROMPT,
    'sagittarius': SAGITTARIUS_PROMPT,
    'aquarius': AQUARIUS_PROMPT,
    'pisces': PISCES_PROMPT,
}


class Human:
    def __init__(self, name=None, gender=None, relation=None, zodiac='leo', topic=None) -> None:
        self.name = name
        self.gender = gender
        self.zodiac = zodiac
        self.character = None
        self.topic = topic  
        self.relation = relation

    def update_character(self):
        self.character = zodiac_character_map.get(self.zodiac.lower()).format(self.gender)

    def retrieve_context(self, query, memory:Memory):
        print("\n",self.name, self.zodiac)
        print(f"Query received: {query}")
        memory.get_memory_info()
        contexts = memory._search_context(query, k=3)
        return contexts
        
    def give_response(self, query, memory:Memory, owner_name):
        print(">>>>>>> ",self.name, self.relation)

        contexts = self.retrieve_context(query, memory)
        response = memory.think(owner_name, 
                                self.character, 
                                content=query, 
                                context=contexts,
                                topic=self.topic,
                                relation=self.relation
                                )
        
        print(f"{owner_name}'s response: {response}")
        return response

    