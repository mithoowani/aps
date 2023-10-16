"""
Web app for applying revised EULAR 2023 antiphospholipid syndrome (APS) classification criteria
Full text: Arthritis Rheumatol . 2023 Oct;75(10):1687-1702.  doi: 10.1002/art.42624.  Epub 2023 Aug 28
"""

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

MICROVASCULAR_SUSPECTED_CRITERIA = {
    'Livedo racemosa (exam)': 'livedo_racemosa',
    'Livedoid vasculopathy lesions (exam)': 'livedo_vasculopathy_exam',
    'Acute/chronic aPL-nephropathy (exam or lab)': 'apl_nephropathy_exam',
    'Pulmonary hemorrhage (symptoms and imaging)': 'pulm_hemorrhage_symptoms'
}

MICROVASCULAR_ESTABLISHED_CRITERIA = {
    'Livedoid vasculopathy (pathology)': 'livedo_vasculopathy_path',
    'Acute/chronic aPL-nephropathy (pathology)': 'apl_nephropathy_path',
    'Pulmonary hemorrhage (BAL or pathology)': 'pulm_hemorrhage_path',
    'Myocardial disease (imaging or pathology)': 'myocardial_path',
    'Adrenal hemorrhage (imaging or pathology)': 'adrenal_hemorrhage_path'
}

OBSTETRIC_CRITERIA = {
    '3 or more consecutive pre-fetal (<10w) and/or early fetal (10w -15w 6d) deaths (**1 point**)':
        '3_consecutive_losses',

    'Fetal death (16w – 33w 6d) in the absence of 1 pre-eclampsia (PEC) with severe features or placental '
    'insufficiency with severe features (**1 point**)': '16_week_fetal_death',

    'Pre-eclampsia with severe features (<34w) _OR_ placental insufficiency with 3 severe features (<34w with/without '
    'fetal death (**3 points**)': 'pre_eclampsia_or_pi',

    'Pre-eclampsia with severe features (<34w) _AND_ placental insufficiency with 3 severe features (<34w '
    'with/without fetal death (**4 points**)': 'pre_eclampsia_and_pi'
}

CARDIAC_CRITERIA = {
    'Thickening (**2 points**)': 'valve_thickening',
    'Vegetation (**4 points**)': 'valve_vegetation'
}

LAC_CRITERIA = {
    'Positive LAC (single – one time) (**1 point**)': 'single_lac',
    'Positive LAC (persistent) (**5 points**)': 'persistent_lac'
}

APL_CRITERIA = {
    'Moderate or high positive IgM (aCL and/or aβ2GPI) (**1 point**)': 'mod_high_igm',
    'Moderate positive IgG (aCL and/or aβ2GPI) (**4 points**)': 'mod_pos_igg',
    'High positive IgG (aCL _OR_ aβ2GPI) (**5 points**)': 'high_pos_igg_or',
    'High positive IgG (aCL _AND_ aβ2GPI) (**7 points**)': 'high_pos_igg_and',
}


def initialize_app():
    # Initialize page to start at 0
    st.session_state.setdefault('page', 0)

    # Initialize cache to save initial state of all widgets
    # As the program runs, session_state.cache will update with the saved state of all widgets
    st.session_state.setdefault('cache', dict())


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


def persistent_checkbox(text, key):
    st.session_state.cache.setdefault(key, False)
    return st.checkbox(text,
                       value=st.session_state.cache[key],
                       key=key,
                       on_change=update_cache,
                       kwargs={'key': key})


def show_next_and_back_buttons(last_page=False, score_page=False):
    """
    Shows buttons at bottom of page:
    If last_page = True (scoring criteria D8), 'Next' button captioned as 'Calculate score' instead
    If score_page = True, no 'Next' button is displayed
    Note that last_page and score_page should never be BOTH true
    """
    if last_page:
        col1, inter_cols_space, col2 = st.columns([1, 3, 1])
    else:
        col1, inter_cols_space, col2 = st.columns([1, 8, 1])

    with col1:
        back_button = st.button('Back')

    with col2:
        if last_page:
            next_button = st.button('Calculate score')
        elif score_page:
            next_button = None
        else:
            next_button = st.button('Next')

    # Move to next page and refresh
    if next_button:
        st.session_state['page'] += 1
        st.rerun()

    # Move to previous page and refresh
    if back_button:
        st.session_state['page'] -= 1
        st.rerun()


