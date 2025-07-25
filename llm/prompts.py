CLASSIFICATION_PROMPT = """You are a medical expert. Classify these symptoms: {symptoms}

Categories: Blood Diseases, Deficiency Diseases, Allergies, 
Degenerative Diseases, Infectious Diseases, General Medicine

Wards: general, emergency, ICU, maternity, pediatric, 
orthopedic, ENT, ophthalmology, dermatology, neurology

Respond ONLY in this format:
Category: <selected_category>
Ward: <selected_ward>"""