import os
from datetime import date

import requests
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL","http://localhost:8000")

if not API_BASE_URL:
    st.warning(
        "API_BASE_URL is not configured. Please set the API_BASE_URL environment variable to your backend URL."
    )
    st.stop()

API_BASE_URL = API_BASE_URL.rstrip("/")

LANGUAGES = {
    "en": "English",
    "hi": "हिन्दी",
    "te": "తెలుగు",
    "ta": "தமிழ்",
    "ml": "മലയാളം",
    "kn": "ಕನ್ನಡ",
}

TRANSLATIONS = {
    "en": {
        "app_title": "Elder Care Assistant",
        "app_tagline": "Compassionate care, one step at a time",
        "language": "Language",
        "localhost_warning": "Running on localhost. Set API_BASE_URL to your backend host for deployed environments.",
        "login_required": "👋 Please sign in or create an account to use this section.",
        "tab.account": "👤 Account",
        "tab.health": "🩺 Health",
        "tab.reminders": "⏰ Reminders",
        "tab.chat": "💬 Chat",
        "tab.family": "👨‍👩‍👧 Family",
        "tab.emergency": "🚨 Emergency",
        "sign_in": "Sign In",
        "create_account": "Create Account",
        "email": "Email",
        "password": "Password",
        "sign_in_button": "Sign in →",
        "signed_in": "✅ Signed in successfully!",
        "first_name": "First name",
        "last_name": "Last name",
        "date_of_birth": "Date of birth",
        "phone_number": "Phone number",
        "create_account_button": "Create account →",
        "account_created": "🎉 Account created for {name}!",
        "sign_out": "Sign out",
        "add_health_reading": "🩺 Add Health Reading",
        "reading_type": "Reading type",
        "primary_value": "Primary value",
        "secondary_value": "Secondary value (if any)",
        "unit": "Unit",
        "notes": "Notes",
        "save_reading": "Save reading →",
        "reading_saved": "✅ Reading saved — status: {status}",
        "health_summary": "📊 Health Summary",
        "add_reminder": "⏰ Add Reminder",
        "reminder_type": "Reminder type",
        "title": "Title",
        "description": "Description",
        "schedule": "Schedule",
        "time": "Time",
        "create_reminder": "Create reminder →",
        "reminder_created": "✅ Reminder created: {title}",
        "upcoming_reminders": "📋 Upcoming Reminders",
        "medicine_information": "💊 Medicine Information",
        "enter_medicine_name": "Enter medicine name",
        "explain_medicine": "Explain this medicine →",
        "chat_with_assistant": "💬 Chat with Assistant",
        "chat_placeholder": "Ask me anything...",
        "add_family_member": "👨‍👩‍👧 Add Family Member",
        "family_email": "Family member's email",
        "phone_help": "Include country code, e.g. +919876543210",
        "relationship": "Relationship (e.g. Son, Daughter)",
        "can_view_health": "Can view health records",
        "can_edit_reminders": "Can edit reminders",
        "add_family_member_button": "Add family member →",
        "email_required": "Please enter an email address.",
        "family_added": "✅ Added {email}",
        "members": "👥 Members",
        "no_family_members": "No family members added yet.",
        "phone_numbers": "📞 Phone Numbers",
        "emergency_response": "🚨 Emergency Response",
        "emergency_warning": "Use this only in a real emergency. This will alert your emergency contacts immediately.",
        "emergency_type": "Emergency type",
        "severity": "Severity",
        "activate_emergency": "🚨 Activate Emergency Protocol",
        "reading_type.blood_pressure": "Blood pressure",
        "reading_type.glucose": "Glucose",
        "reading_type.temperature": "Temperature",
        "reading_type.heart_rate": "Heart rate",
        "reading_type.oxygen": "Oxygen",
        "reminder_type.medication": "Medication",
        "reminder_type.appointment": "Appointment",
        "reminder_type.activity": "Activity",
        "reminder_type.hydration": "Hydration",
        "schedule.daily": "Daily",
        "schedule.weekly": "Weekly",
        "schedule.once": "Once",
        "emergency_type.general": "General",
        "emergency_type.fall": "Fall",
        "emergency_type.medical": "Medical",
        "emergency_type.medication": "Medication",
        "severity.high": "High",
        "severity.critical": "Critical",
    },
    "hi": {
        "app_title": "वरिष्ठ देखभाल सहायक",
        "app_tagline": "सहानुभूतिपूर्ण देखभाल, एक समय में एक कदम",
        "language": "भाषा",
        "localhost_warning": "ऐप localhost पर चल रहा है। डिप्लॉयमेंट के लिए API_BASE_URL को अपने backend host पर सेट करें।",
        "login_required": "👋 इस भाग का उपयोग करने के लिए कृपया साइन इन करें या खाता बनाएं।",
        "tab.account": "👤 खाता",
        "tab.health": "🩺 स्वास्थ्य",
        "tab.reminders": "⏰ रिमाइंडर",
        "tab.chat": "💬 चैट",
        "tab.family": "👨‍👩‍👧 परिवार",
        "tab.emergency": "🚨 आपातकाल",
        "sign_in": "साइन इन",
        "create_account": "खाता बनाएं",
        "email": "ईमेल",
        "password": "पासवर्ड",
        "sign_in_button": "साइन इन करें →",
        "signed_in": "✅ सफलतापूर्वक साइन इन हो गया!",
        "first_name": "पहला नाम",
        "last_name": "अंतिम नाम",
        "date_of_birth": "जन्म तिथि",
        "phone_number": "फोन नंबर",
        "create_account_button": "खाता बनाएं →",
        "account_created": "🎉 {name} के लिए खाता बन गया!",
        "sign_out": "साइन आउट",
        "add_health_reading": "🩺 स्वास्थ्य रीडिंग जोड़ें",
        "reading_type": "रीडिंग प्रकार",
        "primary_value": "मुख्य मान",
        "secondary_value": "दूसरा मान (यदि हो)",
        "unit": "इकाई",
        "notes": "नोट्स",
        "save_reading": "रीडिंग सेव करें →",
        "reading_saved": "✅ रीडिंग सेव हुई — स्थिति: {status}",
        "health_summary": "📊 स्वास्थ्य सारांश",
        "add_reminder": "⏰ रिमाइंडर जोड़ें",
        "reminder_type": "रिमाइंडर प्रकार",
        "title": "शीर्षक",
        "description": "विवरण",
        "schedule": "समय-सारणी",
        "time": "समय",
        "create_reminder": "रिमाइंडर बनाएं →",
        "reminder_created": "✅ रिमाइंडर बना: {title}",
        "upcoming_reminders": "📋 आने वाले रिमाइंडर",
        "medicine_information": "💊 दवा की जानकारी",
        "enter_medicine_name": "दवा का नाम दर्ज करें",
        "explain_medicine": "इस दवा को समझाएं →",
        "chat_with_assistant": "💬 सहायक से चैट करें",
        "chat_placeholder": "कुछ भी पूछें...",
        "add_family_member": "👨‍👩‍👧 परिवार सदस्य जोड़ें",
        "family_email": "परिवार सदस्य का ईमेल",
        "phone_help": "देश कोड शामिल करें, जैसे +919876543210",
        "relationship": "रिश्ता (जैसे बेटा, बेटी)",
        "can_view_health": "स्वास्थ्य रिकॉर्ड देख सकता/सकती है",
        "can_edit_reminders": "रिमाइंडर संपादित कर सकता/सकती है",
        "add_family_member_button": "परिवार सदस्य जोड़ें →",
        "email_required": "कृपया ईमेल पता दर्ज करें।",
        "family_added": "✅ {email} जोड़ा गया",
        "members": "👥 सदस्य",
        "no_family_members": "अभी कोई परिवार सदस्य नहीं जोड़ा गया है।",
        "phone_numbers": "📞 फोन नंबर",
        "emergency_response": "🚨 आपातकालीन प्रतिक्रिया",
        "emergency_warning": "इसे केवल वास्तविक आपातकाल में उपयोग करें। यह आपके आपातकालीन संपर्कों को तुरंत सूचित करेगा।",
        "emergency_type": "आपातकाल प्रकार",
        "severity": "गंभीरता",
        "activate_emergency": "🚨 आपातकालीन प्रोटोकॉल सक्रिय करें",
        "reading_type.blood_pressure": "रक्तचाप",
        "reading_type.glucose": "ग्लूकोज",
        "reading_type.temperature": "तापमान",
        "reading_type.heart_rate": "हृदय गति",
        "reading_type.oxygen": "ऑक्सीजन",
        "reminder_type.medication": "दवा",
        "reminder_type.appointment": "अपॉइंटमेंट",
        "reminder_type.activity": "गतिविधि",
        "reminder_type.hydration": "पानी पीना",
        "schedule.daily": "रोजाना",
        "schedule.weekly": "साप्ताहिक",
        "schedule.once": "एक बार",
        "emergency_type.general": "सामान्य",
        "emergency_type.fall": "गिरना",
        "emergency_type.medical": "चिकित्सा",
        "emergency_type.medication": "दवा",
        "severity.high": "उच्च",
        "severity.critical": "गंभीर",
    },
    "te": {
        "app_title": "వృద్ధుల సంరక్షణ సహాయకుడు",
        "app_tagline": "కరుణతో కూడిన సంరక్షణ, ఒక్కో అడుగుగా",
        "language": "భాష",
        "localhost_warning": "యాప్ localhost పై నడుస్తోంది. డిప్లాయ్ చేసినప్పుడు API_BASE_URL ను మీ backend host కు సెట్ చేయండి.",
        "login_required": "👋 ఈ విభాగాన్ని ఉపయోగించడానికి దయచేసి సైన్ ఇన్ చేయండి లేదా ఖాతా సృష్టించండి.",
        "tab.account": "👤 ఖాతా",
        "tab.health": "🩺 ఆరోగ్యం",
        "tab.reminders": "⏰ గుర్తింపులు",
        "tab.chat": "💬 చాట్",
        "tab.family": "👨‍👩‍👧 కుటుంబం",
        "tab.emergency": "🚨 అత్యవసరం",
        "sign_in": "సైన్ ఇన్",
        "create_account": "ఖాతా సృష్టించండి",
        "email": "ఇమెయిల్",
        "password": "పాస్‌వర్డ్",
        "sign_in_button": "సైన్ ఇన్ చేయండి →",
        "signed_in": "✅ విజయవంతంగా సైన్ ఇన్ అయ్యారు!",
        "first_name": "మొదటి పేరు",
        "last_name": "చివరి పేరు",
        "date_of_birth": "పుట్టిన తేదీ",
        "phone_number": "ఫోన్ నంబర్",
        "create_account_button": "ఖాతా సృష్టించండి →",
        "account_created": "🎉 {name} కోసం ఖాతా సృష్టించబడింది!",
        "sign_out": "సైన్ అవుట్",
        "add_health_reading": "🩺 ఆరోగ్య రీడింగ్ జోడించండి",
        "reading_type": "రీడింగ్ రకం",
        "primary_value": "ప్రధాన విలువ",
        "secondary_value": "రెండవ విలువ (ఉంటే)",
        "unit": "యూనిట్",
        "notes": "గమనికలు",
        "save_reading": "రీడింగ్ సేవ్ చేయండి →",
        "reading_saved": "✅ రీడింగ్ సేవ్ అయింది — స్థితి: {status}",
        "health_summary": "📊 ఆరోగ్య సారాంశం",
        "add_reminder": "⏰ గుర్తింపు జోడించండి",
        "reminder_type": "గుర్తింపు రకం",
        "title": "శీర్షిక",
        "description": "వివరణ",
        "schedule": "షెడ్యూల్",
        "time": "సమయం",
        "create_reminder": "గుర్తింపు సృష్టించండి →",
        "reminder_created": "✅ గుర్తింపు సృష్టించబడింది: {title}",
        "upcoming_reminders": "📋 రాబోయే గుర్తింపులు",
        "medicine_information": "💊 మందు సమాచారం",
        "enter_medicine_name": "మందు పేరు నమోదు చేయండి",
        "explain_medicine": "ఈ మందును వివరించండి →",
        "chat_with_assistant": "💬 సహాయకుడితో చాట్ చేయండి",
        "chat_placeholder": "ఏదైనా అడగండి...",
        "add_family_member": "👨‍👩‍👧 కుటుంబ సభ్యుడిని జోడించండి",
        "family_email": "కుటుంబ సభ్యుడి ఇమెయిల్",
        "phone_help": "దేశ కోడ్ చేర్చండి, ఉదా. +919876543210",
        "relationship": "సంబంధం (ఉదా. కుమారుడు, కుమార్తె)",
        "can_view_health": "ఆరోగ్య రికార్డులు చూడగలరు",
        "can_edit_reminders": "గుర్తింపులను సవరించగలరు",
        "add_family_member_button": "కుటుంబ సభ్యుడిని జోడించండి →",
        "email_required": "దయచేసి ఇమెయిల్ చిరునామా నమోదు చేయండి.",
        "family_added": "✅ {email} జోడించబడింది",
        "members": "👥 సభ్యులు",
        "no_family_members": "ఇంకా కుటుంబ సభ్యులు జోడించబడలేదు.",
        "phone_numbers": "📞 ఫోన్ నంబర్లు",
        "emergency_response": "🚨 అత్యవసర స్పందన",
        "emergency_warning": "ఇది నిజమైన అత్యవసర పరిస్థితిలో మాత్రమే ఉపయోగించండి. ఇది మీ అత్యవసర పరిచయాలకు వెంటనే హెచ్చరిక పంపుతుంది.",
        "emergency_type": "అత్యవసర రకం",
        "severity": "తీవ్రత",
        "activate_emergency": "🚨 అత్యవసర ప్రోటోకాల్ సక్రియం చేయండి",
        "reading_type.blood_pressure": "రక్తపోటు",
        "reading_type.glucose": "గ్లూకోజ్",
        "reading_type.temperature": "ఉష్ణోగ్రత",
        "reading_type.heart_rate": "హృదయ స్పందన",
        "reading_type.oxygen": "ఆక్సిజన్",
        "reminder_type.medication": "మందు",
        "reminder_type.appointment": "అపాయింట్‌మెంట్",
        "reminder_type.activity": "కార్యకలాపం",
        "reminder_type.hydration": "నీరు తాగడం",
        "schedule.daily": "రోజూ",
        "schedule.weekly": "వారానికి",
        "schedule.once": "ఒక్కసారి",
        "emergency_type.general": "సాధారణ",
        "emergency_type.fall": "పడిపోవడం",
        "emergency_type.medical": "వైద్య",
        "emergency_type.medication": "మందు",
        "severity.high": "అధిక",
        "severity.critical": "తీవ్రం",
    },
    "ta": {
        "app_title": "மூத்தோர் பராமரிப்பு உதவியாளர்",
        "app_tagline": "கருணையுள்ள பராமரிப்பு, ஒரு படியாக",
        "language": "மொழி",
        "localhost_warning": "ஆப் localhost-ல் இயங்குகிறது. deployment-க்கு API_BASE_URL-ஐ உங்கள் backend host-க்கு அமைக்கவும்.",
        "login_required": "👋 இந்தப் பகுதியைப் பயன்படுத்த தயவுசெய்து உள்நுழையுங்கள் அல்லது கணக்கு உருவாக்குங்கள்.",
        "tab.account": "👤 கணக்கு",
        "tab.health": "🩺 உடல்நலம்",
        "tab.reminders": "⏰ நினைவூட்டல்கள்",
        "tab.chat": "💬 அரட்டை",
        "tab.family": "👨‍👩‍👧 குடும்பம்",
        "tab.emergency": "🚨 அவசரம்",
        "sign_in": "உள்நுழை",
        "create_account": "கணக்கு உருவாக்கு",
        "email": "மின்னஞ்சல்",
        "password": "கடவுச்சொல்",
        "sign_in_button": "உள்நுழை →",
        "signed_in": "✅ வெற்றிகரமாக உள்நுழைந்தீர்கள்!",
        "first_name": "முதல் பெயர்",
        "last_name": "கடைசி பெயர்",
        "date_of_birth": "பிறந்த தேதி",
        "phone_number": "தொலைபேசி எண்",
        "create_account_button": "கணக்கு உருவாக்கு →",
        "account_created": "🎉 {name} க்கு கணக்கு உருவாக்கப்பட்டது!",
        "sign_out": "வெளியேறு",
        "add_health_reading": "🩺 உடல்நல அளவைச் சேர்க்கவும்",
        "reading_type": "அளவு வகை",
        "primary_value": "முதன்மை மதிப்பு",
        "secondary_value": "இரண்டாம் மதிப்பு (இருந்தால்)",
        "unit": "அலகு",
        "notes": "குறிப்புகள்",
        "save_reading": "அளவை சேமி →",
        "reading_saved": "✅ அளவு சேமிக்கப்பட்டது — நிலை: {status}",
        "health_summary": "📊 உடல்நல சுருக்கம்",
        "add_reminder": "⏰ நினைவூட்டல் சேர்க்கவும்",
        "reminder_type": "நினைவூட்டல் வகை",
        "title": "தலைப்பு",
        "description": "விளக்கம்",
        "schedule": "அட்டவணை",
        "time": "நேரம்",
        "create_reminder": "நினைவூட்டல் உருவாக்கு →",
        "reminder_created": "✅ நினைவூட்டல் உருவாக்கப்பட்டது: {title}",
        "upcoming_reminders": "📋 வரவிருக்கும் நினைவூட்டல்கள்",
        "medicine_information": "💊 மருந்து தகவல்",
        "enter_medicine_name": "மருந்து பெயரை உள்ளிடவும்",
        "explain_medicine": "இந்த மருந்தை விளக்கவும் →",
        "chat_with_assistant": "💬 உதவியாளருடன் அரட்டை",
        "chat_placeholder": "எதையும் கேளுங்கள்...",
        "add_family_member": "👨‍👩‍👧 குடும்ப உறுப்பினரைச் சேர்க்கவும்",
        "family_email": "குடும்ப உறுப்பினரின் மின்னஞ்சல்",
        "phone_help": "நாடு குறியீட்டைச் சேர்க்கவும், உதா. +919876543210",
        "relationship": "உறவு (உதா. மகன், மகள்)",
        "can_view_health": "உடல்நல பதிவுகளை பார்க்கலாம்",
        "can_edit_reminders": "நினைவூட்டல்களைத் திருத்தலாம்",
        "add_family_member_button": "குடும்ப உறுப்பினரைச் சேர்க்கவும் →",
        "email_required": "தயவுசெய்து மின்னஞ்சல் முகவரியை உள்ளிடவும்.",
        "family_added": "✅ {email} சேர்க்கப்பட்டது",
        "members": "👥 உறுப்பினர்கள்",
        "no_family_members": "இன்னும் குடும்ப உறுப்பினர்கள் சேர்க்கப்படவில்லை.",
        "phone_numbers": "📞 தொலைபேசி எண்கள்",
        "emergency_response": "🚨 அவசர பதில்",
        "emergency_warning": "உண்மையான அவசரநிலையில் மட்டும் இதைப் பயன்படுத்தவும். இது உங்கள் அவசர தொடர்புகளுக்கு உடனடியாக எச்சரிக்கை அனுப்பும்.",
        "emergency_type": "அவசர வகை",
        "severity": "தீவிரம்",
        "activate_emergency": "🚨 அவசர நடைமுறையை செயல்படுத்து",
        "reading_type.blood_pressure": "இரத்த அழுத்தம்",
        "reading_type.glucose": "குளுக்கோஸ்",
        "reading_type.temperature": "வெப்பநிலை",
        "reading_type.heart_rate": "இதய துடிப்பு",
        "reading_type.oxygen": "ஆக்சிஜன்",
        "reminder_type.medication": "மருந்து",
        "reminder_type.appointment": "நேர்முகம்",
        "reminder_type.activity": "செயல்பாடு",
        "reminder_type.hydration": "தண்ணீர் குடித்தல்",
        "schedule.daily": "தினமும்",
        "schedule.weekly": "வாரந்தோறும்",
        "schedule.once": "ஒருமுறை",
        "emergency_type.general": "பொது",
        "emergency_type.fall": "விழுதல்",
        "emergency_type.medical": "மருத்துவம்",
        "emergency_type.medication": "மருந்து",
        "severity.high": "உயர்",
        "severity.critical": "மிக தீவிரம்",
    },
    "ml": {
        "app_title": "വയോജന പരിചരണ സഹായി",
        "app_tagline": "കരുണയുള്ള പരിചരണം, ഓരോ ഘട്ടമായി",
        "language": "ഭാഷ",
        "localhost_warning": "ആപ്പ് localhost-ൽ പ്രവർത്തിക്കുന്നു. deploy ചെയ്യുമ്പോൾ API_BASE_URL നിങ്ങളുടെ backend host ആയി സജ്ജമാക്കുക.",
        "login_required": "👋 ഈ വിഭാഗം ഉപയോഗിക്കാൻ ദയവായി സൈൻ ഇൻ ചെയ്യുക അല്ലെങ്കിൽ അക്കൗണ്ട് സൃഷ്ടിക്കുക.",
        "tab.account": "👤 അക്കൗണ്ട്",
        "tab.health": "🩺 ആരോഗ്യം",
        "tab.reminders": "⏰ ഓർമ്മപ്പെടുത്തലുകൾ",
        "tab.chat": "💬 ചാറ്റ്",
        "tab.family": "👨‍👩‍👧 കുടുംബം",
        "tab.emergency": "🚨 അടിയന്തരാവസ്ഥ",
        "sign_in": "സൈൻ ഇൻ",
        "create_account": "അക്കൗണ്ട് സൃഷ്ടിക്കുക",
        "email": "ഇമെയിൽ",
        "password": "പാസ്‌വേഡ്",
        "sign_in_button": "സൈൻ ഇൻ ചെയ്യുക →",
        "signed_in": "✅ വിജയകരമായി സൈൻ ഇൻ ചെയ്തു!",
        "first_name": "പേര്",
        "last_name": "അവസാന പേര്",
        "date_of_birth": "ജനന തീയതി",
        "phone_number": "ഫോൺ നമ്പർ",
        "create_account_button": "അക്കൗണ്ട് സൃഷ്ടിക്കുക →",
        "account_created": "🎉 {name} നായി അക്കൗണ്ട് സൃഷ്ടിച്ചു!",
        "sign_out": "സൈൻ ഔട്ട്",
        "add_health_reading": "🩺 ആരോഗ്യ റീഡിംഗ് ചേർക്കുക",
        "reading_type": "റീഡിംഗ് തരം",
        "primary_value": "പ്രാഥമിക മൂല്യം",
        "secondary_value": "രണ്ടാം മൂല്യം (ഉണ്ടെങ്കിൽ)",
        "unit": "യൂണിറ്റ്",
        "notes": "കുറിപ്പുകൾ",
        "save_reading": "റീഡിംഗ് സേവ് ചെയ്യുക →",
        "reading_saved": "✅ റീഡിംഗ് സേവ് ചെയ്തു — നില: {status}",
        "health_summary": "📊 ആരോഗ്യ സംഗ്രഹം",
        "add_reminder": "⏰ ഓർമ്മപ്പെടുത്തൽ ചേർക്കുക",
        "reminder_type": "ഓർമ്മപ്പെടുത്തൽ തരം",
        "title": "ശീർഷകം",
        "description": "വിവരണം",
        "schedule": "ഷെഡ്യൂൾ",
        "time": "സമയം",
        "create_reminder": "ഓർമ്മപ്പെടുത്തൽ സൃഷ്ടിക്കുക →",
        "reminder_created": "✅ ഓർമ്മപ്പെടുത്തൽ സൃഷ്ടിച്ചു: {title}",
        "upcoming_reminders": "📋 വരാനിരിക്കുന്ന ഓർമ്മപ്പെടുത്തലുകൾ",
        "medicine_information": "💊 മരുന്ന് വിവരം",
        "enter_medicine_name": "മരുന്നിന്റെ പേര് നൽകുക",
        "explain_medicine": "ഈ മരുന്ന് വിശദീകരിക്കുക →",
        "chat_with_assistant": "💬 സഹായിയോട് ചാറ്റ് ചെയ്യുക",
        "chat_placeholder": "എന്തും ചോദിക്കൂ...",
        "add_family_member": "👨‍👩‍👧 കുടുംബാംഗത്തെ ചേർക്കുക",
        "family_email": "കുടുംബാംഗത്തിന്റെ ഇമെയിൽ",
        "phone_help": "രാജ്യ കോഡ് ഉൾപ്പെടുത്തുക, ഉദാ. +919876543210",
        "relationship": "ബന്ധം (ഉദാ. മകൻ, മകൾ)",
        "can_view_health": "ആരോഗ്യ രേഖകൾ കാണാം",
        "can_edit_reminders": "ഓർമ്മപ്പെടുത്തലുകൾ തിരുത്താം",
        "add_family_member_button": "കുടുംബാംഗത്തെ ചേർക്കുക →",
        "email_required": "ദയവായി ഇമെയിൽ വിലാസം നൽകുക.",
        "family_added": "✅ {email} ചേർത്തു",
        "members": "👥 അംഗങ്ങൾ",
        "no_family_members": "ഇനിയും കുടുംബാംഗങ്ങളെ ചേർത്തിട്ടില്ല.",
        "phone_numbers": "📞 ഫോൺ നമ്പറുകൾ",
        "emergency_response": "🚨 അടിയന്തര പ്രതികരണം",
        "emergency_warning": "യഥാർത്ഥ അടിയന്തരാവസ്ഥയിൽ മാത്രം ഇത് ഉപയോഗിക്കുക. ഇത് നിങ്ങളുടെ അടിയന്തര ബന്ധുക്കളെ ഉടൻ അറിയിക്കും.",
        "emergency_type": "അടിയന്തര തരം",
        "severity": "തീവ്രത",
        "activate_emergency": "🚨 അടിയന്തര പ്രോട്ടോക്കോൾ സജീവമാക്കുക",
        "reading_type.blood_pressure": "രക്തസമ്മർദ്ദം",
        "reading_type.glucose": "ഗ്ലൂക്കോസ്",
        "reading_type.temperature": "താപനില",
        "reading_type.heart_rate": "ഹൃദയമിടിപ്പ്",
        "reading_type.oxygen": "ഓക്സിജൻ",
        "reminder_type.medication": "മരുന്ന്",
        "reminder_type.appointment": "അപ്പോയിന്റ്മെന്റ്",
        "reminder_type.activity": "പ്രവർത്തനം",
        "reminder_type.hydration": "വെള്ളം കുടിക്കൽ",
        "schedule.daily": "ദിവസേന",
        "schedule.weekly": "ആഴ്ചതോറും",
        "schedule.once": "ഒരിക്കൽ",
        "emergency_type.general": "പൊതു",
        "emergency_type.fall": "വീഴ്ച",
        "emergency_type.medical": "മെഡിക്കൽ",
        "emergency_type.medication": "മരുന്ന്",
        "severity.high": "ഉയർന്ന",
        "severity.critical": "ഗുരുതരം",
    },
    "kn": {
        "app_title": "ಹಿರಿಯರ ಆರೈಕೆ ಸಹಾಯಕ",
        "app_tagline": "ಕರುಣೆಯ ಆರೈಕೆ, ಒಂದೊಂದು ಹೆಜ್ಜೆಯಲ್ಲಿ",
        "language": "ಭಾಷೆ",
        "localhost_warning": "ಆಪ್ localhost ನಲ್ಲಿ ನಡೆಯುತ್ತಿದೆ. deploy ಮಾಡಿದಾಗ API_BASE_URL ಅನ್ನು ನಿಮ್ಮ backend host ಗೆ ಸೆಟ್ ಮಾಡಿ.",
        "login_required": "👋 ಈ ವಿಭಾಗವನ್ನು ಬಳಸಲು ದಯವಿಟ್ಟು ಸೈನ್ ಇನ್ ಮಾಡಿ ಅಥವಾ ಖಾತೆ ರಚಿಸಿ.",
        "tab.account": "👤 ಖಾತೆ",
        "tab.health": "🩺 ಆರೋಗ್ಯ",
        "tab.reminders": "⏰ ನೆನಪಿಗಳು",
        "tab.chat": "💬 ಚಾಟ್",
        "tab.family": "👨‍👩‍👧 ಕುಟುಂಬ",
        "tab.emergency": "🚨 ತುರ್ತು",
        "sign_in": "ಸೈನ್ ಇನ್",
        "create_account": "ಖಾತೆ ರಚಿಸಿ",
        "email": "ಇಮೇಲ್",
        "password": "ಪಾಸ್‌ವರ್ಡ್",
        "sign_in_button": "ಸೈನ್ ಇನ್ ಮಾಡಿ →",
        "signed_in": "✅ ಯಶಸ್ವಿಯಾಗಿ ಸೈನ್ ಇನ್ ಆಗಿದೆ!",
        "first_name": "ಮೊದಲ ಹೆಸರು",
        "last_name": "ಕೊನೆಯ ಹೆಸರು",
        "date_of_birth": "ಜನ್ಮ ದಿನಾಂಕ",
        "phone_number": "ಫೋನ್ ಸಂಖ್ಯೆ",
        "create_account_button": "ಖಾತೆ ರಚಿಸಿ →",
        "account_created": "🎉 {name} ಗಾಗಿ ಖಾತೆ ರಚಿಸಲಾಗಿದೆ!",
        "sign_out": "ಸೈನ್ ಔಟ್",
        "add_health_reading": "🩺 ಆರೋಗ್ಯ ರೀಡಿಂಗ್ ಸೇರಿಸಿ",
        "reading_type": "ರೀಡಿಂಗ್ ಪ್ರಕಾರ",
        "primary_value": "ಮುಖ್ಯ ಮೌಲ್ಯ",
        "secondary_value": "ಎರಡನೇ ಮೌಲ್ಯ (ಇದ್ದರೆ)",
        "unit": "ಘಟಕ",
        "notes": "ಟಿಪ್ಪಣಿಗಳು",
        "save_reading": "ರೀಡಿಂಗ್ ಉಳಿಸಿ →",
        "reading_saved": "✅ ರೀಡಿಂಗ್ ಉಳಿಸಲಾಗಿದೆ — ಸ್ಥಿತಿ: {status}",
        "health_summary": "📊 ಆರೋಗ್ಯ ಸಾರಾಂಶ",
        "add_reminder": "⏰ ನೆನಪು ಸೇರಿಸಿ",
        "reminder_type": "ನೆನಪು ಪ್ರಕಾರ",
        "title": "ಶೀರ್ಷಿಕೆ",
        "description": "ವಿವರಣೆ",
        "schedule": "ವೇಳಾಪಟ್ಟಿ",
        "time": "ಸಮಯ",
        "create_reminder": "ನೆನಪು ರಚಿಸಿ →",
        "reminder_created": "✅ ನೆನಪು ರಚಿಸಲಾಗಿದೆ: {title}",
        "upcoming_reminders": "📋 ಮುಂಬರುವ ನೆನಪಿಗಳು",
        "medicine_information": "💊 ಔಷಧಿ ಮಾಹಿತಿ",
        "enter_medicine_name": "ಔಷಧಿಯ ಹೆಸರು ನಮೂದಿಸಿ",
        "explain_medicine": "ಈ ಔಷಧಿಯನ್ನು ವಿವರಿಸಿ →",
        "chat_with_assistant": "💬 ಸಹಾಯಕರೊಂದಿಗೆ ಚಾಟ್ ಮಾಡಿ",
        "chat_placeholder": "ಏನಾದರೂ ಕೇಳಿ...",
        "add_family_member": "👨‍👩‍👧 ಕುಟುಂಬ ಸದಸ್ಯರನ್ನು ಸೇರಿಸಿ",
        "family_email": "ಕುಟುಂಬ ಸದಸ್ಯರ ಇಮೇಲ್",
        "phone_help": "ದೇಶ ಕೋಡ್ ಸೇರಿಸಿ, ಉದಾ. +919876543210",
        "relationship": "ಸಂಬಂಧ (ಉದಾ. ಮಗ, ಮಗಳು)",
        "can_view_health": "ಆರೋಗ್ಯ ದಾಖಲೆಗಳನ್ನು ನೋಡಬಹುದು",
        "can_edit_reminders": "ನೆನಪಿಗಳನ್ನು ಸಂಪಾದಿಸಬಹುದು",
        "add_family_member_button": "ಕುಟುಂಬ ಸದಸ್ಯರನ್ನು ಸೇರಿಸಿ →",
        "email_required": "ದಯವಿಟ್ಟು ಇಮೇಲ್ ವಿಳಾಸವನ್ನು ನಮೂದಿಸಿ.",
        "family_added": "✅ {email} ಸೇರಿಸಲಾಗಿದೆ",
        "members": "👥 ಸದಸ್ಯರು",
        "no_family_members": "ಇನ್ನೂ ಕುಟುಂಬ ಸದಸ್ಯರನ್ನು ಸೇರಿಸಲಾಗಿಲ್ಲ.",
        "phone_numbers": "📞 ಫೋನ್ ಸಂಖ್ಯೆಗಳು",
        "emergency_response": "🚨 ತುರ್ತು ಪ್ರತಿಕ್ರಿಯೆ",
        "emergency_warning": "ನಿಜವಾದ ತುರ್ತು ಪರಿಸ್ಥಿತಿಯಲ್ಲಿ ಮಾತ್ರ ಇದನ್ನು ಬಳಸಿ. ಇದು ನಿಮ್ಮ ತುರ್ತು ಸಂಪರ್ಕಗಳಿಗೆ ತಕ್ಷಣ ಎಚ್ಚರಿಕೆ ಕಳುಹಿಸುತ್ತದೆ.",
        "emergency_type": "ತುರ್ತು ಪ್ರಕಾರ",
        "severity": "ತೀವ್ರತೆ",
        "activate_emergency": "🚨 ತುರ್ತು ಪ್ರೋಟೋಕಾಲ್ ಸಕ್ರಿಯಗೊಳಿಸಿ",
        "reading_type.blood_pressure": "ರಕ್ತದ ಒತ್ತಡ",
        "reading_type.glucose": "ಗ್ಲೂಕೋಸ್",
        "reading_type.temperature": "ತಾಪಮಾನ",
        "reading_type.heart_rate": "ಹೃದಯ ಬಡಿತ",
        "reading_type.oxygen": "ಆಮ್ಲಜನಕ",
        "reminder_type.medication": "ಔಷಧಿ",
        "reminder_type.appointment": "ಭೇಟಿ",
        "reminder_type.activity": "ಚಟುವಟಿಕೆ",
        "reminder_type.hydration": "ನೀರು ಕುಡಿಯುವುದು",
        "schedule.daily": "ಪ್ರತಿದಿನ",
        "schedule.weekly": "ವಾರಕ್ಕೊಮ್ಮೆ",
        "schedule.once": "ಒಮ್ಮೆ",
        "emergency_type.general": "ಸಾಮಾನ್ಯ",
        "emergency_type.fall": "ಬೀಳುವುದು",
        "emergency_type.medical": "ವೈದ್ಯಕೀಯ",
        "emergency_type.medication": "ಔಷಧಿ",
        "severity.high": "ಹೆಚ್ಚು",
        "severity.critical": "ಗಂಭೀರ",
    },
}


