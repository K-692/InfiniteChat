import os
from helper import *
import streamlit as st
from human import Human
from pathlib import Path
from brain import Memory, Brain
from prompt import find_topic_prompt
from streamlit_extras.add_vertical_space import add_vertical_space
os.environ["TOKENIZERS_PARALLELISM"] = "false"


st.set_page_config(layout="wide",
                    page_icon="🤖",
                    page_title="Infinite Chat powered by AI"
                    )

st.markdown(
    "<h1 style='text-align: center; color: grey;'>Infinite Chat powered by AI</h1>", 
    unsafe_allow_html=True)
st.markdown(
    "<h4 style='text-align: center; color: grey;'>Perhaps their discourse will elucidate your queries!</h4>", 
    unsafe_allow_html=True)


if 'person1_name' not in st.session_state:
    st.session_state.person1_name = "Person1"

if 'person2_name' not in st.session_state:
    st.session_state.person2_name = "Person2"

if 'start_text' not in st.session_state:
    st.session_state.start_text = "Hi"

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'is_started' not in st.session_state:
    st.session_state.is_started = False

if 'person1_memory' not in st.session_state:
    st.session_state.person1_memory = Memory(st.session_state.person1_name)

if 'person2_memory' not in st.session_state:
    st.session_state.person2_memory = Memory(st.session_state.person2_name )

if 'person1' not in st.session_state:
    st.session_state.person1 = Human()

if 'person2' not in st.session_state:
    st.session_state.person2 = Human()

if "prev_reply" not in st.session_state:
    st.session_state.prev_reply = "Hi"

if "who_start" not in st.session_state:
    st.session_state.who_start = st.session_state.person1_name

if "topic" not in st.session_state:
    st.session_state.topic = ""


def display_message():
    for msg in st.session_state.chat_history:
        c1, _ = st.columns(2)
        with c1:
            with st.chat_message(emo_map.get(st.session_state.person1.gender)):
                st.write(st.session_state.person1_name)
                st.write(remove_outer_quotes(msg[st.session_state.person1_name]))
        _, c2 = st.columns(2)    
        with c2:
            with st.chat_message(emo_map.get(st.session_state.person2.gender)):
                st.write(st.session_state.person2_name)
                st.write(remove_outer_quotes(msg[st.session_state.person2_name]))

def add_chat():
    person1_response = st.session_state.person1.give_response(
            st.session_state.prev_reply,
            st.session_state.person1_memory,
            st.session_state.person1_name,
        )
    
    person2_response = st.session_state.person2.give_response(
            person1_response,
            st.session_state.person2_memory,
            st.session_state.person2_name,
        )
    
    conv = format_conversation(person1_response, person2_response)
    st.session_state.person1_memory.add_in_memory(conv, st.session_state.person1_name, st.session_state.person2_name)
    st.session_state.person2_memory.add_in_memory(conv, st.session_state.person1_name, st.session_state.person2_name)
    st.session_state.prev_reply = person2_response
    
    st.session_state.chat_history.append(
        {
            st.session_state.person1_name: person1_response,
            st.session_state.person2_name: person2_response
        }
    )

def format_conversation(person1_text, person2_text):
    return f"{st.session_state.person1_name} said: {person1_text} \n {st.session_state.person2_name} said: {person2_text}"

def find_topic(conversation):
    response = Brain().think(content=find_topic_prompt.format(st.session_state.person1_name, 
                                                              st.session_state.person2_name, 
                                                              conversation),
                            task="find_topic")
    
    st.session_state.person1.topic = response
    st.session_state.person2.topic = response


