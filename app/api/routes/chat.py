from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import uuid
import re

from app.database.db import get_db
from app.models.models import User, ChatMessage
from app.middleware.auth import get_current_user
from app.schemas.schemas import ChatMessageCreate, ChatMessageResponse

router = APIRouter()

MEDICINE_INFO = {
    "paracetamol": {
        "name": "Paracetamol / Acetaminophen",
        "aliases": ["acetaminophen", "dolo", "calpol", "crocin", "tylenol"],
        "uses": "pain relief and fever reduction.",
        "how_taken": "usually taken only as directed on the label or prescription, with careful attention to the total daily dose.",
        "side_effects": "usually mild when taken correctly; overdose can seriously damage the liver.",
        "precautions": "avoid taking multiple cold/flu or pain products that also contain paracetamol/acetaminophen. People with liver disease or heavy alcohol use should ask a clinician before using it.",
        "questions": [
            "What is the correct dose and maximum daily limit for this person?",
            "Is it already included in another medicine being taken?",
            "How many days is it safe to use before getting checked?",
        ],
    },
    "ibuprofen": {
        "name": "Ibuprofen",
        "aliases": ["brufen", "advil", "motrin"],
        "uses": "pain, fever, and inflammation such as body aches, joint pain, or dental pain.",
        "how_taken": "usually taken with food or milk to reduce stomach irritation, as directed by a clinician or label.",
        "side_effects": "stomach pain, acidity, nausea, raised blood pressure, kidney strain, or bleeding risk in some people.",
        "precautions": "avoid or ask a doctor first if there is kidney disease, stomach ulcer/bleeding, blood thinners, uncontrolled blood pressure, heart disease, or late pregnancy.",
        "questions": [
            "Is this safe with my blood pressure, kidney function, stomach history, and other medicines?",
            "Should I avoid it if I take aspirin or blood thinners?",
            "What warning symptoms mean I should stop and call a doctor?",
        ],
    },
    "amoxicillin": {
        "name": "Amoxicillin",
        "aliases": ["amoxil"],
        "uses": "a prescription antibiotic used for certain bacterial infections.",
        "how_taken": "taken exactly as prescribed; the full course is usually important unless the prescriber says otherwise.",
        "side_effects": "diarrhea, nausea, rash, yeast infection, or allergic reaction.",
        "precautions": "do not use leftover antibiotics or share them. Tell the doctor about penicillin allergy, kidney disease, or severe diarrhea.",
        "questions": [
            "What infection is this treating and how many days should it be taken?",
            "What should I do if a dose is missed?",
            "What allergy symptoms require urgent help?",
        ],
    },
    "azithromycin": {
        "name": "Azithromycin",
        "aliases": ["azee", "zithromax"],
        "uses": "a prescription antibiotic used for some bacterial respiratory, throat, skin, and other infections.",
        "how_taken": "taken only as prescribed, often once daily for a short course.",
        "side_effects": "nausea, diarrhea, stomach pain, headache, or rarely heart rhythm problems.",
        "precautions": "tell the clinician about heart rhythm problems, liver disease, low potassium/magnesium, or medicines that affect heart rhythm.",
        "questions": [
            "Is this definitely needed for a bacterial infection?",
            "Should it be taken before or after food?",
            "Does it interact with any heart or allergy medicines?",
        ],
    },
    "metformin": {
        "name": "Metformin",
        "aliases": ["glycomet", "glucophage"],
        "uses": "type 2 diabetes management by helping lower blood sugar and improve insulin sensitivity.",
        "how_taken": "often taken with meals to reduce stomach upset, exactly as prescribed.",
        "side_effects": "nausea, loose stools, stomach discomfort, metallic taste, and rarely lactic acidosis in high-risk situations.",
        "precautions": "kidney function matters. Ask about temporary stopping rules during severe dehydration, major illness, surgery, or contrast scans.",
        "questions": [
            "What blood sugar targets should I follow?",
            "How often should kidney function and B12 be checked?",
            "What should I do during vomiting, diarrhea, or poor food intake?",
        ],
    },
    "amlodipine": {
        "name": "Amlodipine",
        "aliases": ["amlong", "norvasc"],
        "uses": "high blood pressure and some types of chest pain called angina.",
        "how_taken": "usually taken once daily at the same time, as prescribed.",
        "side_effects": "ankle swelling, flushing, headache, dizziness, tiredness, or palpitations.",
        "precautions": "do not stop suddenly without medical advice. Report severe dizziness, fainting, or significant swelling.",
        "questions": [
            "What blood pressure range is expected for me?",
            "Should I track home blood pressure readings?",
            "What should I do if ankle swelling appears?",
        ],
    },
    "losartan": {
        "name": "Losartan",
        "aliases": ["losar", "cozaar"],
        "uses": "high blood pressure, kidney protection in some people with diabetes, and some heart conditions.",
        "how_taken": "usually taken once daily as prescribed.",
        "side_effects": "dizziness, raised potassium, kidney function changes, or fatigue.",
        "precautions": "kidney function and potassium may need monitoring. Avoid in pregnancy unless a specialist specifically advises otherwise.",
        "questions": [
            "When should potassium and kidney function be checked?",
            "Should I avoid potassium supplements or salt substitutes?",
            "What blood pressure readings should prompt a call?",
        ],
    },
    "atorvastatin": {
        "name": "Atorvastatin",
        "aliases": ["atorva", "lipitor"],
        "uses": "lowering LDL cholesterol and reducing heart attack/stroke risk in selected patients.",
        "how_taken": "usually taken once daily as prescribed.",
        "side_effects": "muscle aches, mild stomach upset, headache, or liver enzyme changes in some people.",
        "precautions": "report severe muscle pain, dark urine, unusual weakness, or yellowing of eyes/skin. Avoid pregnancy unless specifically advised.",
        "questions": [
            "What is my LDL goal and heart-risk category?",
            "Should liver tests be checked?",
            "Does this interact with my other medicines?",
        ],
    },
    "aspirin": {
        "name": "Aspirin",
        "aliases": ["ecosprin", "disprin"],
        "uses": "pain/fever at some doses and prevention of blood clots in selected heart or stroke patients at low doses.",
        "how_taken": "taken only as directed; low-dose aspirin for heart/stroke prevention should be clinician-directed.",
        "side_effects": "stomach irritation, acidity, bruising, bleeding, or allergy/wheezing in some people.",
        "precautions": "ask before use if there is ulcer/bleeding history, blood thinners, kidney disease, asthma sensitivity, or upcoming surgery.",
        "questions": [
            "Am I taking this for pain or for heart/stroke prevention?",
            "Is my bleeding risk too high?",
            "Should it be taken with food or stomach protection?",
        ],
    },
    "omeprazole": {
        "name": "Omeprazole",
        "aliases": ["omez", "prilosec"],
        "uses": "acid reflux, gastritis, ulcers, and stomach protection in selected patients.",
        "how_taken": "often taken before food, commonly before breakfast, as directed.",
        "side_effects": "headache, nausea, gas, constipation, diarrhea, or low magnesium/B12 risk with long-term use.",
        "precautions": "persistent vomiting, weight loss, black stools, trouble swallowing, or chest pain needs medical review.",
        "questions": [
            "How long should I take this?",
            "Do I need tests if acidity keeps returning?",
            "Could lifestyle changes reduce symptoms?",
        ],
    },
    "pantoprazole": {
        "name": "Pantoprazole",
        "aliases": ["pan", "pantocid", "protonix"],
        "uses": "acid reflux, gastritis, ulcers, and stomach protection in selected patients.",
        "how_taken": "often taken before food, commonly before breakfast, as directed.",
        "side_effects": "headache, nausea, gas, constipation, diarrhea, or low magnesium/B12 risk with long-term use.",
        "precautions": "persistent vomiting, weight loss, black stools, trouble swallowing, or chest pain needs medical review.",
        "questions": [
            "How long should I take this?",
            "Do I need it daily or only for a short course?",
            "Could it interact with my other medicines?",
        ],
    },
    "cetirizine": {
        "name": "Cetirizine",
        "aliases": ["zyrtec", "cetzine"],
        "uses": "allergy symptoms such as sneezing, runny nose, itching, and hives.",
        "how_taken": "usually taken once daily as directed.",
        "side_effects": "sleepiness, dry mouth, tiredness, or dizziness.",
        "precautions": "avoid driving or alcohol if it causes drowsiness. Dose adjustment may be needed in kidney disease.",
        "questions": [
            "Will this make me sleepy?",
            "Is it safe with my kidney function and other medicines?",
            "When should allergy symptoms be checked by a doctor?",
        ],
    },
    "levothyroxine": {
        "name": "Levothyroxine",
        "aliases": ["thyronorm", "eltroxin", "synthroid"],
        "uses": "low thyroid hormone levels, also called hypothyroidism.",
        "how_taken": "usually taken on an empty stomach with water, separated from calcium, iron, and some antacids as advised.",
        "side_effects": "too high a dose can cause palpitations, sweating, weight loss, anxiety, or shakiness; too low may leave hypothyroid symptoms.",
        "precautions": "dose should be guided by TSH/T4 blood tests and clinician advice.",
        "questions": [
            "When should TSH be rechecked?",
            "How far apart should I take calcium, iron, or antacids?",
            "What symptoms suggest the dose may be too high or too low?",
        ],
    },
    "insulin": {
        "name": "Insulin",
        "aliases": ["human insulin", "glargine", "lispro", "aspart"],
        "uses": "diabetes treatment by lowering blood sugar.",
        "how_taken": "given by injection exactly as prescribed; timing depends on the insulin type and meals.",
        "side_effects": "low blood sugar, weight gain, injection-site irritation, or rarely allergic reaction.",
        "precautions": "know the signs of low sugar: sweating, shaking, hunger, confusion, weakness, or fainting. Keep a quick sugar source available if advised.",
        "questions": [
            "What type of insulin is this and when should it be taken?",
            "What should I do if I skip a meal or sugar is low?",
            "How should it be stored and rotated at injection sites?",
        ],
    },
}