def show_entry_criteria_page():
    """Page showing entry criteria for algorithm"""
    st.write("# Step 1: Entry criteria")
    col1, col2 = st.columns(2)
    with col1:
        st.write('#### At least one clinical criterion')
        for i, criterion in enumerate(CLINICAL_CRITERIA):
            persistent_checkbox(criterion, f'clinical_{i}')

    with col2:
        st.write('#### Positive antiphospholipid test within three years of the clinical criterion')
        for i, criterion in enumerate(LAB_CRITERIA):
            persistent_checkbox(criterion, f'lab_{i}')

    # Can only proceed if patient meets at least one clinical and one lab criterion
    submit_entry_criteria = st.button('Apply additive criteria', disabled=not meets_entry_criteria())

    # Refresh to show the next page
    if submit_entry_criteria:
        st.session_state['page'] += 1
        st.rerun()


def show_additive_vte_page():
    """Page showing additive criteria for D1 (venous thromboembolism)"""
    st.write("# Additive clinical criteria #")
    st.write('### D1. Macrovascular (Venous thromboembolism) ###')
    major_risk_factors_tab, minor_risk_factors_tab = st.tabs(['__Major risk factors__', '__Minor risk factors__'])
    with major_risk_factors_tab:
        st.markdown("""
        1.  **Active malignancy** with no or noncurative treatment received, ongoing curative treatment including hormonal therapy, or recurrence progression despite curative treatment at the time of the event
        2.  **Hospital admission** confined to bed (only bathroom privileges) with an acute illness for at least 3 days within 3 months prior to the event. Major trauma with fractures or spinal cord injury within 1 month prior to the event
        3.  **Surgery** with general/spinal/epidural anesthesia for >30 minutes within 3 months prior to the event
        """)
    with minor_risk_factors_tab:
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
        persistent_checkbox('VTE with a high risk profile (1 point)', 'vte_high_risk')
        st.markdown('One or more _major_ risk factors or two or more _minor_ risk factors at the time of the event')

    with col2:
        persistent_checkbox('VTE without a high risk profile (3 points)', 'vte_low_risk')

    show_next_and_back_buttons()


def show_additive_ate_page():
    """Page showing additive criteria for D2 (arterial thromboembolism)"""
    st.write("# Additive clinical criteria #")
    st.write('### D2. Macrovascular (Arterial thromboembolism) ###')
    high_risk_factors_tab, mod_risk_factors_tab = st.tabs(
        ['__High CVD risk factors__', '__Moderate CVD risk factors__'])
    with high_risk_factors_tab:
        st.markdown("""
        1.  **Arterial hypertension** with systolic blood pressure (BP) ≥180 mm Hg or diastolic BP ≥110 mm Hg
        2.  **Chronic kidney disease** with estimated glomerular filtration rate ≤60 ml/minute for more than 3 months
        3.  **Diabetes mellitus** with organ damage or long disease duration (type 1 for ≥20 years; type 2 for ≥10 years)
        4.  **Hyperlipidemia** (severe) with total cholesterol ≥310 mg/dl (8 mmoles/liter) or low-density lipoprotein (LDL)–cholesterol >190 mg/dl (4.9 mmoles/liter)
        """)
    with mod_risk_factors_tab:
        st.markdown("""
        1.  **Arterial hypertension** on treatment, or with persistent systolic BP ≥140 mm Hg or diastolic BP ≥90 mm Hg
        2.  **Current tobacco smoking**
        3.  **Diabetes mellitus** with no organ damage and short disease duration (type 1 <20 years; type 2 <10 years)
        4.  **Hyperlipidemia** (moderate) on treatment, or with total cholesterol above normal range and <310 mg/dl (8 mmoles/liter), or LDL-cholesterol above normal range and <190 mg/dl (4.9 mmoles/liter)
        5.  **Obesity** (BMI ≥30 kg/m2)
        """)

    st.markdown('#')

    col1, col2 = st.columns(2)
    with col1:
        persistent_checkbox('ATE with a high risk CVD profile (2 points)', 'ate_high_risk')
        st.markdown('One or more _high CVD risk factors_ or 3 or more _moderate CVD risk factors_')

    with col2:
        persistent_checkbox('ATE without a high risk CVD profile (4 points)', 'ate_low_risk')

    show_next_and_back_buttons()


