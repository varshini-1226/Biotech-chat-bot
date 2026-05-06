import sqlite3

def create_database():
    conn = sqlite3.connect("biotech_chatbot.db")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS faq (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT NOT NULL,
            answer TEXT NOT NULL
        );
    """)

    faqs = [

    # Basic molecular biology
    ("dna", "DNA is the genetic material that carries hereditary information in living organisms."),
    ("rna", "RNA helps in protein synthesis by carrying genetic information from DNA."),
    ("gene", "A gene is a segment of DNA that codes for a specific protein or trait."),

    # PCR
    ("what is pcr", 
     "PCR (Polymerase Chain Reaction) is a technique used to amplify specific DNA sequences."),

    ("steps in pcr", 
     "The main steps in PCR are denaturation, annealing, and extension."),

    ("pcr steps", 
     "PCR involves three steps: denaturation, annealing, and extension."),

    ("full form of pcr", 
     "The full form of PCR is Polymerase Chain Reaction."),

    ("pcr full form", 
     "PCR stands for Polymerase Chain Reaction."),

    ("types of pcr", 
     "Types of PCR include conventional PCR, RT‑PCR, real‑time PCR, and multiplex PCR."),

    # ELISA
    ("elisa", "ELISA is a technique used to detect antigens or antibodies using enzyme-linked reactions."),
    ("types of elisa", "Types of ELISA include direct, indirect, sandwich, and competitive ELISA."),

    # Protein analysis
    ("sds-page", "SDS-PAGE separates proteins based on molecular weight."),
    ("western blot", "Western blot is used to detect specific proteins using antibodies."),

    # Genetic engineering
    ("plasmid", "A plasmid is a circular DNA molecule used as a vector in genetic engineering."),
    ("restriction enzyme", "Restriction enzymes cut DNA at specific recognition sites."),
    ("crispr", "CRISPR is a gene-editing technology used to modify DNA precisely."),

    # Cell culture & biotech
    ("cell culture", "Cell culture is the process of growing cells under controlled laboratory conditions."),
    ("bioreactor", "A bioreactor is a vessel used to grow microorganisms or cells for product formation."),
    ("fermentation", "Fermentation is a metabolic process where microorganisms convert substrates into products."),

    # Immunology
    ("vaccine", "Vaccines stimulate the immune system to provide protection against diseases."),
    ("antibody", "Antibodies are proteins produced by the immune system to recognize antigens."),

]
 

    cur.execute("DELETE FROM faq;")
    cur.executemany("INSERT INTO faq (keyword, answer) VALUES (?, ?);", faqs)

    conn.commit()
    conn.close()
    print("Database created and FAQs inserted successfully.")

if __name__ == "__main__":
    create_database()