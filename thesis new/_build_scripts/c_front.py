from dx import *

TITLE = "Comparative Benchmarking of CatBoost, TabPFN, and TabFM for Explainable Multi-Tier Hair Fall Risk Stratification"
AUTHOR = "Krishna Gautam"
LCID = "(LC ID: LC0015002874)"
COLLEGE = "Lincoln International College of Management & IT"
UNIV = "Lincoln University College, Malaysia"
DATE = "September, 2026"
SUPERVISOR = "Rabin Thapa"
LOGO = "/tmp/claude-1000/-home-krishna-Desktop-Thesis-Hairfall-Thesis/3a0d67b6-c14e-4ab2-95b7-3de697bbdd86/scratchpad/assets/logo-000.png"


def _center(t, text, size=16, bold=False, after=10, line=1.5):
    p = t.p(text, align=C, bold=bold, size=size, space_after=after, line=line)
    return p


def cover(t):
    t.first_section_setup()
    t.blank(1)
    _center(t, "Thesis for the Degree of Master of Computer Science (MCS)", 16)
    t.blank(1)
    _center(t, TITLE, 20, True)
    t.blank(3)
    para = t.doc.add_paragraph(); para.alignment = C
    para.add_run().add_picture(LOGO, width=Cm(5.0))
    t.blank(3)
    _center(t, AUTHOR, 16, True)
    _center(t, LCID, 16)
    t.blank(1)
    _center(t, COLLEGE, 16)
    t.blank(1)
    _center(t, UNIV, 16, True)
    _center(t, DATE, 16, True)


def title_page(t):
    t.blank(1)
    _center(t, "Research Project for the Degree of Master of Computer Science (MCS)", 16)
    t.blank(1)
    _center(t, TITLE, 20, True)
    t.blank(3)
    _center(t, f"Supervised by {SUPERVISOR}", 16, True)
    t.blank(1)
    _center(t, "A thesis submitted in partial fulfilment of the requirements for the degree of Master of Computer Science (MCS)", 16)
    t.blank(3)
    _center(t, AUTHOR, 16, True)
    _center(t, LCID, 16)
    t.blank(1)
    _center(t, COLLEGE, 16)
    _center(t, UNIV, 16, True)
    _center(t, DATE, 16, True)


def _sign_block(t, lines):
    t.blank(3)
    t.p("……………………………………", align=L, space_after=0)
    t.p("Signature", align=L, space_after=0)
    for ln in lines:
        t.p(ln, align=L, space_after=0)


def declaration(t):
    t.unnumbered_heading("Declaration", page_break=False)
    t.p(f"I hereby declare that this study entitled **{TITLE}** is based on my original research work. "
        "Related works on the topic by other researchers have been duly acknowledged. I owe all the liabilities relating to the "
        "accuracy and authenticity of the data and any other information included hereunder.", indent=1.0)
    _sign_block(t, [f"Name of the Student: {AUTHOR}", "Registration Number: LC ID: LC0015002874", "Date: ……………………………"])


def recommendation(t):
    t.unnumbered_heading("Recommendation")
    t.p(f"This is to certify that this thesis entitled **{TITLE}**, prepared and submitted by **{AUTHOR}**, in partial fulfilment of the "
        "requirements of the degree of Master of Computer Science (MCS) awarded by Lincoln University College, Malaysia, has been "
        "completed under my supervision. I recommend the same for acceptance by Lincoln University College, Malaysia.", indent=1.0)
    _sign_block(t, [f"Name of the Supervisor: {SUPERVISOR}", f"Organization: {COLLEGE}", "Date: ……………………………"])


