"""
papers.py — Your literature database
=====================================
Fill in this file manually to add papers to the network.

HOW TO ADD A PAPER:
1. Copy a block from the PAPERS list below
2. Fill in the fields (use None if you don't know something)
3. Use the citekey as the unique ID (e.g. "@smith2023")

HOW TO ADD A CONNECTION (cited_by / responds_to):
- In EDGES, add a dict with "from" and "to" using citekeys
- Direction: "from" responds to / cites "to"

ARTICLE TYPES (suggestions, use anything that fits):
  "Opinion article", "Perspective article", "Review", "Comment",
  "Commentary", "Viewpoint", "Empirical study", "Book chapter"
"""

# ─────────────────────────────────────────────
#  PAPERS
#  Each dict = one paper. Fill in what you have.
# ─────────────────────────────────────────────

PAPERS = [

    {
        "id":          "@abiodun2019a",
        "title":       '"Seeing Color," A Discussion of the Implications and Applications of Race in the Field of Neuroscience',
        "author":      "Sade J. Abiodun",
        "year":        2019,
        "journal":     "Frontiers in Human Neuroscience",
        "type":        "Opinion article",
        "doi":         "https://doi.org/10.3389/fnhum.2019.00280",
        "keywords":    ["diversity", "race", "representation", "racism", "bias"],
        "background":  "Neuroscience, neurocinematics",
        "context":     "Mostly U.S., referencing Europe",
        "react_to":    None,          # Set to a citekey string if this paper directly responds to one
        "notes":       None,          # Any personal notes you want to appear in the panel
    },

    {
        "id":          "@cardenas-iniguez2024",
        "title":       "Recommendations for the responsible use and communication of race and ethnicity in neuroimaging research",
        "author":      "Carlos Cardenas-Iniguez & Marybel Robledo Gonzalez",
        "year":        2024,
        "journal":     "Nature Neuroscience",
        "type":        "Perspective article",
        "doi":         "https://www.nature.com/articles/s41593-024-01608-4",
        "keywords":    ["race", "ethnicity", "neuroimaging", "recommendations"],
        "background":  "Public Health Sciences; addiction science & neurocognitive development",
        "context":     "U.S.",
        "react_to":    None,
        "notes":       "Key reference: gives 11 recommendations across 5 research domains. Used as benchmark in Recommendations overview sheet.",
    },

    {
        "id":          "@carter2022",
        "title":       "It's about racism, not race: a call to purge oppressive practices from neuropsychiatry and scientific discovery",
        "author":      "Carter, S.E., Mekawi, Y. & Harnett, N.G.",
        "year":        2022,
        "journal":     "Neuropsychopharmacology",
        "type":        "Comment",
        "doi":         "https://www.nature.com/articles/s41386-022-01367-5",
        "keywords":    ["racism", "neuropsychiatry", "structural racism"],
        "background":  "Clinical Psychology; Psychological and Brain Sciences; Psychiatry",
        "context":     "U.S.",
        "react_to":    None,
        "notes":       None,
    },

    {
        "id":          "@cubelli2018a",
        "title":       "Taking race out of neuroscience too",
        "author":      "Roberto Cubelli, Sergio Della Sala",
        "year":        2018,
        "journal":     "Cortex",
        "type":        "Comment",
        "doi":         "10.1016/j.cortex.2017.04.023",
        "keywords":    ["race", "neuroscience", "scientific racism"],
        "background":  "Cognitive Neuropsychology; Psycholinguistics; Clinical Psychology",
        "context":     "Europe",
        "react_to":    None,
        "notes":       "Earliest anchor paper in this corpus. Argues race is a pseudoscientific concept with no place as an analytical instrument.",
    },

    {
        "id":          "@dotson2020",
        "title":       "The importance of diversity in cognitive neuroscience",
        "author":      "Vonetta M. Dotson, Audrey Duarte",
        "year":        2020,
        "journal":     "Annals of the New York Academy of Sciences",
        "type":        "Review",
        "doi":         "10.1111/nyas.14268",
        "keywords":    ["diversity", "race", "socioeconomic status", "cognitive neuroscience"],
        "background":  "Clinical psychology, neuropsychology; Neurobiology",
        "context":     "US",
        "react_to":    None,
        "notes":       "Reacts to NIH policy shift on demographic reporting and the reproducibility crisis.",
    },

    {
        "id":          "@gilpin2021",
        "title":       "Toward an Anti-Racist Approach to Biomedical and Neuroscience Research",
        "author":      "Nicholas W. Gilpin and Michael A. Taffe",
        "year":        2021,
        "journal":     "Journal of Neuroscience",
        "type":        "Commentary",
        "doi":         "https://doi.org/10.1523/JNEUROSCI.1319-21.2021",
        "keywords":    ["anti-racism", "NIH funding", "biomedical research"],
        "background":  "Physiology, Psychology; Psychiatry, Psychology",
        "context":     "U.S.",
        "react_to":    None,
        "notes":       "Reacts to NIH Director Collins statement on structural racism. Focus on unequal NIH funding to Black scientists.",
    },

    {
        "id":          "@kaisertrujillo2022",
        "title":       "A discussion on the notion of race in cognitive neuroscience research",
        "author":      "Kaiser Trujillo, Kessé, Rollins, Della Sala & Cubelli",
        "year":        2021,
        "journal":     "CORTEX",
        "type":        "Viewpoint",
        "doi":         "10.1016/j.cortex.2021.11.007",
        "keywords":    ["race", "scientific racism", "cognitive neuroscience", "implicit race bias", "neuroimaging"],
        "background":  "Gender Studies in STEM; Sociology of neuroscience; Cognitive Neuropsychology; Clinical Psychology",
        "context":     "Europe (authors) + Rollins US",
        "react_to":    "@cubelli2018a",    # ← this paper directly responds to Cubelli 2018
        "notes":       "Debate format: Kaiser Trujillo, Kessé, Rollins argue race must be retained as social construct. Della Sala & Cubelli respond against.",
    },

    {
        "id":          "@muller2023",
        "title":       "Next steps for global collaboration to minimize racial and ethnic bias in neuroscience",
        "author":      "Ruth Müller et al.",
        "year":        2023,
        "journal":     "Nature Neuroscience",
        "type":        "Comment",
        "doi":         None,
        "keywords":    ["global collaboration", "racial bias", "neuroscience"],
        "background":  "Molecular biology / STS; Political Science; Philosophy; Sociology; Neuroengineering; Neurology",
        "context":     "European critique of US-centric framing",
        "react_to":    ["@webb2022", "@ricard2023"],   # ← responds to MULTIPLE papers: use a list
        "notes":       "TUM-affiliated authors (Buyx, Ploner). Most relevant European perspective in this corpus.",
    },

    {
        "id":          "@ricard2023",
        "title":       "Confronting racially exclusionary practices in the acquisition and analyses of neuroimaging data",
        "author":      "Ricard, Parker, Dhamala et al.",
        "year":        2022,
        "journal":     "Nature Neuroscience",
        "type":        "Perspective article",
        "doi":         None,
        "keywords":    ["neuroimaging", "exclusionary practices", "racial bias"],
        "background":  "Clinical Psychology; Biology; Neuroscience; Electrical & Computer Engineering; Psychiatry",
        "context":     "US, UK",
        "react_to":    None,
        "notes":       None,
    },

    {
        "id":          "@shen2020",
        "title":       "Racial Injustice and Neuroethics: Time for Action",
        "author":      "Francis X. Shen",
        "year":        2020,
        "journal":     "AJOB Neuroscience",
        "type":        "Commentary",
        "doi":         None,
        "keywords":    ["racial injustice", "neuroethics"],
        "background":  "Law, neuroscience",
        "context":     "U.S.",
        "react_to":    None,
        "notes":       "Responds to BRAIN Neuroethics Roadmap.",
    },

    {
        "id":          "@webb2022",
        "title":       "Addressing racial and phenotypic bias in human neuroscience methods",
        "author":      "E. Kate Webb, J. Arthur Etter and Jasmine A. Kwasa",
        "year":        2022,
        "journal":     "Nature Neuroscience",
        "type":        "Perspective article",
        "doi":         None,
        "keywords":    ["phenotypic bias", "electrodermal recordings", "neuroscience methods"],
        "background":  "Psychiatry and Behavioral Sciences; Biology and Philosophy; Electrical & Computer Engineering",
        "context":     "U.S.",
        "react_to":    None,
        "notes":       "Responds to Kredlow et al. on electrodermal recording methods.",
    },

    {
        "id":          "@webb2022a",
        "title":       "Radically reframing studies on neurobiology and socioeconomic circumstances",
        "author":      "E. Kate Webb, Carlos Cardenas-Iniguez, Robyn Douglas",
        "year":        None,
        "journal":     "Frontiers in Integrative Neuroscience",
        "type":        "Perspective article",
        "doi":         None,
        "keywords":    ["socioeconomic position", "neighborhood disadvantage", "neurobiology of stress", "social justice", "structural racism"],
        "background":  "Psychiatry and Behavioral Sciences; Public Health Sciences; Clinical Psychology",
        "context":     "U.S.",
        "react_to":    None,
        "notes":       None,
    },

    # ─────────────────────────────────────────
    # ADD YOUR NEXT PAPER HERE — copy this block:
    # ─────────────────────────────────────────
    # {
    #     "id":          "@lastname2024",
    #     "title":       "Title of the paper",
    #     "author":      "First Author et al.",
    #     "year":        2024,
    #     "journal":     "Journal Name",
    #     "type":        "Article type",
    #     "doi":         "https://doi.org/...",
    #     "keywords":    ["keyword1", "keyword2"],
    #     "background":  "Disciplinary background of authors",
    #     "context":     "US / Europe / Global",
    #     "react_to":    None,     # or "@citekey" or ["@key1", "@key2"]
    #     "notes":       "Any notes you want visible in the visualization",
    # },

]
