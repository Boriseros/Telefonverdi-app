# telefon_pris.py

import streamlit as st

# Mapping avdelingsnummer til MVA-status
avdeling_mva_map = {
    "1": 1,  # Pliktig
    "2": 1,
    "3": 0   # Ikke pliktig
}

# Justerer originalprisen med egenandel og MVA
def adjust_original_price(original_price, egenandel, avd_value):
    price_after_egenandel = original_price - egenandel
    if avd_value == 0:
        return price_after_egenandel * 1.25
    else:
        return price_after_egenandel

# Rest verdi basert på alder i måneder
def calculate_phone_value(original_price, age_months):
    if age_months < 12:
        value = original_price * 0.8
    elif 12 <= age_months < 24:
        value = original_price * 0.5
    elif 24 <= age_months < 36:
        value = original_price * 0.2
    else:  # 36 måneder og oppover
        value = 500
    return round(value, 2)

# Streamlit UI
st.set_page_config(page_title="Verdifastsetting", page_icon="📱")
st.title("Brukt Mobil/PC Verdifastsetting")

#with st.form("verdi_form", clear_on_submit=False):
st.header("Opplysninger")
original_price_input = st.number_input("Originalpris (kr)", min_value=0.0, step=100.0)
egenandel = st.number_input("Egenandel (kr)", min_value=0.0, step=100.0, value=0.0)

#avd_choice = st.selectbox("Velg avdelingsnummer", list(avdeling_mva_map.keys()))
#avd_value = avdeling_mva_map[avd_choice]
#mva_status = "Pliktig" if avd_value == 1 else "Ikke pliktig"
#st.write(f"MVA-status for {avd_choice}: {'Pliktig' if avd_value == 1 else 'Ikke pliktig'} avdeling")

avd_input = st.text_input("Skriv inn avdelingsnummer")

avd_value = avdeling_mva_map.get(avd_input.strip(), None)

if avd_value is not None:
    mva_status = "Pliktig" if avd_value == 1 else "Ikke pliktig"
    st.write(f"MVA-status for Avd. {avd_input}: **{mva_status} avdeling**")
else:
    st.warning("⚠️ Avdelingsnummeret finnes ikke i systemet.")






#age = st.slider("Alder på enheten (år)", 0.0, 4.0, step = 0.1)
# Input: age in months
age_months = st.slider("Alder på enheten (måneder)", 0, 72, 12, step=1)

# Convert to human-friendly format
years = age_months // 12
months = age_months % 12

if years > 0 and months > 0:
    alder_visning = f"{years} år og {months} måneder"
elif years > 0:
    alder_visning = f"{years} år"
else:
    alder_visning = f"{months} måneder"

st.write(f"Alder på enheten: **{alder_visning}**")
   

sale_type = st.radio("Er dette en gave eller et salg?", ["Gave", "Salg"], index=None)

    # Only show this if Gave is selected
har_andre_gaver = False
andre_gaver_verdi = 0.0
if sale_type == "Gave":
    har_andre_gaver = st.checkbox("Har den ansatte fått andre gaver i år?")
    if har_andre_gaver:
        andre_gaver_verdi = st.number_input(
            "Total verdi av andre gaver (kr)",
            min_value=0.0,
            step=100.0,
            key="andre_gaver_input"
        )

# Form only wraps the button
with st.form("beregn_form"):
    submitted = st.form_submit_button("Beregn verdi")


if submitted:
    # Determine avd_value from avd_choice
    avdeling_mva_map = {
        "Avd. 1": 1,
        "Avd. 2": 1,
        "Avd. 3": 0
    }
    avd_value = avdeling_mva_map.get(avd_choice, 1)

    # Adjust and calculate
    adjusted_price = adjust_original_price(original_price_input, egenandel, avd_value)
    resale_value = calculate_phone_value(adjusted_price, age_months)

    if sale_type == "Gave":
        st.info("🎁 Dette er en gave. Ingen faktura kreves.")
        st.write(f"Gaveverdi: **{resale_value} kr**")

        total_gaveverdi = resale_value + (andre_gaver_verdi if har_andre_gaver else 0)

        st.write(f"📊 Samlet gaveverdi inkl. andre gaver: **{total_gaveverdi} kr**")

        if avd_value == 1:  # Pliktig
            if total_gaveverdi > 5000:
                st.error("🚨 Send e-post til **HR og regnskap** (pliktig avdeling, samlet verdi over 5000 kr).")
            else:
                st.warning("✉️ Send e-post til **regnskap for uttaks-MVA** (pliktig avdeling, samlet verdi under 5000 kr).")
        else:  # Ikke pliktig
            if total_gaveverdi > 5000:
                st.error("🚨 Send e-post til **HR** (ikke pliktig avdeling, samlet verdi over 5000 kr).")
            else:
                st.success("✅ Det trengs ingen videre handling (ikke pliktig, samlet verdi under 5000 kr).")

    elif sale_type == "Salg":
        st.success("🧾 Dette er et salg. Faktura kreves.")
        st.write(f"Salgsverdi: **{resale_value} kr**")
