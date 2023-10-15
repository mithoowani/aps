import streamlit as st

CLINICAL_CRITERIA = ['Macrovascular: Venous thromboembolism',
                     'Macrovascular: Arterial thromboembolism',
                     'Microvascular',
                     'Obstetric criteria',
                     'Cardiac valve',
                     'Hematology']

LAB_CRITERIA = ['Lupus anticoagulant',
                'Anti-cardiolipin (IgG or IgM) at moderate-high titre',
                'Anti-b2-glycoprotein I (IgG or IgM) at moderate-high titre']


def initialize_app():
    # Initialize page to start at 0
    st.session_state.setdefault('page', 0)

    # Initialize cache to save initial state of all widgets
    # As the program runs, session_state.cache will update with the current state of all widgets
    # in order to save their state
    if 'cache' not in st.session_state:
        st.session_state.cache = dict()
    for i in range(len(CLINICAL_CRITERIA)):
        st.session_state.cache.setdefault(f'clinical_{i}', False)
    for i in range(len(LAB_CRITERIA)):
        st.session_state.cache.setdefault(f'lab_{i}', False)


def meets_entry_criteria():
    """Checks whether entry criteria are met to enter the algorithm, i.e. whether at least one clinical criterion
    and at least one laboratory criterion are checked off by the user"""
    meets_clinical_criteria = any(st.session_state.cache[f'clinical_{i}'] for i in range(len(CLINICAL_CRITERIA)))
    meets_lab_criteria = any(st.session_state.cache[f'lab_{i}'] for i in range(len(LAB_CRITERIA)))
    if meets_clinical_criteria and meets_lab_criteria:
        return True
    else:
        return False


def update_cache(key):
    """Updates session_sate.cache to reflect the current state of each widget; this ensures
    that the state gets preserved when switching between pages in the app"""
    st.session_state.cache[key] = st.session_state[key]


initialize_app()

if st.session_state['page'] == 0:  # Entry criteria page
    st.write("# Step 1: Entry criteria")
    col1, col2 = st.columns(2)
    with col1:
        st.write('#### At least one clinical criterion')
        for i, criterion in enumerate(CLINICAL_CRITERIA):
            obj_key = f'clinical_{i}'
            st.checkbox(criterion,
                        value=st.session_state.cache[obj_key],
                        key=obj_key,
                        on_change=update_cache,
                        kwargs={'key': obj_key})

    with col2:
        st.write('#### Positive antiphospholipid test within three years of the clinical criterion')
        for i, criterion in enumerate(LAB_CRITERIA):
            obj_key = f'lab_{i}'
            st.checkbox(criterion,
                        value=st.session_state.cache[obj_key],
                        key=obj_key,
                        on_change=update_cache,
                        kwargs={'key': obj_key})

    # Can only proceed if patient meets at least one clinical and one lab criterion
    submit_entry_criteria = st.button('Apply additive criteria', disabled=not meets_entry_criteria())

    # Refresh to show the next page
    if submit_entry_criteria:
        st.session_state['page'] += 1
        st.rerun()

elif st.session_state['page'] == 1:
    st.write("# Additive clinical criteria #")
    st.write('### D1. Macrovascular (Venous thromboembolism) ####')
    major_risk_factors, minor_risk_factors = st.tabs(['__Major risk factors__', '__Minor risk factors__'])
    with major_risk_factors:
        st.markdown("""
        1.  **Active malignancy** with no or noncurative treatment received, ongoing curative treatment including hormonal therapy, or recurrence progression despite curative treatment at the time of the event
        2.  **Hospital admission** confined to bed (only bathroom privileges) with an acute illness for at least 3 days within 3 months prior to the event. Major trauma with fractures or spinal cord injury within 1 month prior to the event
        3.  **Surgery** with general/spinal/epidural anesthesia for >30 minutes within 3 months prior to the event
        """)
    with minor_risk_factors:
        st.markdown("""
        1.  **Active systemic autoimmune disease or active inflammatory bowel disease** using disease activity measures guided by current recommendations.
        2.  **Acute/active severe infection** according to guidelines, e.g., sepsis, pneumonia, SARS-CoV-2
        3.  **Central venous catheter** in the same vascular bed
        4.  **Hormone replacement therapy, estrogen containing oral contraceptives, or ongoing in vitro fertilization treatment**
        5.  **Long distance travel** (≥8 hours)
        6.  **Obesity** (body mass index [BMI] ≥30 kg/m2)
        7.  **Pregnancy or postpartum period** within 6 weeks after delivery
        8.  **Prolonged immobilization** not counted above, e.g., leg injury associated with reduced mobility, or confined to bed out of hospital for at least 3 days.
        9.  **Surgery** with general/spinal/epidural anesthesia for <30 minutes within 3 months prior to the event
        """)

    st.markdown('#')

    col1, col2 = st.columns(2)
    with col1:
        vte_high_risk_profile = st.checkbox('VTE with a high risk profile (1 point)', key='vte_high_risk')
        st.markdown('One or more _major_ risk factors or two or more _minor_ risk factors at the time of the event')

    with col2:
        vte_low_risk_profile = st.checkbox('VTE without a high risk profile (3 points)', key='vte_low_risk')

    col1, inter_cols_space, col2 = st.columns([1, 8, 1])
    with col1:
        back_button = st.button('Back')

    with col2:
        next_button = st.button('Next')

    # Move to next page and refresh
    if next_button:
        st.session_state['page'] += 1
        st.rerun()

    # Move to previous page and refresh
    if back_button:
        st.session_state['page'] -= 1
        st.rerun()
