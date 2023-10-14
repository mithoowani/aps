import streamlit as st


def initialize():
    st.session_state.setdefault('page', 0)
    st.session_state.setdefault('ch1', False)
    st.session_state.setdefault('ch2', False)


def next_page():
    if st.session_state.page == 0:
        st.session_state.page += 1
    else:
        st.session_state.page = 0


initialize()

st.write("""# Hello""")
st.write('This is my *first* Streamlit app')
st.write('This is some additional writing')

st.button('Switch page', on_click=next_page)

if st.session_state.page == 0:
    col1, col2, col3 = st.columns([2, 2, 1])

    with st.form(key='user_input'):
        with col1:
            diagnoses = ['PE', 'DVT', 'PE and DVT']
            diagnosis = st.radio('What is the diagnosis?', options=diagnoses)

            ch1 = st.checkbox('Check 1', value=st.session_state['ch1'])
            st.session_state['ch1'] = ch1

            ch2 = st.checkbox('Check 2', value=st.session_state['ch2'])
            st.session_state['ch2'] = ch2

            st.write(sum([ch1, ch2]))

        with col2:
            severity_options = ['Mild', 'Moderate', 'Severe']
            severity = st.radio('How severe?', options=severity_options)

            st.multiselect('Stuff', ['a', 'b', 'c'])

        with col3:
            setting_options = ['Inpatient', 'Outpatient', 'ED', 'Home']
            setting = st.radio('Patient care setting', setting_options)

            st.selectbox('Select', [1, 2, 3])

        submitted = st.form_submit_button('Submit')

        if submitted:
            st.write('You entered', diagnosis)
            st.write('You entered', severity)
            st.write('You entered', setting)

else:
    st.write('This is the next page')
    st.checkbox('This is another checkbox')
    st.checkbox('This is yet another checkbox')

st.write('Bottom of form')
