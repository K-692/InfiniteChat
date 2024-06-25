from chromadb.utils import embedding_functions
import chromadb
from prompt import *
import os
from groq import Groq
from dotenv import load_dotenv

class Brain:
    def __init__(self):
        load_dotenv()
        self.client = Groq(api_key=os.environ.get("GROQ_KEY"))

    def think(self, 
              owner_name=None,
              zodiac_character=None,
              context=None,
              content="", 
              topic=None,
              relation=None,
              model_name="llama3-8b-8192", 
              task="general" 
              ):
        try:
            chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": regulation_prompt.format(owner_name, 
                                                        zodiac_character, 
                                                        relation,
                                                        topic, 
                                                        content, 
                                                        context) if task=="general" else content,
                }
            ],
            model=model_name,
            )

            print(f"LLM response {task}: {chat_completion.choices[0].message.content}\n")
            return chat_completion.choices[0].message.content        
        
        except Exception as e:
            print(f"Getting error as {e}")
            return "Not able to connect with my brain."

class Memory(Brain):
    def __init__(self, owner_name:str) -> None:
        super().__init__()
        self.embeddings = embedding_functions.DefaultEmbeddingFunction()
        self.db_name = "memory/"
        self.information = owner_name

    def _create_or_get_memory(self):
        memory = chromadb.PersistentClient(self.db_name)
        return memory

    def _add_event(self, memory, conversation):
        all_info = memory.get_or_create_collection(name=self.information, embedding_function=self.embeddings)
        last_entry =  all_info.count()
        all_info.add(
            documents=conversation,
            ids=[f"id{last_entry+1}"],
            metadatas = [{"source": "Conversation"}]
        )

    def add_in_memory(self, conversation, man_name, woman_name):
        memory = self._create_or_get_memory()
        self._add_event(memory, 
                        self.think(content=store_memory_prompt.format(man_name, 
                                                              woman_name, 
                                                              conversation), 
                                   task="summarization"))


    def _search_context(self, query, k=3):
        memory = self._create_or_get_memory()
        all_info = memory.get_or_create_collection(name=self.information, embedding_function=self.embeddings)
        results = all_info.query(
        query_texts=[query],
        n_results=k
        )
        context_string = ""
        for result in results.get("documents")[0]:
            context_string += f"{result}\n\n" 

        print("-------------------------------------------")
        print("Contexts: \n", context_string)
        print("-------------------------------------------")
        return context_string


    def get_memory_info(self):
        memory = self._create_or_get_memory()
        print("Memory path:", self.db_name)
        print("Collections available:", memory.list_collections())
        print("Total number of informatic events stored: ", memory.get_or_create_collection(name=self.information).count())


    def erase_memory(self):
        memory = self._create_or_get_memory()
        memory.delete_collection(name=self.information)
        self.get_memory_info()