def initial_process():
    print("##### Initial ######")

    if st.session_state.who_start == st.session_state.person1_name:
        person1_memory = st.session_state.person1_memory._create_or_get_memory()
        st.session_state.person1_memory._add_event(person1_memory, st.session_state.start_text)
        person2_memory = st.session_state.person2_memory._create_or_get_memory()
        st.session_state.person2_memory._add_event(person2_memory, "Conversation starts.")
        
        response = st.session_state.person2.give_response(
        st.session_state.start_text,
        st.session_state.person2_memory,
        st.session_state.person2_name
        )

        conv = format_conversation(st.session_state.start_text, response)
        st.session_state.person1_memory.add_in_memory(conv, st.session_state.person1_name, st.session_state.person2_name)
        st.session_state.person2_memory.add_in_memory(conv, st.session_state.person1_name, st.session_state.person2_name)
        st.session_state.chat_history.append(
            {
                st.session_state.person1_name: st.session_state.start_text,
                st.session_state.person2_name: response
            }
        )
        st.session_state.prev_reply = response

    else:
        person1_memory = st.session_state.person1_memory._create_or_get_memory()
        st.session_state.person1_memory._add_event(person1_memory, st.session_state.prev_reply)
        person2_memory = st.session_state.person2_memory._create_or_get_memory()
        st.session_state.person2_memory._add_event(person2_memory, st.session_state.start_text)

        st.session_state.chat_history.append(
            {
                st.session_state.person1_name: st.session_state.prev_reply,
                st.session_state.person2_name: st.session_state.start_text
            }
        )
        conv = format_conversation(st.session_state.prev_reply, st.session_state.start_text)
        st.session_state.prev_reply = st.session_state.start_text

    find_topic(conv)


def session_start():
    c1, c2 = st.columns(2)
    with c1:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.session_state.person1_name = st.text_input(label="Person 1", value=st.session_state.person1_name)
            st.session_state.person2_name = st.text_input(label="Person 2", value=st.session_state.person2_name)
            st.session_state.person1.name = st.session_state.person1_name 
            st.session_state.person2.name = st.session_state.person2_name 

        with col2:
            st.session_state.person1.gender = st.selectbox(f"{st.session_state.person1_name}'s gender: ",
                                  ("Male", "Female"))
            st.session_state.person2.gender = st.selectbox(f"{st.session_state.person2_name}'s gender: ",
                                                        index=1,
                                                        options=("Male", "Female"))
    
        with col3:
            st.session_state.person1.zodiac = st.selectbox(f"{st.session_state.person1_name}'s zodiac: ",
                                                        options=zodiac_signs,
                                                        index=9
                                                        )
            st.session_state.person2.zodiac = st.selectbox(f"{st.session_state.person2_name}'s zodiac: ",
                                                        index=7,
                                                        options=zodiac_signs)
       
        st.session_state.person1.update_character()
        st.session_state.person2.update_character()


        with col4:
            add_vertical_space(3)
            st.session_state.who_start = st.radio(
            "Who will start chat👇🏻",
            key="who",
            options=[st.session_state.person1_name, st.session_state.person2_name],
            )


    with c2:
        st.session_state.start_text  = st.text_input(f"What {st.session_state.who_start} will ask?", 
                                                     value=st.session_state.start_text)
    
        relation  = st.selectbox(f"How is {st.session_state.person1_name} related to {st.session_state.person2_name}?", 
                                                     options=relationships.get(st.session_state.person1.gender),
                                                     index=8,
                                                     )

        st.session_state.person1.relation = relation
        st.session_state.person2.relation = get_relationship_mapping(relation, st.session_state.person2.gender)


    if st.button("Start", key="start", use_container_width=True) and not st.session_state.is_started:
        st.session_state.is_started = True
        initial_process()

    

def main():
    if not st.session_state.is_started:
        session_start()

    if st.session_state.is_started and st.button("Clear Memory", key="clear"):
        st.session_state.person1_memory.erase_memory()
        st.session_state.person2_memory.erase_memory()
        st.session_state.chat_history=[]
        print("####### CLEARED #######")
        st.session_state.prev_reply = "Hi"
        st.session_state.topic = ""
        session_start()
        st.session_state.is_started = False
        st.rerun()


    display_message()
    print("\n\n\n")
    if st.session_state.is_started: 
        st.button("Continue", on_click=add_chat, use_container_width=True)

if __name__ == "__main__":
    main()

