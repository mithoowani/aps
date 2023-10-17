from collections import namedtuple

Criterion = namedtuple('Criterion', ['key', 'domain', 'descriptor', 'points'])

criteria = {
    '16_week_fetal_death': Criterion(key='16_week_fetal_death', domain=4, descriptor='Fetal death (16w – 33w 6d) in the absence of pre-eclampsia (PEC) with severe features or placental insufficiency with severe features (**1 point**)', points=1),
    '3_consecutive_losses': Criterion(key='3_consecutive_losses', domain=4, descriptor='3 or more consecutive pre-fetal (<10w) and/or early fetal (10w -15w 6d) deaths (**1 point**)', points=1),
    'adrenal_hemorrhage_path': Criterion(key='adrenal_hemorrhage_path', domain=3, descriptor='Adrenal hemorrhage (imaging or pathology)', points=5),
    'apl_nephropathy_exam': Criterion(key='apl_nephropathy_exam', domain=3, descriptor='Acute/chronic aPL-nephropathy (exam or lab)', points=2),
    'apl_nephropathy_path': Criterion(key='apl_nephropathy_path', domain=3, descriptor='Acute/chronic aPL-nephropathy (pathology)', points=5),
    'ate_high_risk': Criterion(key='ate_high_risk', domain=2, descriptor='ATE with a high risk CVD profile (**2 points**)', points=2),
    'ate_low_risk': Criterion(key='ate_low_risk', domain=2, descriptor='ATE without a high risk CVD profile (**4 points**)', points=4),
    'high_pos_igg_and': Criterion(key='high_pos_igg_and', domain=8, descriptor='High positive IgG (aCL _AND_ aβ2GPI) (**7 points**)', points=7),
    'high_pos_igg_or': Criterion(key='high_pos_igg_or', domain=8, descriptor='High positive IgG (aCL _OR_ aβ2GPI) (**5 points**)', points=5),
    'livedo_racemosa': Criterion(key='livedo_racemosa', domain=3, descriptor='Livedo racemosa (exam)', points=2),
    'livedo_vasculopathy_exam': Criterion(key='livedo_vasculopathy_exam', domain=3, descriptor='Livedoid vasculopathy lesions (exam)', points=2),
    'livedo_vasculopathy_path': Criterion(key='livedo_vasculopathy_path', domain=3, descriptor='Livedoid vasculopathy (pathology)', points=5),
    'mod_high_igm': Criterion(key='mod_high_igm', domain=8, descriptor='Moderate or high positive IgM (aCL and/or aβ2GPI) (**1 point**)', points=1),
    'mod_pos_igg': Criterion(key='mod_pos_igg', domain=8, descriptor='Moderate positive IgG (aCL and/or aβ2GPI) (**4 points**)', points=4),
    'myocardial_path': Criterion(key='myocardial_path', domain=3, descriptor='Myocardial disease (imaging or pathology)', points=5),
    'persistent_lac': Criterion(key='persistent_lac', domain=7, descriptor='Positive LAC (persistent) (**5 points**)', points=5),
    'pre_eclampsia_and_pi': Criterion(key='pre_eclampsia_and_pi', domain=4, descriptor='Pre-eclampsia with severe features (<34w) _AND_ placental insufficiency with severe features (<34w with/without fetal death (**4 points**)', points=4),
    'pre_eclampsia_or_pi': Criterion(key='pre_eclampsia_or_pi', domain=4, descriptor='Pre-eclampsia with severe features (<34w) _OR_ placental insufficiency with severe features (<34w with/without fetal death (**3 points**)', points=3),
    'pulm_hemorrhage_path': Criterion(key='pulm_hemorrhage_path', domain=3, descriptor='Pulmonary hemorrhage (BAL or pathology)', points=5),
    'pulm_hemorrhage_symptoms': Criterion(key='pulm_hemorrhage_symptoms', domain=3, descriptor='Pulmonary hemorrhage (symptoms and imaging)', points=2),
    'single_lac': Criterion(key='single_lac', domain=7, descriptor='Positive LAC (single – one time) (**1 point**)', points=1),
    'thrombocytopenia': Criterion(key='thrombocytopenia', domain=6, descriptor='Thrombocytopenia (lowest 20-130 x109/L) (**2 points**)', points=2),
    'valve_thickening': Criterion(key='valve_thickening', domain=5, descriptor='Thickening (**2 points**)', points=2),
    'valve_vegetation': Criterion(key='valve_vegetation', domain=5, descriptor='Vegetation (**4 points**)', points=4),
    'vte_high_risk': Criterion(key='vte_high_risk', domain=1, descriptor='VTE with a high risk profile (**1 point**)', points=1),
    'vte_low_risk': Criterion(key='vte_low_risk', domain=1, descriptor='VTE without a high risk profile (**3 points**)', points=3)
}