import csv

data = [
    # Simple ENG (1-10)
    {"patient_id": 1, "soap_text": "Cholera caused by Vibrio cholerae 01, biovar cholerae", "expected_icd_codes": "A000", "lang": "ENG"},
    {"patient_id": 2, "soap_text": "Typhoid fever diagnosed recently", "expected_icd_codes": "A010", "lang": "ENG"},
    {"patient_id": 3, "soap_text": "Salmonella enteritis with mild diarrhea", "expected_icd_codes": "A020", "lang": "ENG"},
    {"patient_id": 4, "soap_text": "Botulism suspected after canned food ingestion", "expected_icd_codes": "A051", "lang": "ENG"},
    {"patient_id": 5, "soap_text": "Acute amebic dysentery presenting with bloody stools", "expected_icd_codes": "A060", "lang": "ENG"},
    {"patient_id": 6, "soap_text": "Rotavirus enteritis in a child", "expected_icd_codes": "A080", "lang": "ENG"},
    {"patient_id": 7, "soap_text": "Acute gastroenteritis caused by norovirus", "expected_icd_codes": "A081", "lang": "ENG"},
    {"patient_id": 8, "soap_text": "Miliary tuberculosis confirmed by sputum microscopy", "expected_icd_codes": "A190", "lang": "ENG"},
    {"patient_id": 9, "soap_text": "Skin infection due to amebiasis", "expected_icd_codes": "A067", "lang": "ENG"},
    {"patient_id": 10, "soap_text": "Shigellosis caused by Shigella dysenteriae", "expected_icd_codes": "A030", "lang": "ENG"},

    # Simple NO (11-20)
    {"patient_id": 11, "soap_text": "Kolera som skyldes Vibrio cholerae 01, biovar cholerae", "expected_icd_codes": "A000", "lang": "NO"},
    {"patient_id": 12, "soap_text": "Tyfoidfeber diagnostisert nylig", "expected_icd_codes": "A010", "lang": "NO"},
    {"patient_id": 13, "soap_text": "Salmonellaenteritt med magesmerter", "expected_icd_codes": "A020", "lang": "NO"},
    {"patient_id": 14, "soap_text": "Botulisme etter inntak av hermetikk", "expected_icd_codes": "A051", "lang": "NO"},
    {"patient_id": 15, "soap_text": "Akutt amøbedysenteri med blodig diaré", "expected_icd_codes": "A060", "lang": "NO"},
    {"patient_id": 16, "soap_text": "Rotavirusenteritt hos barn", "expected_icd_codes": "A080", "lang": "NO"},
    {"patient_id": 17, "soap_text": "Akutt gastroenteritt som skyldes norovirus", "expected_icd_codes": "A081", "lang": "NO"},
    {"patient_id": 18, "soap_text": "Miliærtuberkulose bekreftet ved mikroskopi av sputum", "expected_icd_codes": "A190", "lang": "NO"},
    {"patient_id": 19, "soap_text": "Amøbeinfeksjon i hud", "expected_icd_codes": "A067", "lang": "NO"},
    {"patient_id": 20, "soap_text": "Shigellose som skyldes Shigella dysenteriae", "expected_icd_codes": "A030", "lang": "NO"},

    # Medium ENG (21-30)
    {"patient_id": 21, "soap_text": "Patient shows chronic amebic infection in the intestinal tract with intermittent symptoms", "expected_icd_codes": "A061", "lang": "ENG"},
    {"patient_id": 22, "soap_text": "Chronic tuberculous infection involving strupehode and glottis confirmed bacteriologically", "expected_icd_codes": "A155", "lang": "ENG"},
    {"patient_id": 23, "soap_text": "Enteritis caused by Yersinia enterocolitica, moderate severity", "expected_icd_codes": "A046", "lang": "ENG"},
    {"patient_id": 24, "soap_text": "Suspected leptospirosis with jaundice and hemorrhagic symptoms", "expected_icd_codes": "A270", "lang": "ENG"},
    {"patient_id": 25, "soap_text": "Gastrointestinal tularemia with fever and abdominal pain", "expected_icd_codes": "A213", "lang": "ENG"},
    {"patient_id": 26, "soap_text": "Generalized tularemia showing systemic symptoms", "expected_icd_codes": "A217", "lang": "ENG"},
    {"patient_id": 27, "soap_text": "Tuberculous meningitis with confirmed diagnosis", "expected_icd_codes": "A170", "lang": "ENG"},
    {"patient_id": 28, "soap_text": "Suspected pulmonary tuberculosis with negative bacteriology", "expected_icd_codes": "A160", "lang": "ENG"},
    {"patient_id": 29, "soap_text": "Sepsis caused by Erysipelothrix", "expected_icd_codes": "A267", "lang": "ENG"},
    {"patient_id": 30, "soap_text": "Acute miliary tuberculosis with multiple organ involvement", "expected_icd_codes": "A191", "lang": "ENG"},

    # Medium NO (31-40)
    {"patient_id": 31, "soap_text": "Pasienten har kronisk amøbeinfeksjon i tarmkanalen med intermittente symptomer", "expected_icd_codes": "A061", "lang": "NO"},
    {"patient_id": 32, "soap_text": "Kronisk tuberkulose i strupehode og glottis, bekreftet bakteriologisk", "expected_icd_codes": "A155", "lang": "NO"},
    {"patient_id": 33, "soap_text": "Enteritt forårsaket av Yersinia enterocolitica, moderat alvorlighetsgrad", "expected_icd_codes": "A046", "lang": "NO"},
    {"patient_id": 34, "soap_text": "Mistenkt leptospirose med gulsott og blødningssymptomer", "expected_icd_codes": "A270", "lang": "NO"},
    {"patient_id": 35, "soap_text": "Gastrointestinal tularemi med feber og magesmerter", "expected_icd_codes": "A213", "lang": "NO"},
    {"patient_id": 36, "soap_text": "Generalisert tularemi med systemiske symptomer", "expected_icd_codes": "A217", "lang": "NO"},
    {"patient_id": 37, "soap_text": "Tuberkuløs meningitt med bekreftet diagnose", "expected_icd_codes": "A170", "lang": "NO"},
    {"patient_id": 38, "soap_text": "Mistenkt lunge tuberkulose med negativ bakteriologisk undersøkelse", "expected_icd_codes": "A160", "lang": "NO"},
    {"patient_id": 39, "soap_text": "Sepsis forårsaket av Erysipelothrix", "expected_icd_codes": "A267", "lang": "NO"},
    {"patient_id": 40, "soap_text": "Akutt miliær tuberkulose med flere organsystem involvert", "expected_icd_codes": "A191", "lang": "NO"},
]

with open("soap_eval_data.csv", mode="w", newline="", encoding="utf-8") as f:
    fieldnames = ["patient_id", "soap", "expected_codes", "lang"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for row in data:
        writer.writerow({
            "patient_id": row["patient_id"],
            "soap": row["soap_text"],
            "expected_codes": row["expected_icd_codes"],
            "lang": row["lang"]
        })

print("soap_eval_data.csv created with 40 rows.")