def t(key, **kwargs):
    language = st.session_state.get("language", "en")
    text = TRANSLATIONS.get(language, TRANSLATIONS["en"]).get(key, TRANSLATIONS["en"].get(key, key))
    return text.format(**kwargs) if kwargs else text


def translated_option(prefix):
    return lambda value: t(f"{prefix}.{value}")

st.set_page_config(
    page_title=t("app_title"),
    page_icon="🌿",
    layout="wide",
)

# ── Custom styles ────────────────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=Noto+Sans+Devanagari:wght@400;600;700;800&family=Noto+Sans+Telugu:wght@400;600;700;800&family=Noto+Sans+Tamil:wght@400;600;700;800&family=Noto+Sans+Malayalam:wght@400;600;700;800&family=Noto+Sans+Kannada:wght@400;600;700;800&display=swap" rel="stylesheet">

<style>
/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Nunito', 'Noto Sans Devanagari', 'Noto Sans Telugu', 'Noto Sans Tamil', 'Noto Sans Malayalam', 'Noto Sans Kannada', sans-serif !important;
    background-color: #FAF7F2 !important;
    color: #2C2C2C !important;
}

/* ── Header banner ── */
.eca-header {
    background: linear-gradient(135deg, #1B3A5C 0%, #2E6B8A 100%);
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 18px;
}
.eca-header h1 {
    font-family: 'Nunito', 'Noto Sans Devanagari', 'Noto Sans Telugu', 'Noto Sans Tamil', 'Noto Sans Malayalam', 'Noto Sans Kannada', sans-serif !important;
    color: #FAF7F2 !important;
    font-size: 2.2rem !important;
    margin: 0 !important;
    letter-spacing: 0;
}
.eca-header p {
    color: #E8D5B0 !important;
    margin: 4px 0 0 0 !important;
    font-size: 1rem;
    font-weight: 600;
}
.eca-icon {
    font-size: 3rem;
    line-height: 1;
}

/* ── Section headings ── */
h2, h3, .stSubheader {
    font-family: 'Nunito', 'Noto Sans Devanagari', 'Noto Sans Telugu', 'Noto Sans Tamil', 'Noto Sans Malayalam', 'Noto Sans Kannada', sans-serif !important;
    color: #1B3A5C !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #EDE8E0;
    border-radius: 12px;
    padding: 6px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Nunito', 'Noto Sans Devanagari', 'Noto Sans Telugu', 'Noto Sans Tamil', 'Noto Sans Malayalam', 'Noto Sans Kannada', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    color: #1B3A5C !important;
    border-radius: 8px !important;
    padding: 8px 20px !important;
    border: none !important;
    background: transparent !important;
}
.stTabs [aria-selected="true"] {
    background: #1B3A5C !important;
    color: #FAF7F2 !important;
}
.stTabs [data-baseweb="tab-highlight"] {
    display: none !important;
}

/* ── Buttons ── */
.stButton > button {
    font-family: 'Nunito', 'Noto Sans Devanagari', 'Noto Sans Telugu', 'Noto Sans Tamil', 'Noto Sans Malayalam', 'Noto Sans Kannada', sans-serif !important;
    font-weight: 700 !important;
    background: #E8A838 !important;
    color: #1B3A5C !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    font-size: 0.95rem !important;
    transition: background 0.2s ease, transform 0.1s ease;
    box-shadow: 0 2px 6px rgba(0,0,0,0.12);
}
.stButton > button:hover {
    background: #D4922A !important;
    transform: translateY(-1px);
}
.stButton > button[kind="primary"] {
    background: #C0392B !important;
    color: #FAF7F2 !important;
}
.stButton > button[kind="primary"]:hover {
    background: #A93226 !important;
}

/* ── Form submit buttons ── */
.stFormSubmitButton > button {
    font-family: 'Nunito', 'Noto Sans Devanagari', 'Noto Sans Telugu', 'Noto Sans Tamil', 'Noto Sans Malayalam', 'Noto Sans Kannada', sans-serif !important;
    font-weight: 700 !important;
    background: #3D8B8B !important;
    color: #FAF7F2 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    font-size: 0.95rem !important;
    transition: background 0.2s ease;
    box-shadow: 0 2px 6px rgba(0,0,0,0.12);
}
.stFormSubmitButton > button:hover {
    background: #2E6B6B !important;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input,
.stSelectbox > div > div {
    font-family: 'Nunito', 'Noto Sans Devanagari', 'Noto Sans Telugu', 'Noto Sans Tamil', 'Noto Sans Malayalam', 'Noto Sans Kannada', sans-serif !important;
    border-radius: 10px !important;
    border: 2px solid #D4C9BB !important;
    background: #FFFFFF !important;
    color: #2C2C2C !important;
    font-size: 0.95rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #3D8B8B !important;
    box-shadow: 0 0 0 3px rgba(61,139,139,0.15) !important;
}

/* ── Labels ── */
label, .stSelectbox label, .stTextInput label, .stNumberInput label {
    font-family: 'Nunito', 'Noto Sans Devanagari', 'Noto Sans Telugu', 'Noto Sans Tamil', 'Noto Sans Malayalam', 'Noto Sans Kannada', sans-serif !important;
    font-weight: 700 !important;
    color: #1B3A5C !important;
    font-size: 0.9rem !important;
}

/* ── Forms ── */
.stForm {
    background: #FFFFFF !important;
    border-radius: 14px !important;
    padding: 20px !important;
    border: 1px solid #E8DDD2 !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06) !important;
}

/* ── Alerts ── */
.stSuccess, [data-testid="stNotification"] {
    border-radius: 10px !important;
    font-family: 'Nunito', 'Noto Sans Devanagari', 'Noto Sans Telugu', 'Noto Sans Tamil', 'Noto Sans Malayalam', 'Noto Sans Kannada', sans-serif !important;
    font-weight: 600 !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #1B3A5C !important;
}
section[data-testid="stSidebar"] * {
    color: #FAF7F2 !important;
}

/* ── Dataframe ── */
.stDataFrame {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid #E8DDD2 !important;
}

/* ── Divider ── */
hr {
    border-color: #E8DDD2 !important;
    margin: 20px 0 !important;
}

/* ── Info / Warning boxes ── */
.stInfo, .stWarning, .stError {
    border-radius: 10px !important;
    font-family: 'Nunito', 'Noto Sans Devanagari', 'Noto Sans Telugu', 'Noto Sans Tamil', 'Noto Sans Malayalam', 'Noto Sans Kannada', sans-serif !important;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: #FFFFFF !important;
    border-radius: 12px !important;
    border: 1px solid #E8DDD2 !important;
    margin-bottom: 8px !important;
}
</style>
""", unsafe_allow_html=True)

# ── Top language switcher and banner ─────────────────────────────────────────
language_codes = list(LANGUAGES.keys())
current_language = st.session_state.get("language", "en")
selected_language = st.selectbox(
    t("language"),
    language_codes,
    index=language_codes.index(current_language),
    format_func=lambda code: LANGUAGES[code],
)
if selected_language != current_language:
    st.session_state.language = selected_language
    st.rerun()

st.markdown(f"""
<div class="eca-header">
    <div class="eca-icon">🌿</div>
    <div>
        <h1>{t("app_title")}</h1>
        <p>{t("app_tagline")}</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ── API helper ───────────────────────────────────────────────────────────────
def api_request(method, path, *, json=None, params=None, auth=True):
    headers = {}
    if auth and st.session_state.get("token"):
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    try:
        response = requests.request(
            method,
            f"{API_BASE_URL}{path}",
            json=json,
            params=params,
            headers=headers,
            timeout=10,
        )
    except requests.RequestException as exc:
        return None, f"Could not reach API: {exc}"

    if response.ok:
        if response.content:
            return response.json(), None
        return {}, None
    try:
        detail = response.json().get("detail", response.text)
    except ValueError:
        detail = response.text
    return None, f"{response.status_code}: {detail}"


def require_login():
    if st.session_state.get("token"):
        return True
    st.info(t("login_required"))
    return False


# ── Sections ─────────────────────────────────────────────────────────────────
def render_auth():
    left, right = st.columns(2)

    with left:
        st.subheader(t("sign_in"))
        with st.form("login_form"):
            email = st.text_input(t("email"), key="login_email")
            password = st.text_input(t("password"), type="password", key="login_password")
            submitted = st.form_submit_button(t("sign_in_button"))
            if submitted:
                data, error = api_request(
                    "POST",
                    "/api/v1/auth/login",
                    params={"email": email, "password": password},
                    auth=False,
                )
                if error:
                    st.error(error)
                else:
                    st.session_state.token = data["access_token"]
                    st.success(t("signed_in"))
                    st.rerun()

    with right:
        st.subheader(t("create_account"))
        with st.form("register_form"):
            first_name = st.text_input(t("first_name"))
            last_name = st.text_input(t("last_name"))
            register_email = st.text_input(t("email"), key="register_email")
            register_password = st.text_input(t("password"), type="password", key="register_password")
            dob = st.date_input(
                t("date_of_birth"),
                value=date(1960, 1, 1),
                min_value=date(1900, 1, 1),
                max_value=date(2000, 12, 31),
            )
            phone = st.text_input(t("phone_number"), placeholder="+91XXXXXXXXXX")
            submitted = st.form_submit_button(t("create_account_button"))
            if submitted:
                payload = {
                    "email": register_email,
                    "password": register_password,
                    "first_name": first_name,
                    "last_name": last_name,
                    "date_of_birth": dob.isoformat(),
                    "phone_number": phone or None,
                }
                data, error = api_request("POST", "/api/v1/auth/register", json=payload, auth=False)
                if error:
                    st.error(error)
                else:
                    st.success(t("account_created", name=f"{data['first_name']} {data['last_name']}"))
                    login_data, login_error = api_request(
                        "POST",
                        "/api/v1/auth/login",
                        params={"email": register_email, "password": register_password},
                        auth=False,
                    )
                    if login_error:
                        st.warning(login_error)
                    else:
                        st.session_state.token = login_data["access_token"]
                        st.rerun()

    if st.session_state.get("token"):
        st.divider()
        if st.button(t("sign_out")):
            st.session_state.pop("token", None)
            st.rerun()


def render_health():
    if not require_login():
        return

    left, right = st.columns([1, 1])

    with left:
        st.subheader(t("add_health_reading"))
        with st.form("health_form"):
            reading_type = st.selectbox(
                t("reading_type"),
                ["blood_pressure", "glucose", "temperature", "heart_rate", "oxygen"],
                format_func=translated_option("reading_type"),
            )
            value = st.number_input(t("primary_value"), min_value=0.0, step=1.0)
            secondary_value = st.number_input(t("secondary_value"), min_value=0.0, step=1.0)
            unit = st.text_input(t("unit"), value="mmHg" if reading_type == "blood_pressure" else "")
            notes = st.text_area(t("notes"))
            submitted = st.form_submit_button(t("save_reading"))
            if submitted:
                payload = {
                    "reading_type": reading_type,
                    "value": value,
                    "secondary_value": secondary_value if secondary_value else None,
                    "unit": unit,
                    "notes": notes or None,
                }
                data, error = api_request("POST", "/api/v1/health/readings", json=payload)
                if error:
                    st.error(error)
                else:
                    st.success(t("reading_saved", status=data.get("status")))

    with right:
        st.subheader(t("health_summary"))
        data, error = api_request("GET", "/api/v1/health/summary")
        if error:
            st.error(error)
        else:
            st.json(data)


def render_reminders():
    if not require_login():
        return

    left, right = st.columns([1, 1])

    with left:
        st.subheader(t("add_reminder"))
        with st.form("reminder_form"):
            reminder_type = st.selectbox(
                t("reminder_type"),
                ["medication", "appointment", "activity", "hydration"],
                format_func=translated_option("reminder_type"),
            )
            title = st.text_input(t("title"))
            description = st.text_area(t("description"))
            schedule_type = st.selectbox(
                t("schedule"),
                ["daily", "weekly", "once"],
                format_func=translated_option("schedule"),
            )
            schedule_time = st.time_input(t("time"))
            submitted = st.form_submit_button(t("create_reminder"))
            if submitted:
                payload = {
                    "reminder_type": reminder_type,
                    "title": title,
                    "description": description or None,
                    "schedule_type": schedule_type,
                    "schedule_time": schedule_time.strftime("%H:%M"),
                    "days_of_week": None,
                    "reminder_minutes_before": 10,
                }
                data, error = api_request("POST", "/api/v1/reminders/", json=payload)
                if error:
                    st.error(error)
                else:
                    st.success(t("reminder_created", title=data.get("title")))

    with right:
        st.subheader(t("upcoming_reminders"))
        data, error = api_request("GET", "/api/v1/reminders/upcoming")
        if error:
            st.error(error)
        else:
            st.dataframe(data.get("upcoming", []), use_container_width=True)


def render_chat():
    if not require_login():
        return

    st.subheader(t("medicine_information"))
    with st.form("medicine_chat_form"):
        medicine_name = st.text_input(t("enter_medicine_name"))
        explain_medicine = st.form_submit_button(t("explain_medicine"))
        if explain_medicine and medicine_name.strip():
            data, error = api_request(
                "POST",
                "/api/v1/chat/message",
                json={"message": f"Medicine name: {medicine_name}", "context": "medicine"},
            )
            if error:
                st.error(error)
            else:
                st.chat_message("user").write(medicine_name)
                st.chat_message("assistant").write(data["response"])

    st.divider()
    st.subheader(t("chat_with_assistant"))
    message = st.chat_input(t("chat_placeholder"))
    if message:
        data, error = api_request(
            "POST",
            "/api/v1/chat/message",
            json={"message": message, "context": "general"},
        )
        if error:
            st.error(error)
        else:
            st.chat_message("user").write(message)
            st.chat_message("assistant").write(data["response"])

    data, error = api_request("GET", "/api/v1/chat/history")
    if not error and data:
        for item in data.get("messages", []):
            st.chat_message(item["role"]).write(item["content"])


def render_family():
    if not require_login():
        return

    if "family_phones" not in st.session_state:
        st.session_state.family_phones = {}

    left, right = st.columns([1, 1])

    with left:
        st.subheader(t("add_family_member"))
        with st.form("family_form"):
            family_email = st.text_input(t("family_email"))
            family_phone = st.text_input(
                t("phone_number"),
                placeholder="+91XXXXXXXXXX",
                help=t("phone_help"),
            )
            relationship = st.text_input(t("relationship"))
            can_view_health = st.checkbox(t("can_view_health"), value=True)
            can_edit_reminders = st.checkbox(t("can_edit_reminders"))
            submitted = st.form_submit_button(t("add_family_member_button"))
            if submitted:
                if not family_email:
                    st.warning(t("email_required"))
                else:
                    payload = {
                        "family_email": family_email,
                        "relationship": relationship,
                        "can_view_health": can_view_health,
                        "can_edit_reminders": can_edit_reminders,
                    }
                    data, error = api_request("POST", "/api/v1/family/members", json=payload)
                    if error:
                        st.error(error)
                    else:
                        if family_phone:
                            st.session_state.family_phones[family_email] = family_phone
                        st.success(t("family_added", email=data.get("family_email")))

    with right:
        st.subheader(t("members"))
        data, error = api_request("GET", "/api/v1/family/members")
        if error:
            st.error(error)
        else:
            members = data.get("members", [])
            if members:
                for m in members:
                    email = m.get("family_email", "")
                    m["phone_number"] = st.session_state.family_phones.get(email, "—")
                st.dataframe(members, use_container_width=True)
            else:
                st.info(t("no_family_members"))

        if st.session_state.family_phones:
            st.divider()
            st.subheader(t("phone_numbers"))
            for email, phone in st.session_state.family_phones.items():
                st.markdown(f"**{email}** &nbsp;→&nbsp; `{phone}`")


def render_emergency():
    if not require_login():
        return

    st.subheader(t("emergency_response"))
    st.markdown(
        "<p style='color:#C0392B; font-weight:700; font-size:1rem;'>"
        f"{t('emergency_warning')}"
        "</p>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        emergency_type = st.selectbox(
            t("emergency_type"),
            ["general", "fall", "medical", "medication"],
            format_func=translated_option("emergency_type"),
        )
    with col2:
        severity = st.selectbox(t("severity"), ["high", "critical"], format_func=translated_option("severity"))

    if st.button(t("activate_emergency"), type="primary"):
        data, error = api_request(
            "POST",
            "/api/v1/emergency/activate",
            json={"type": emergency_type, "severity": severity},
        )
        if error:
            st.error(error)
        else:
            st.warning(f"⚠️ {data.get('message')}")
            st.json(data)


# ── App layout ────────────────────────────────────────────────────────────────
tabs = st.tabs([t("tab.account"), t("tab.health"), t("tab.reminders"), t("tab.chat"), t("tab.family"), t("tab.emergency")])

with tabs[0]:
    render_auth()
with tabs[1]:
    render_health()
with tabs[2]:
    render_reminders()
with tabs[3]:
    render_chat()
with tabs[4]:
    render_family()
with tabs[5]:
    render_emergency()

