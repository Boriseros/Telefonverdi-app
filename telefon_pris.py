# telefon_pris.py

import streamlit as st

# Mapping avdelingsnummer til MVA-status
avdeling_mva_map = {
    # Avdelingsnummer: MVA-status (1 for pliktig, 0 for ikke pliktig)    
    "1000":	1, 
    "1010":	1,
    "1020":	1,
    "1030":	1,
    "1100":	1,
    "1200":	1,
    "1300":	1,
    "1310":	1,
    "1400":	1,
    "1410":	1,
    "1420":	1,
    "2100":	0, 
    "2210":	0,
    "2211":	0,
    "2215":	0,
    "2220":	0,
    "2230":	0,
    "2240":	0,
    "2310":	0,
    "2320":	1,
    "2410":	0,
    "2420":	0,
    "2430":	0,
    "2510":	1,
    "3100":	1,
    "3101":	1,
    "3102":	1,
    "3103":	1,
    "3104":	1,
    "3105":	1,
    "3106":	1,
    "3107":	1,
    "3108":	1,
    "3109":	1,
    "3110":	1,
    "3111":	1,
    "3112":	1,
    "3113":	1,
    "3114":	1,
    "3115":	1,
    "3116":	1,
    "3117":	1,
    "3118":	1,
    "3119":	1,
    "3120":	1,
    "3121":	1,
    "3122":	1,
    "3126":	1,
    "3127":	1,
    "3128":	1,
    "3129":	1,
    "3130":	1,
    "3210":	0,
    "3220":	0,
    "3230":	0,
    "4100":	0,
    "4110":	0,
    "4120":	0,
    "4210":	0,
    "4220":	0,
    "4230":	0,
    "4240":	0,
    "4250":	0,
    "4310":	0,
    "4315":	0,
    "4510":	1,
    "4520":	1,
    "4610":	0,
    "9910":	1,
    "9920":	1,
    "9930":	0,
    "9940":	1,
    "9950":	1,
    "9960":	0,
    "9970":	0,
    "4410":	1,
    "4415":	1,
    "4420":	1,
    "4430":	1,
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
st.title("📱Brukt Mobil/PC Verdifastsetting")

#with st.form("verdi_form", clear_on_submit=False):
st.header("Opplysninger")
original_price_input = st.number_input("Originalpris (netto) fra faktura (kr)", min_value=0.0, step=100.0)
egenandel = st.number_input("Egenandel (kr)", min_value=0.0, step=100.0, value=0.0)

#avd_choice = st.selectbox("Velg avdelingsnummer", list(avdeling_mva_map.keys()))
#avd_value = avdeling_mva_map[avd_choice]
#mva_status = "Pliktig" if avd_value == 1 else "Ikke pliktig"
#st.write(f"MVA-status for {avd_choice}: {'Pliktig' if avd_value == 1 else 'Ikke pliktig'} avdeling")


#avd_value = avdeling_mva_map.get(avd_input.strip(), None)
avd_input = st.text_input("Skriv inn avdelingsnummer")

if avd_input.strip():  # only run if user typed something
    avd_value = avdeling_mva_map.get(avd_input.strip())


    if avd_value is not None:
        mva_status = "Pliktig" if avd_value == 1 else "Ikke pliktig"
        #st.write(f"**{mva_status} avdeling**")
    else:
        st.error("Skriv avdelingsnummeret.")





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
    # Get the avdeling value based on input
    
    avd_value = avdeling_mva_map.get(avd_input, 1)

    # Adjust and calculate
    adjusted_price = adjust_original_price(original_price_input, egenandel, avd_value)
    resale_value = calculate_phone_value(adjusted_price, age_months)

    if sale_type == "Gave":
        #st.info("Dette er en gave. Ingen faktura kreves.")
        st.write(f"Gaveverdi for telefon/pc: **{resale_value} kr**")

        total_gaveverdi = resale_value + (andre_gaver_verdi if har_andre_gaver else 0)

        if har_andre_gaver:
            st.write(f"Samlet gaveverdi inkl. andre gaver: **{total_gaveverdi} kr**")
    

        if avd_value == 1:  # Pliktig
            if total_gaveverdi > 5000:
                st.error("Send e-post til **HR** med samlet gaveverdi og til **Regnskap** med gaveverdi for telefon/pc (pliktig avdeling - uttaks MVA, samlet verdi over 5000 kr - trenges innberetning på lønn).")
            else:
                st.warning("Send e-post til **Regnskap** (pliktig avdeling - uttaks MVA, samlet verdi under 5000 kr - ingen innberetning på lønn).")
        else:  # Ikke pliktig
            if total_gaveverdi > 5000:
                st.error("Send e-post til **HR** med samlet gaveverdi (ikke pliktig avdeling _ ingen uttaks MVA, samlet verdi over 5000 kr - trenges innberetning på lønn).")
            else:
                st.success("Det trengs ingen videre handling (ikke pliktig avdeling og samlet verdi under 5000 kr).")

    elif sale_type == "Salg":
        st.success("Dette er et salg. Send epost til regnskap for fakturering.")
        st.write(f"Salgsverdi: **{resale_value} kr**")
