"""
Web app for applying revised EULAR 2023 antiphospholipid syndrome (APS) classification criteria
Full text: Arthritis Rheumatol . 2023 Oct;75(10):1687-1702.  doi: 10.1002/art.42624.  Epub 2023 Aug 28
"""

# TODO: Consider adding type hinting in future
# TODO: Refactor the generic pages to a common function (DRY)
# TODO: Clean up docstrings

import streamlit as st
from aps_criteria import Criterion, criteria

ENTRY_CLINICAL_CRITERIA = ['Venous thromboembolism',
                           'Arterial thromboembolism',
                           'Microvascular (_e.g._ livedo racemosa, pulmonary hemorrhage, aPL nephropathy, adrenal hemorrhage...)',
                           'Obstetric morbidity (_e.g._ 3 or more consecutive early fetal losses...)',
                           'Cardiac valve thickening or vegetation',
                           'Thrombocytopenia']

ENTRY_LAB_CRITERIA = ['Lupus anticoagulant',
                      'Anti-cardiolipin (IgG or IgM) at moderate-high titre',
                      'Anti-b2-glycoprotein I (IgG or IgM) at moderate-high titre']


def initialize_app():
    # Initialize page to start at 0
    st.session_state.setdefault('page', 0)

    # Initialize cache to save initial state of all widgets
    # As the program runs, session_state.cache will update with the saved state of all widgets
    st.session_state.setdefault('cache', dict())


def meets_entry_criteria():
    """Checks whether entry criteria are met to enter the algorithm, i.e. whether at least one clinical criterion
    and at least one laboratory criterion are checked off by the user"""
    meets_clinical_criteria = any(st.session_state[f'entry_clinical_{i}'] for i in range(len(ENTRY_CLINICAL_CRITERIA)))
    meets_lab_criteria = any(st.session_state[f'entry_lab_{i}'] for i in range(len(ENTRY_LAB_CRITERIA)))
    if meets_clinical_criteria and meets_lab_criteria:
        return True
    else:
        return False


def update_cache(key: str):
    """Updates session_sate.cache to reflect the current state of each widget; this ensures
    that the state gets preserved when switching between pages in the app"""
    st.session_state.cache[key] = st.session_state[key]


def calculate_scores():
    """Calculates the clinical and laboratory scores, returns a dictionary of scores representing total score in each
    domain. Note that only the highest score per domain counts toward the total score"""

    items_selected_per_domain = {n: [0] for n in range(1, 9)}  # each domain starts with score of 0
    score_per_domain = {n: 0 for n in range(1, 9)}

    for criterion, checked in st.session_state.cache.items():
        if checked:
            domain = criteria[criterion].domain
            points = criteria[criterion].points
            items_selected_per_domain[domain].append(points)

    for domain, points in items_selected_per_domain.items():
        score_per_domain[domain] = max(points)

    return score_per_domain


def stateful_checkbox(criterion: Criterion):
    st.session_state.cache.setdefault(criterion.key, False)

    return st.checkbox(criterion.descriptor,
                       value=st.session_state.cache[criterion.key],
                       key=criterion.key,
                       on_change=update_cache,
                       kwargs={'key': criterion.key})


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