def certificate(t):
    t.unnumbered_heading("Certificate")
    t.p(f"This thesis entitled **{TITLE}** prepared and submitted by **{AUTHOR}** has been examined by us and is accepted for the "
        "award of the degree of Master of Computer Science (MCS) by Lincoln University College, Malaysia.", indent=1.0)
    for name, role in (("……………………………………", "External Examiner"), (SUPERVISOR, "Supervisor"), ("……………………………………", "Head of Department / Principal")):
        t.blank(2)
        t.p(name, align=L, bold=(name == SUPERVISOR), space_after=0, line=1.15)
        t.p("Signature: ……………………………          Date signed: ……………………", align=L, space_after=0, line=1.15)
        t.p(role, align=L, space_after=0, line=1.15)


def acknowledgements(t):
    t.unnumbered_heading("Acknowledgements")
    t.p("I would like to express my sincere gratitude to my supervisor, Rabin Thapa, for his guidance, suggestions and encouragement "
        "throughout this research. His comments at every stage helped me to shape the study and to improve this thesis.", indent=1.0)
    t.p("I am thankful to Lincoln International College of Management & IT and to all the faculty members and staff of the Master of "
        "Computer Science programme for their teaching and support during my studies. I also thank the company for providing its dataset "
        "for this study, and the developers of the open-source software used in the experiments.", indent=1.0)
    t.p("I am grateful to my classmates and friends for their discussions and help, and to my family for their patience, support and encouragement.", indent=1.0)
    _sign_block(t, [f"Name of the Student: {AUTHOR}", "Registration Number: LC ID: LC0015002874", "Date: ……………………………"])


def abbreviations(t):
    t.unnumbered_heading("List of Abbreviations/Acronyms")
    rows = [("ALT", "Alanine Aminotransferase"), ("CPU", "Central Processing Unit"), ("CUDA", "Compute Unified Device Architecture"),
            ("CV", "Cross-Validation"), ("EHR", "Electronic Health Record"), ("GPU", "Graphics Processing Unit"),
            ("KNN", "k-Nearest Neighbour"), ("MAE", "Mean Absolute Error"), ("MCS", "Master of Computer Science"),
            ("NeurIPS", "Conference on Neural Information Processing Systems"), ("OOM", "Out of Memory"),
            ("QWK", "Quadratic Weighted Kappa"), ("ROC-AUC", "Receiver Operating Characteristic – Area Under the Curve"),
            ("SHAP", "Shapley Additive Explanations"), ("SVM", "Support Vector Machine"), ("TabFM", "Tabular Foundation Model"),
            ("TabPFN", "Tabular Prior-Fitted Network"), ("VRAM", "Video Random Access Memory")]
    for a, b in rows:
        para = t.doc.add_paragraph()
        pf = para.paragraph_format
        pf.alignment = L; pf.line_spacing = 1.5; pf.space_after = Pt(2)
        pf.tab_stops.add_tab_stop(Cm(3.2), WD_TAB_ALIGNMENT.LEFT)
        pf.left_indent = Cm(3.2); pf.first_line_indent = Cm(-3.2)
        t._runs(para, f"{a}\t{b}")


def units(t):
    t.unnumbered_heading("Units and Conversions")
    rows = [("%", "Percent"), ("g/dL", "Grams per decilitre"), ("GB", "Gigabyte"), ("h", "Hour"), ("mg/dL", "Milligrams per decilitre"),
            ("min", "Minute"), ("ng/mL", "Nanograms per millilitre"), ("s", "Second"), ("U/L", "Units per litre"),
            ("µg/dL", "Micrograms per decilitre"), ("µg/L", "Micrograms per litre")]
    for a, b in rows:
        para = t.doc.add_paragraph()
        pf = para.paragraph_format
        pf.alignment = L; pf.line_spacing = 1.5; pf.space_after = Pt(2)
        pf.tab_stops.add_tab_stop(Cm(3.2), WD_TAB_ALIGNMENT.LEFT)
        pf.left_indent = Cm(3.2); pf.first_line_indent = Cm(-3.2)
        t._runs(para, f"{a}\t{b}")


def abstract(t, paras, keywords):
    t.unnumbered_heading("ABSTRACT")
    for x in paras:
        t.p(x, indent=1.0)
    t.blank(1, 12)
    t.p("**Keywords:** " + keywords, align=L)
