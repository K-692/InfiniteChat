zodiac_signs = (
    'aries',
    'taurus',
    'gemini',
    'cancer',
    'leo',
    'virgo',
    'libra',
    'scorpio',
    'sagittarius',
    'capricorn',
    'aquarius',
    'pisces'
)

emo_map = {
    'Male':'🧔🏻',
    'Female':'👩🏻‍🦰'
}


relationships = {
    "Male": ["Father", "Son", "Brother", "Uncle", "Nephew", "Cousin", "Grandfather", "Grandson",
    "Friend", "Colleague", "Mentor", "Mentee", "Partner", "Roommate", "Neighbor",
    "Teammate", "Classmate", "Boss", "Employee", "Acquaintance", "Rival", "Confidant",
    "Husband", "Boyfriend", "Fiancé"],
    "Female": ["Mother", "Daughter", "Sister", "Aunt", "Niece", "Cousin", "Grandmother", "Granddaughter",
    "Wife", "Girlfriend", "Fiancée",
    "Friend", "Colleague", "Mentor", "Mentee", "Partner", "Roommate", "Neighbor",
    "Teammate", "Classmate", "Boss", "Employee", "Acquaintance", "Rival", "Confidant"]
}

def get_relationship_mapping(relationship, second_person_gender):
    relationship_mappings = {
        "Father": {"Male": "Son", "Female": "Daughter"},
        "Mother": {"Male": "Son", "Female": "Daughter"},
        "Son": {"Male": "Father", "Female": "Mother"},
        "Daughter": {"Male": "Father", "Female": "Mother"},
        "Brother": {"Male": "Brother", "Female": "Sister"},
        "Sister": {"Male": "Brother", "Female": "Sister"},
        "Uncle": {"Male": "Nephew", "Female": "Niece"},
        "Aunt": {"Male": "Nephew", "Female": "Niece"},
        "Nephew": {"Male": "Uncle", "Female": "Aunt"},
        "Niece": {"Male": "Uncle", "Female": "Aunt"},
        "Cousin": {"Male": "Cousin", "Female": "Cousin"},
        "Grandfather": {"Male": "Grandson", "Female": "Granddaughter"},
        "Grandmother": {"Male": "Grandson", "Female": "Granddaughter"},
        "Grandson": {"Male": "Grandfather", "Female": "Grandmother"},
        "Granddaughter": {"Male": "Grandfather", "Female": "Grandmother"},
        "Husband": {"Female": "Wife"},
        "Wife": {"Male": "Husband"},
        "Boyfriend": {"Female": "Girlfriend"},
        "Girlfriend": {"Male": "Boyfriend"},
        "Fiancé": {"Female": "Fiancée"},
        "Fiancée": {"Male": "Fiancé"},
        "Friend": {"Male": "Friend", "Female": "Friend"},
        "Colleague": {"Male": "Colleague", "Female": "Colleague"},
        "Mentor": {"Male": "Mentee", "Female": "Mentee"},
        "Mentee": {"Male": "Mentor", "Female": "Mentor"},
        "Partner": {"Male": "Partner", "Female": "Partner"},
        "Roommate": {"Male": "Roommate", "Female": "Roommate"},
        "Neighbor": {"Male": "Neighbor", "Female": "Neighbor"},
        "Teammate": {"Male": "Teammate", "Female": "Teammate"},
        "Classmate": {"Male": "Classmate", "Female": "Classmate"},
        "Boss": {"Male": "Employee", "Female": "Employee"},
        "Employee": {"Male": "Boss", "Female": "Boss"},
        "Acquaintance": {"Male": "Acquaintance", "Female": "Acquaintance"},
        "Rival": {"Male": "Rival", "Female": "Rival"},
        "Confidant": {"Male": "Confidant", "Female": "Confidant"}
    }
    
    if relationship in relationship_mappings:
        if second_person_gender in relationship_mappings[relationship]:
            return relationship_mappings[relationship][second_person_gender]
    else:
        return "Friend"
    

def remove_outer_quotes(text):
    # Check if the text starts and ends with double quotes
    if text.startswith('"') and text.endswith('"'):
        # Remove the outer double quotes
        return text[1:-1]
    return text