def show_microvascular_page():
    """Page showing additive criteria for D3 (microvascular)"""
    st.write("# Additive clinical criteria #")
    st.write('### D3. Microvascular ###')
    col1, col2 = st.columns(2)
    with col1:
        st.write('##### *Suspected* (one or more of the following): 2 points')
        for text, key in MICROVASCULAR_SUSPECTED_CRITERIA.items():
            persistent_checkbox(text, key)

    with col2:
        st.write('##### *Established* (one or more of the following): 5 points')
        for text, key in MICROVASCULAR_ESTABLISHED_CRITERIA.items():
            persistent_checkbox(text, key)

    show_next_and_back_buttons()


def show_obstetric_page():
    """Page showing additive criteria for D4 (obstetric)"""
    st.write("# Additive clinical criteria #")
    st.write('### D4. Obstetric ###')
    for text, key in OBSTETRIC_CRITERIA.items():
        persistent_checkbox(text, key)

    show_next_and_back_buttons()


def show_cardiac_page():
    """Page showing additive criteria for D5 (cardiac valve)"""
    st.write("# Additive clinical criteria #")
    st.write('### D5. Cardiac valve ###')
    for text, key in CARDIAC_CRITERIA.items():
        persistent_checkbox(text, key)

    show_next_and_back_buttons()


def show_hematology_page():
    """Page showing additive criteria for D6 (hematology)"""
    st.write("# Additive clinical criteria #")
    st.write('### D6. Hematology ###')
    persistent_checkbox('Thrombocytopenia (lowest 20-130 x109/L) (**2 points**)', 'thrombocytopenia')

    show_next_and_back_buttons()


def show_lac_page():
    """Page showing additive criteria for D7 (lupus anticoagulant)"""
    st.write("# Additive laboratory criteria #")
    st.write('### D7. aPL test by coagulation-based functional assay (lupus anticoagulant test [LAC]) ###')
    for text, key in LAC_CRITERIA.items():
        persistent_checkbox(text, key)

    show_next_and_back_buttons()


def show_apl_page():
    """Page showing additive criteria for D8 (aPL tests)"""
    st.write("# Additive laboratory criteria #")
    st.write('### D8. aPL test by solid phase assay (anti-cardiolipin antibody [aCL] ELISA and/or '
             'anti-β2-glycoprotein-I antibody [aβ2GPI] ELISA [persistent]) ###')
    for text, key in APL_CRITERIA.items():
        persistent_checkbox(text, key)

    show_next_and_back_buttons(last_page=True)


def show_score():
    """Page showing the final scoring criteria"""
    st.write('You have reached the final page!')
    show_next_and_back_buttons(score_page=True)


if __name__ == '__main__':
    initialize_app()

    match st.session_state['page']:
        case 0:
            show_entry_criteria_page()

        case 1:
            show_additive_vte_page()

        case 2:
            show_additive_ate_page()

        case 3:
            show_microvascular_page()

        case 4:
            show_obstetric_page()

        case 5:
            show_cardiac_page()

        case 6:
            show_hematology_page()

        case 7:
            show_lac_page()

        case 8:
            show_apl_page()

        case 9:
            show_score()
