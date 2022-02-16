import deepl
import streamlit as st

if 'access' not in st.session_state:
    st.session_state.access = False
    
if not(st.session_state.access):
    password = st.text_input('Please enter password')
    if password == st.secrets["accesskey"]:
        st.session_state.access = True
        st.experimental_rerun()

if st.session_state.access:
    translator = deepl.Translator(st.secrets["apikey"])
    languages = {'English (US)':'EN-US', 'Spanish':'ES', "Portuguese (Portugal)":'PT-PT'}
    selectedLang = st.selectbox('Select your native language',languages)
    langCode = languages[selectedLang]
    
    text = st.text_area("Enter your text", height=200)
    submit = st.button("Submit")
    
    if submit and text != "":
        st.info("Note: these corrections may mix articles (i.e. replace ihn/sie with es).")
        for sentence in text.split(". "):
            
            #recover original meaning intended by user (hopefully)
            to_src = translator.translate_text(sentence, target_lang=langCode).text
            
            #translate to gramatically correct German
            to_german = translator.translate_text(to_src, target_lang="DE").text
            
            st.markdown(f'>>{sentence}\n')
            if to_german == to_src:
                st.markdown('This means: ')
                st.markdown(f'>>{to_src}\n')
                st.markdown("This sentence could not be corrected.")
                st.markdown('---')
            if to_german != sentence and to_german != to_src:
                st.markdown('This should (probably) be: ')
                st.markdown(f'>>{to_german}\n')
                st.markdown('Which means: ')
                st.markdown(f'>>{to_src}\n')
                st.markdown('---')
            if to_german == sentence:
                st.markdown('This sentence was perfect!\n')
                st.markdown('---')