@router.post("/message", response_model=ChatMessageResponse)
async def send_chat_message(
    chat_data: ChatMessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send message to companion"""
    # Store user message
    user_message = ChatMessage(
        user_id=current_user.id,
        conversation_id=uuid.uuid4(),
        role="user",
        content=chat_data.message
    )
    db.add(user_message)
    db.commit()

    # Generate response (simplified - would use Claude API in production)
    response_text = generate_companion_response(chat_data.message)
    emotional_tone = detect_emotional_tone(chat_data.message)

    # Store assistant message
    assistant_message = ChatMessage(
        user_id=current_user.id,
        conversation_id=user_message.conversation_id,
        role="assistant",
        content=response_text,
        emotional_tone=emotional_tone
    )
    db.add(assistant_message)
    db.commit()

    return {
        "response": response_text,
        "confidence": 0.85,
        "emotional_tone": emotional_tone
    }

@router.get("/history")
async def get_chat_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get chat history"""
    messages = db.query(ChatMessage).filter(
        ChatMessage.user_id == current_user.id
    ).order_by(ChatMessage.created_at.desc()).limit(50).all()

    return {
        "messages": [
            {
                "role": m.role,
                "content": m.content,
                "created_at": m.created_at.isoformat()
            }
            for m in reversed(messages)
        ],
        "count": len(messages)
    }

def generate_companion_response(user_message: str) -> str:
    """Generate a safe health-focused companion response."""
    lower_msg = user_message.lower().strip()

    emergency_terms = [
        "chest pain",
        "can't breathe",
        "cannot breathe",
        "shortness of breath",
        "stroke",
        "face drooping",
        "arm weakness",
        "slurred speech",
        "severe bleeding",
        "unconscious",
        "fainted",
        "suicidal",
        "kill myself",
    ]
    if any(term in lower_msg for term in emergency_terms):
        return (
            "This could be urgent. Please call local emergency services now, or use the Emergency section in this app. "
            "If possible, stay seated or lying down and ask someone nearby to stay with you."
        )

    medicine_name = extract_medicine_name(user_message)
    if medicine_name:
        return generate_medicine_explanation(medicine_name)

    if is_medical_report_message(user_message):
        return generate_report_explanation(user_message)

    health_topics = [
        (
            ["blood pressure", "bp", "hypertension"],
            "For blood pressure, sit quietly for 5 minutes, keep your arm supported at heart level, and take two readings a minute apart. "
            "A single high reading can happen from stress, caffeine, pain, or activity. If readings are repeatedly high, share them with your healthcare provider. "
            "If you have very high readings with chest pain, trouble breathing, weakness, confusion, or severe headache, seek urgent care."
        ),
        (
            ["blood sugar", "glucose", "diabetes", "sugar level"],
            "For blood sugar, follow the target range your clinician gave you, because goals vary by age, medicines, meals, and health history. "
            "Track when the reading was taken, such as fasting or after food. If you feel shaky, sweaty, confused, very thirsty, very weak, or unusually drowsy, contact a clinician promptly."
        ),
        (
            ["fever", "temperature", "chills"],
            "For fever, drink fluids, rest, and keep a note of the temperature and symptoms. In older adults, infection can sometimes show up as confusion, weakness, falls, or poor appetite even without a high fever. "
            "Seek medical advice if symptoms are worsening, fever persists, breathing is difficult, or there is confusion."
        ),
        (
            ["medicine", "medication", "tablet", "pill", "dose", "dosage"],
            "For medication questions, do not change the dose or stop a prescribed medicine without checking with your doctor or pharmacist. "
            "Keep a medication list with names, doses, times, and allergies. If you may have taken too much, mixed medicines by mistake, or have swelling, rash, fainting, or breathing trouble, seek urgent help."
        ),
        (
            ["diet", "food", "nutrition", "eat"],
            "A good everyday diet usually means regular meals with vegetables, fruits, protein, whole grains, and enough fluids. "
            "For conditions like diabetes, kidney disease, heart failure, swallowing trouble, or major weight loss, diet advice should be personalized by a clinician or dietitian."
        ),
        (
            ["exercise", "walk", "walking", "activity", "physio"],
            "Gentle movement can help strength, balance, sleep, mood, and blood sugar. Start small, such as short walks or chair exercises, and increase gradually. "
            "Stop and seek advice if exercise causes chest pain, severe breathlessness, dizziness, or new pain."
        ),
        (
            ["sleep", "insomnia", "can't sleep", "cannot sleep"],
            "For sleep, keep a steady wake time, limit late caffeine, get daylight exposure, and wind down with a calm routine. "
            "Tell a clinician if sleep problems are new, severe, linked with pain or breathing trouble, or causing daytime confusion or falls."
        ),
        (
            ["water", "hydration", "dehydrated", "dehydration"],
            "For hydration, sip fluids through the day and watch for dark urine, dizziness, dry mouth, constipation, or unusual tiredness. "
            "Some heart, kidney, or liver conditions require fluid limits, so follow your clinician's instructions if you have one."
        ),
        (
            ["fall", "fell", "dizzy", "balance"],
            "After a fall, check for head injury, severe pain, bleeding, confusion, weakness, or trouble walking. If any are present, seek urgent care. "
            "For prevention, review medicines, improve lighting, remove trip hazards, use proper footwear, and consider balance exercises or a mobility aid assessment."
        ),
        (
            ["pain", "ache", "back pain", "joint pain"],
            "For pain, note where it is, when it started, what worsens it, and whether there is swelling, fever, weakness, numbness, or injury. "
            "Sudden severe pain, chest pain, new weakness, or pain after a fall should be checked urgently."
        ),
        (
            ["cold", "cough", "flu", "sore throat"],
            "For cough or cold symptoms, rest, fluids, and monitoring are helpful. Watch for breathing trouble, chest pain, blue lips, confusion, dehydration, or symptoms that worsen instead of improving. "
            "Older adults should contact a clinician early if symptoms are significant or they have chronic heart, lung, or immune conditions."
        ),
        (
            ["sad", "lonely", "depressed", "anxious", "worried", "stress"],
            "I am sorry you are feeling this way. Talking to someone you trust can help, and small steps like a short walk, regular meals, and a routine can make the day feel steadier. "
            "If you feel unsafe, hopeless, or might hurt yourself, please contact emergency services or a crisis helpline right now."
        ),
    ]

    for keywords, response in health_topics:
        if any(keyword in lower_msg for keyword in keywords):
            return f"{response} I can share general health information, but I cannot diagnose or replace your doctor."

    if "joke" in lower_msg:
        return "A little laughter can help the day feel lighter, but I am best used here for health questions, reminders, and support. What health question can I help with?"
    if "reminder" in lower_msg:
        return "You can create medication, appointment, activity, or hydration reminders in the Reminders section. For medicine timing, follow your prescription label or ask your pharmacist."
    if "help" in lower_msg or "how do i" in lower_msg:
        return "I can help with general health questions about symptoms, vitals, medicines, diet, exercise, sleep, hydration, falls, and when to seek care. What would you like to know?"

    return (
        "Enter a medicine name and I can explain what it is commonly used for, important precautions, common side effects, and what to ask your doctor or pharmacist. "
        "For example: `Medicine name: metformin` or `What is amlodipine used for?` "
        "If this is urgent or involves chest pain, trouble breathing, stroke signs, fainting, severe bleeding, or thoughts of self-harm, seek emergency help now."
    )

def extract_medicine_name(message: str) -> str:
    """Extract a medicine name from the user's message."""
    clean_message = message.strip()
    lower_message = clean_message.lower()
    patterns = [
        r"medicine\s+name\s*:\s*([a-zA-Z0-9][a-zA-Z0-9 .+\-/]*)",
        r"medication\s+name\s*:\s*([a-zA-Z0-9][a-zA-Z0-9 .+\-/]*)",
        r"drug\s+name\s*:\s*([a-zA-Z0-9][a-zA-Z0-9 .+\-/]*)",
        r"what\s+is\s+([a-zA-Z0-9][a-zA-Z0-9 .+\-/]*)\s+used\s+for",
        r"explain\s+([a-zA-Z0-9][a-zA-Z0-9 .+\-/]*)",
        r"tell\s+me\s+about\s+([a-zA-Z0-9][a-zA-Z0-9 .+\-/]*)",
    ]
    for pattern in patterns:
        match = re.search(pattern, lower_message)
        if match:
            return normalize_medicine_name(match.group(1))

    known_names = set(MEDICINE_INFO)
    known_names.update(alias for item in MEDICINE_INFO.values() for alias in item.get("aliases", []))
    for name in sorted(known_names, key=len, reverse=True):
        if re.search(rf"\b{re.escape(name)}\b", lower_message):
            return normalize_medicine_name(name)

    if len(clean_message.split()) <= 4 and not any(char.isdigit() for char in clean_message):
        non_medicine_words = {"hi", "hello", "help", "thanks", "thank you", "ok", "yes", "no"}
        if lower_message not in non_medicine_words:
            return normalize_medicine_name(clean_message)

    return ""

def normalize_medicine_name(name: str) -> str:
    """Normalize user-entered medicine names."""
    cleaned = re.sub(r"\s+", " ", name).strip(" .,:;!?").lower()
    cleanup_words = ["tablet", "capsule", "syrup", "injection", "mg", "mcg", "ml"]
    parts = [part for part in cleaned.split() if part not in cleanup_words and not part.isdigit()]
    return " ".join(parts) if parts else cleaned

def generate_medicine_explanation(medicine_name: str) -> str:
    """Explain common medicine uses and precautions."""
    info = get_medicine_info(medicine_name)
    display_name = info.get("name", medicine_name.title())

    if not info.get("known"):
        return (
            f"I do not have reliable local details for `{display_name}` yet.\n"
            "Please check the spelling or enter the generic name printed under the brand name on the strip/bottle.\n"
            "What I can still help with:\n"
            "- Tell me the generic name, strength, and why it was prescribed.\n"
            "- Share age, known conditions, allergies, pregnancy status if relevant, and current medicines.\n"
            "- Ask your doctor or pharmacist what it is for, when to take it, what side effects to watch for, and whether it interacts with your other medicines.\n"
            "Do not start, stop, or change this medicine based only on this chat."
        )

    response_parts = [
        f"{display_name}",
        f"What it is commonly used for: {info['uses']}",
        f"How it is usually taken: {info['how_taken']}",
        f"Common side effects: {info['side_effects']}",
        f"Important precautions: {info['precautions']}",
        "Questions to ask your doctor or pharmacist:",
    ]
    response_parts.extend(f"- {question}" for question in info["questions"])
    response_parts.append(
        "Safety note: this is general medicine information, not a prescription. Follow the label and your clinician's advice. Seek urgent help for severe allergy symptoms, trouble breathing, fainting, severe bleeding, chest pain, severe confusion, or very unusual weakness."
    )
    return "\n".join(response_parts)

def get_medicine_info(medicine_name: str) -> dict:
    """Return medicine info by generic name or alias."""
    normalized_name = normalize_medicine_name(medicine_name)
    if normalized_name in MEDICINE_INFO:
        return {"known": True, **MEDICINE_INFO[normalized_name]}

    for generic_name, info in MEDICINE_INFO.items():
        if normalized_name in info.get("aliases", []):
            return {"known": True, **info, "name": info.get("name", generic_name.title())}

    return {"known": False, "name": medicine_name.title()}

def is_medical_report_message(message: str) -> bool:
    """Detect pasted reports or report explanation requests."""
    lower_msg = message.lower()
    report_markers = [
        "medical report",
        "lab report",
        "blood report",
        "test report",
        "explain report",
        "reference range",
        "normal range",
        "abnormal",
        "impression",
        "findings",
    ]
    lab_terms = [
        "hemoglobin",
        "hb",
        "wbc",
        "rbc",
        "platelet",
        "glucose",
        "hba1c",
        "cholesterol",
        "triglycerides",
        "creatinine",
        "egfr",
        "urea",
        "sodium",
        "potassium",
        "tsh",
        "t3",
        "t4",
        "alt",
        "ast",
        "bilirubin",
        "vitamin d",
        "b12",
        "urine",
    ]
    term_count = sum(1 for term in lab_terms if term in lower_msg)
    has_numbers = bool(re.search(r"\d", message))
    return any(marker in lower_msg for marker in report_markers) or (term_count >= 2 and has_numbers)

def generate_report_explanation(report_text: str) -> str:
    """Explain medical report text, ask follow-up questions, and suggest safe next steps."""
    findings = extract_report_findings(report_text)

    response_parts = [
        "I can help explain this report in plain language, but I cannot diagnose from a report alone. Lab ranges can differ by lab, age, sex, pregnancy status, medicines, and existing conditions.",
    ]

    if findings:
        response_parts.append("What I noticed:")
        response_parts.extend(f"- {finding}" for finding in findings[:8])
    else:
        response_parts.append(
            "I could not reliably pick out specific values. Please paste the test name, result, unit, and reference range, or include a clear line such as `Hemoglobin 10.2 g/dL, range 12-16`."
        )

    response_parts.append("Questions to answer so I can explain it better:")
    response_parts.extend(
        [
            "- What was the reason for this test: routine checkup, symptoms, follow-up, or emergency?",
            "- Which values are marked High, Low, H, L, abnormal, or outside the reference range?",
            "- What are the person's age, sex, main symptoms, current medicines, and known conditions like diabetes, kidney disease, thyroid disease, or heart disease?",
            "- Is this result new, or has it been abnormal in previous reports too?",
        ]
    )

    response_parts.append("Safe next steps:")
    response_parts.extend(build_report_next_steps(report_text))
    response_parts.append(
        "Seek urgent care now if the report is linked with chest pain, trouble breathing, stroke symptoms, fainting, severe weakness, confusion, severe bleeding, very high fever, or very low/high sugar symptoms."
    )

    return "\n".join(response_parts)

def extract_report_findings(report_text: str) -> list[str]:
    """Extract recognizable tests and explain what they usually relate to."""
    lower_report = report_text.lower()
    test_explanations = [
        (["hemoglobin", " hb "], "Hemoglobin relates to anemia or oxygen-carrying capacity. Low values can be linked with iron/B12 deficiency, blood loss, kidney disease, or chronic illness."),
        (["wbc", "white blood"], "WBC relates to infection, inflammation, stress response, or immune/bone marrow issues."),
        (["platelet"], "Platelets help blood clot. Low or high values may need review, especially with bleeding, bruising, clot history, or infection."),
        (["glucose", "blood sugar"], "Glucose reflects blood sugar at the time of testing. Timing matters: fasting, random, or after food."),
        (["hba1c", "a1c"], "HbA1c reflects average blood sugar over roughly the past few months and is often used for diabetes monitoring."),
        (["cholesterol", "ldl", "hdl", "triglyceride"], "Cholesterol tests estimate heart and blood-vessel risk. The overall risk depends on age, blood pressure, diabetes, smoking, and history."),
        (["creatinine", "egfr", "urea"], "Creatinine, eGFR, and urea relate to kidney function and hydration status."),
        (["sodium", "potassium", "electrolyte"], "Electrolytes affect hydration, heart rhythm, muscles, nerves, and medicines such as diuretics or blood pressure tablets."),
        (["tsh", "thyroid", "t3", "t4"], "Thyroid tests relate to thyroid activity, which can affect weight, energy, pulse, bowels, mood, and temperature tolerance."),
        (["alt", "ast", "bilirubin", "sgpt", "sgot"], "Liver tests can change with liver inflammation, alcohol, fatty liver, infections, bile flow problems, or medicines."),
        (["vitamin d"], "Vitamin D relates to bone and muscle health. Low levels are common and treatment depends on the level and clinician advice."),
        (["b12"], "Vitamin B12 relates to anemia, nerve symptoms, memory, balance, and energy."),
        (["urine", "protein", "pus cells", "rbc"], "Urine findings may relate to hydration, infection, kidney issues, stones, or contamination depending on the exact result."),
    ]

    findings = []
    for keywords, explanation in test_explanations:
        matched_keyword = next((keyword for keyword in keywords if contains_report_keyword(lower_report, keyword)), None)
        if not matched_keyword:
            continue

        lines = [
            line.strip()
            for line in report_text.splitlines()
            if any(contains_report_keyword(line.lower(), keyword) for keyword in keywords)
        ]
        sample = next((line for line in lines if re.search(r"\d", line)), lines[0] if lines else "")
        flag = detect_report_flag(sample)
        finding = explanation
        if sample:
            finding += f" Report line seen: `{sample[:120]}`."
        if flag:
            finding += f" It appears marked as {flag}."
        findings.append(finding)

    return findings

def detect_report_flag(report_line: str) -> str:
    """Detect common high/low report flags without assigning a diagnosis."""
    lower_line = report_line.lower()
    if re.search(r"\b(high|above|elevated|raised|h)\b", lower_line):
        return "high"
    if re.search(r"\b(low|below|reduced|decreased|l)\b", lower_line):
        return "low"
    if "*" in report_line or "!" in report_line:
        return "flagged by the lab"
    return ""

def build_report_next_steps(report_text: str) -> list[str]:
    """Build general next steps based on recognizable report categories."""
    lower_report = report_text.lower()
    next_steps = [
        "- Compare every result with the lab's reference range printed on the same report.",
        "- Share abnormal or newly changed results with the treating doctor, especially if there are symptoms.",
        "- Do not start, stop, or change medicines or supplements only from this chat response.",
    ]

    topic_steps = [
        (["glucose", "hba1c", "a1c"], "- For sugar-related results, note whether the sample was fasting or after food, and keep a log of home readings if available."),
        (["cholesterol", "ldl", "hdl", "triglyceride"], "- For cholesterol results, ask the doctor about overall heart-risk assessment, diet, activity, and whether medication is needed."),
        (["hemoglobin", " hb ", "b12"], "- For anemia-related results, ask whether iron, B12, folate, kidney function, or blood loss evaluation is needed."),
        (["creatinine", "egfr", "urea"], "- For kidney-related results, review hydration, blood pressure, diabetes control, and medicines with a clinician."),
        (["tsh", "thyroid", "t3", "t4"], "- For thyroid results, do not adjust thyroid medicine without medical advice; timing and repeat testing may matter."),
        (["alt", "ast", "bilirubin", "sgpt", "sgot"], "- For liver-related results, review alcohol use, recent infections, pain medicines, supplements, and other medicines with the doctor."),
        (["urine", "pus cells", "protein", "rbc"], "- For urine results, mention burning urination, fever, back pain, swelling, or blood in urine if present."),
    ]

    for keywords, step in topic_steps:
        if any(contains_report_keyword(lower_report, keyword) for keyword in keywords):
            next_steps.append(step)

    return next_steps

def contains_report_keyword(text: str, keyword: str) -> bool:
    """Match short lab names as complete words, not inside other words."""
    normalized_keyword = keyword.strip().lower()
    if not normalized_keyword:
        return False
    if " " in normalized_keyword:
        return normalized_keyword in text
    return bool(re.search(rf"\b{re.escape(normalized_keyword)}\b", text))

def detect_emotional_tone(message: str) -> str:
    """Detect emotional tone (simplified)"""
    lower_msg = message.lower()

    sad_keywords = ["sad", "lonely", "depressed", "miss", "cry"]
    happy_keywords = ["happy", "great", "wonderful", "love", "excited"]
    worried_keywords = ["worried", "nervous", "anxious", "scared", "afraid"]

    if any(kw in lower_msg for kw in sad_keywords):
        return "concerning"
    elif any(kw in lower_msg for kw in happy_keywords):
        return "positive"
    elif any(kw in lower_msg for kw in worried_keywords):
        return "concerning"

    return "neutral"