def hide_streamlit_header_footer():
    hide_streamlit_style = """
                    <style>
                    [data-testid="stToolbar"] {visibility: hidden !important;}
                    footer {visibility: hidden !important;}
                    </style>
                    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def show_entry_criteria_page():
    """Page showing entry criteria for algorithm"""

    hide_streamlit_header_footer()

    st.write("# Entry criteria")
    col1, col2 = st.columns(2)
    with col1:
        st.write('#### At least one clinical criterion')
        for i, criterion in enumerate(ENTRY_CLINICAL_CRITERIA):
            st.checkbox(criterion, key=f'entry_clinical_{i}')

    with col2:
        st.write('#### Positive aPL test within three years of the clinical criterion')
        for i, criterion in enumerate(ENTRY_LAB_CRITERIA):
            st.checkbox(criterion, key=f'entry_lab_{i}')

    st.caption('Note: Refer to full text or subsequent pages for more details. '
               '_Moderate positive aPL test_ = 40-79 units, _high positive aPL test_ ≥ 80 units.')

    # Can only proceed if patient meets at least one clinical and one lab criterion
    submit_entry_criteria = st.button('Apply additive criteria', disabled=not meets_entry_criteria())

    # Refresh to show the next page
    if submit_entry_criteria:
        st.session_state['page'] += 1
        st.rerun()


def show_vte_page():
    """Page showing additive criteria for D1 (venous thromboembolism)"""

    hide_streamlit_header_footer()

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
        stateful_checkbox(criteria['vte_high_risk'])
        st.caption('One or more _major_ risk factors or two or more _minor_ risk factors at the time of the event')

    with col2:
        stateful_checkbox(criteria['vte_low_risk'])

    show_next_and_back_buttons()


def show_ate_page():
    """Page showing additive criteria for D2 (arterial thromboembolism)"""

    hide_streamlit_header_footer()

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
        stateful_checkbox(criteria['ate_high_risk'])
        st.caption('One or more _high CVD risk factors_ or 3 or more _moderate CVD risk factors_')

    with col2:
        stateful_checkbox(criteria['ate_low_risk'])

    show_next_and_back_buttons()


def show_microvascular_page():
    """Page showing additive criteria for D3 (microvascular)"""

    hide_streamlit_header_footer()

    suspected_microvascular_criteria = [criterion for criterion in criteria.values() if (criterion.domain == 3 and
                                                                                         criterion.points == 2)]

    established_microvascular_criteria = [criterion for criterion in criteria.values() if (criterion.domain == 3 and
                                                                                           criterion.points == 5)]

    st.write("# Additive clinical criteria #")
    st.write('### D3. Microvascular ###')
    col1, col2 = st.columns(2)
    with col1:
        st.write('##### *Suspected* (one or more of the following): 2 points')
        for key in suspected_microvascular_criteria:
            stateful_checkbox(key)

    with col2:
        st.write('##### *Established* (one or more of the following): 5 points')
        for key in established_microvascular_criteria:
            stateful_checkbox(key)

    show_next_and_back_buttons()


def show_obstetric_page():
    """Page showing additive criteria for D4 (obstetric)"""

    hide_streamlit_header_footer()

    obstetric_criteria = [criterion for criterion in criteria.values() if criterion.domain == 4]
    obstetric_criteria.sort(key=lambda x: x.points)

    st.write("# Additive clinical criteria #")
    st.write('### D4. Obstetric ###')
    for key in obstetric_criteria:
        stateful_checkbox(key)

    show_next_and_back_buttons()


def show_cardiac_page():
    """Page showing additive criteria for D5 (cardiac valve)"""

    hide_streamlit_header_footer()

    cardiac_criteria = [criterion for criterion in criteria.values() if criterion.domain == 5]
    cardiac_criteria.sort(key=lambda x: x.points)

    st.write("# Additive clinical criteria #")
    st.write('### D5. Cardiac valve ###')
    for key in cardiac_criteria:
        stateful_checkbox(key)

    show_next_and_back_buttons()


def show_hematology_page():
    """Page showing additive criteria for D6 (hematology)"""

    hide_streamlit_header_footer()

    heme_criteria = [criterion for criterion in criteria.values() if criterion.domain == 6]

    st.write("# Additive clinical criteria #")
    st.write('### D6. Hematology ###')
    for key in heme_criteria:
        stateful_checkbox(key)

    show_next_and_back_buttons()


def show_lac_page():
    """Page showing additive criteria for D7 (lupus anticoagulant)"""

    hide_streamlit_header_footer()

    lac_criteria = [criterion for criterion in criteria.values() if criterion.domain == 7]
    lac_criteria.sort(key=lambda x: x.points)

    st.write("# Additive laboratory criteria #")
    st.write('### D7. aPL test by coagulation-based functional assay (lupus anticoagulant test [LAC]) ###')
    for key in lac_criteria:
        stateful_checkbox(key)

    st.caption('Note: Refer to full text for accepted laboratory procedures.')

    show_next_and_back_buttons()


def show_apl_page():
    """Page showing additive criteria for D8 (aPL tests)"""

    hide_streamlit_header_footer()

    apl_criteria = [criterion for criterion in criteria.values() if criterion.domain == 8]
    apl_criteria.sort(key=lambda x: x.points)

    st.write("# Additive laboratory criteria #")
    st.write('### D8. aPL test by solid phase assay (anti-cardiolipin antibody [aCL] ELISA and/or '
             'anti-β2-glycoprotein-I antibody [aβ2GPI] ELISA [persistent]) ###')
    for key in apl_criteria:
        stateful_checkbox(key)

    st.caption('Note: _Moderate positive aPL test_ = 40-79 units, _high positive aPL test_ ≥ 80 units. Refer to full '
               'text for accepted laboratory procedures.')

    show_next_and_back_buttons(last_page=True)


def show_score():
    """Page showing the final scoring criteria"""

    hide_streamlit_header_footer()

    scores = calculate_scores()
    total_clinical_score = sum(scores[i] for i in range(1, 7))
    total_lab_score = sum(scores[i] for i in range(7, 9))

    score_text = f"""
    Domain                                  Score
    D1: Venous thromboembolism              {scores[1]}              
    D2: Arterial thromboembolism            {scores[2]} 
    D3: Microvascular                       {scores[3]} 
    D4: Obstetric                           {scores[4]} 
    D5: Cardiac Valve                       {scores[5]} 
    D6: Hematology                          {scores[6]}     
    --------------------------------------------------
    Total Clinical                          {total_clinical_score}
    
    D7: Laboratory (lupus anticoagulant)    {scores[7]} 
    D8: Laboratory (aPL serology)           {scores[8]} 
    --------------------------------------------------
    Total Lab                               {total_lab_score}
    """

    st.write("# Total score #")
    st.write('_Classified as APS for research purposes if there are at least 3 points '
             'from clinical domains **AND** at least 3 points from laboratory domains_')

    st.markdown('#####')

    if total_clinical_score >= 3 and total_lab_score >= 3:
        st.write('##### Result: Classified as APS for research purposes')

    else:
        st.write('##### Result: Does not meet APS classification criteria')

    st.code(score_text)  # This displays nicely for EMR copy/paste
    st.caption('Copy and paste into your EMR')

    st.markdown('#####')

    show_next_and_back_buttons(score_page=True)


if __name__ == '__main__':
    initialize_app()

    match st.session_state['page']:
        case 0:
            show_entry_criteria_page()

        case 1:
            show_vte_page()

        case 2:
            show_ate_page()

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
