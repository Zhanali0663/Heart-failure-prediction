import streamlit as st
import requests
st.title('Heart-failure-prediction')

with st.form('Подать заявку'):
    Age = st.number_input("Ваш возраст", min_value=18, max_value=110, step=1, value=40)
    Sex = st.selectbox("Пол", ["M", "F"])
    ChestPainType = st.selectbox("Тип боли в груди", ["ASY", "ATA", "NAP", "TA"])
    RestingBP = st.number_input("Давление в покое", min_value=80, max_value=240, step=1, value=120)
    Cholesterol = st.number_input("Холестерин", min_value=80, max_value=500, step=1, value=200)
    FastingBS = st.selectbox("Сахар в крови > 120 (1-да, 0-нет)", [0, 1])
    RestingECG = st.selectbox("ЭКГ в покое", ["Normal", "ST", "LVH"])
    MaxHR = st.number_input("Максимальный пульс", min_value=40, max_value=220, step=5, value=150)
    ExerciseAngina = st.selectbox("Боли при нагрузке", ["N", "Y"])
    Oldpeak = st.number_input("Депрессия ST (Oldpeak)", min_value=0.0, max_value=6.0, step=0.1, value=0.0)
    ST_Slope = st.selectbox("Наклон ST", ["Up", "Flat", "Down"])

    submit = st.form_submit_button('Отправить')

if submit:
    data = {
            "Age": Age, "Sex": Sex, "ChestPainType": ChestPainType,
            "RestingBP": RestingBP, "Cholesterol": Cholesterol,
            "FastingBS": FastingBS, "RestingECG": RestingECG,
            "MaxHR": MaxHR, "ExerciseAngina": ExerciseAngina,
            "Oldpeak": Oldpeak, "ST_Slope": ST_Slope
        }
    
    response = requests.post('http://127.0.0.1:8000/score', json=data)
    result = response.json()
    prob = result['Probability']
    factors = result.get('TopFactors', [])
    
    if result['HeartDisease']:
        st.warning(f'У вас есть болезн. Вероятность: {prob}%')
    else:
        st.success(f'У вас все в порядке Вероятность болезни: {prob}%')

    st.write("### Почему система так решила?")
    for factor, value in factors:
        direction = "повышает риск" if value > 0 else "снижает риск"
        icon = "🚩" if value > 0 else "✅"
        st.write(f"{icon} Фактор **{factor}** значительно {direction}")
    