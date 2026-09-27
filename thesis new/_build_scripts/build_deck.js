const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const fa = require("react-icons/fa");
const D = require("./deck_data.json");

const OUT = "/home/krishna/Desktop/Thesis/Hairfall-Thesis/thesis new/Hairfall_Thesis_Presentation.pptx";
const NAVY = "14213D", INK = "1F2937", MUTED = "6B7280", PANEL = "F3F5F9", WHITE = "FFFFFF";
const AMBER = "E9A23B", BLUE = "2F6FD6", GREEN = "2EA44F", TEAL = "1F8A8A", RED = "C8443B", SOFT = "DCE3EE";
const MC = { CatBoost: AMBER, TabPFN: BLUE, TabFM: GREEN };
const HEAD = "Cambria", BODY = "Calibri";

async function icon(name, color = "#FFFFFF", size = 256) {
  const Comp = fa[name];
  if (!Comp) throw new Error("missing icon " + name);
  const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(Comp, { color, size: String(size) }));
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

const fmt = (n) => n.toLocaleString("en-US");

(async () => {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9"; // 10 x 5.625
  pres.title = "Comparative Benchmarking of CatBoost, TabPFN and TabFM for Explainable Hair Fall Risk Stratification";
  pres.author = "Krishna Gautam";

  const shadow = () => ({ type: "outer", color: "000000", opacity: 0.12, blur: 6, offset: 2, angle: 90 });
  let n = 0;

  function slide(title, notes) {
    n += 1;
    const s = pres.addSlide();
    s.background = { color: WHITE };
    s.addText(title, { x: 0.5, y: 0.28, w: 9.0, h: 0.85, fontFace: HEAD, fontSize: 25, bold: true, color: NAVY, margin: 0, valign: "top", isTextBox: true });
    s.addText(String(n + 0), { x: 9.0, y: 5.22, w: 0.5, h: 0.25, fontFace: BODY, fontSize: 10, color: MUTED, align: "right", margin: 0, isTextBox: true });
    if (notes) s.addNotes(notes);
    return s;
  }
  const card = (s, x, y, w, h, fill = PANEL) => s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: fill }, line: { color: fill, width: 0 }, rectRadius: 0.08, shadow: fill === PANEL ? undefined : shadow() });
  const circle = (s, x, y, d, fill) => s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fill }, line: { color: fill, width: 0 } });
  const txt = (s, t, o) => s.addText(t, Object.assign({ fontFace: BODY, fontSize: 13, color: INK, margin: 0, valign: "top", isTextBox: true }, o));
  async function iconCircle(s, name, x, y, d, fill, color = "#FFFFFF") {
    circle(s, x, y, d, fill);
    const pad = d * 0.26;
    s.addImage({ data: await icon(name, color), x: x + pad, y: y + pad, w: d - 2 * pad, h: d - 2 * pad });
  }

  // ---------------------------------------------------------------- 1 title
  {
    n += 1;
    const s = pres.addSlide();
    s.background = { color: NAVY };
    s.addNotes("Good morning. My thesis compares a classical tuned model, CatBoost, with two new pre-trained 'foundation' models, TabPFN and TabFM, for predicting hair fall risk, and it also explains what each model relies on.");
    txt(s, "MCS THESIS PRESENTATION", { x: 0.6, y: 0.55, w: 6.0, h: 0.3, fontSize: 11, bold: true, color: AMBER, charSpacing: 3 });
    txt(s, "Comparative Benchmarking of CatBoost, TabPFN and TabFM for Explainable Hair Fall Risk Stratification", { x: 0.6, y: 1.0, w: 5.9, h: 2.1, fontFace: HEAD, fontSize: 28, bold: true, color: WHITE });
    txt(s, "Krishna Gautam", { x: 0.6, y: 3.45, w: 5.9, h: 0.35, fontSize: 20, bold: true, color: WHITE });
    txt(s, "Supervised by Rabin Thapa", { x: 0.6, y: 3.85, w: 5.9, h: 0.3, fontSize: 15, color: SOFT });
    txt(s, "Lincoln International College of Management & IT\nLincoln University College, Malaysia  ·  September 2026", { x: 0.6, y: 4.45, w: 5.9, h: 0.6, fontSize: 11, color: SOFT });
    card(s, 6.95, 0.75, 2.5, 1.25, WHITE);
    s.addImage({ path: "logo-000.png", x: 7.1, y: 0.95, w: 2.2, h: 0.844 });
    const chips = [["CatBoost", AMBER, "tuned decision trees"], ["TabPFN", BLUE, "pre-trained transformer"], ["TabFM", GREEN, "Google foundation model"]];
    chips.forEach(([t, c, sub], i) => {
      const y = 2.55 + i * 0.78;
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 6.95, y, w: 2.5, h: 0.62, fill: { color: c }, line: { color: c, width: 0 }, rectRadius: 0.1 });
      txt(s, t, { x: 7.1, y: y + 0.05, w: 2.2, h: 0.28, fontSize: 15, bold: true, color: WHITE });
      txt(s, sub, { x: 7.1, y: y + 0.33, w: 2.2, h: 0.22, fontSize: 10.5, color: WHITE });
    });
  }

  // ---------------------------------------------------------------- 2 agenda
  {
    const s = slide("What we will cover", "Here is the roadmap: why the problem matters, how the study was designed, what we found, how the models can be explained, what it costs, and what we conclude.");
    const items = [
      ["1", "Introduction", "Why hair fall risk is hard, the gaps, our questions", "Slides 3–6", TEAL],
      ["2", "Method", "The three models, the data, a fair test", "Slides 7–10", TEAL],
      ["3", "Results", "Accuracy, training size, significance, errors", "Slides 11–15", TEAL],
      ["4", "Explainability", "What drives the risk (SHAP)", "Slides 16–17", TEAL],
      ["5", "Cost and discussion", "Run time, model choice, limits", "Slides 18–20", TEAL],
      ["6", "Conclusion", "Answers and recommendations", "Slides 21–22", TEAL],
    ];
    items.forEach(([num, t, d, r], i) => {
      const x = 0.5 + (i % 3) * 3.075, y = 1.4 + Math.floor(i / 3) * 1.95;
      card(s, x, y, 2.85, 1.7, WHITE);
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: 2.85, h: 1.7, fill: { color: PANEL }, line: { color: SOFT, width: 0.75 }, rectRadius: 0.08 });
      circle(s, x + 0.2, y + 0.2, 0.5, NAVY);
      txt(s, num, { x: x + 0.2, y: y + 0.2, w: 0.5, h: 0.5, fontSize: 18, bold: true, color: WHITE, align: "center", valign: "middle" });
      txt(s, t, { x: x + 0.85, y: y + 0.22, w: 1.85, h: 0.5, fontFace: HEAD, fontSize: 15, bold: true, color: NAVY, valign: "middle" });
      txt(s, d, { x: x + 0.2, y: y + 0.85, w: 2.45, h: 0.5, fontSize: 12, color: INK });
      txt(s, r, { x: x + 0.2, y: y + 1.35, w: 2.45, h: 0.25, fontSize: 11, bold: true, color: AMBER });
    });
  }

  // ---------------------------------------------------------------- 3 background
  {
    const s = slide("Hair fall risk is hard to judge by eye", "Hair loss has many causes at once. No single blood test gives the answer, and today the assessment depends on what the patient says and on a late clinical check. A tool that combines many measurements could give an earlier, more objective estimate.");
    const rows = [
      ["FaFlask", "Many causes act together", "Iron, protein, vitamin D, liver function, stress, sleep, chemicals and family history all play a part."],
      ["FaSearch", "No single test tells the risk", "Risk comes from the mix of factors, so one measurement alone is not reliable."],
      ["FaUserMd", "Today: history and late examination", "Assessment depends on what patients report, differs between doctors and is hard to reach in many places."],
    ];
    for (let i = 0; i < 3; i++) {
      const y = 1.4 + i * 1.22;
      await iconCircle(s, rows[i][0], 0.5, y + 0.05, 0.7, TEAL);
      txt(s, rows[i][1], { x: 1.45, y: y, w: 4.7, h: 0.35, fontFace: HEAD, fontSize: 16, bold: true, color: NAVY });
      txt(s, rows[i][2], { x: 1.45, y: y + 0.38, w: 4.7, h: 0.7, fontSize: 12.5 });
    }
    card(s, 6.55, 1.35, 2.95, 3.65, NAVY);
    [["21,606", "patients in the dataset"], ["20", "clinical and lifestyle features"], ["3", "risk tiers: Low · Moderate · High"]].forEach(([big, small], i) => {
      const y = 1.55 + i * 1.15;
      txt(s, big, { x: 6.8, y, w: 2.5, h: 0.6, fontFace: HEAD, fontSize: 34, bold: true, color: AMBER });
      txt(s, small, { x: 6.8, y: y + 0.62, w: 2.5, h: 0.4, fontSize: 12, color: WHITE });
    });
  }

  // ---------------------------------------------------------------- 4 gaps
  {
    const s = slide("Three gaps in earlier work made this study necessary", "First, earlier studies disagree about which model is best. Second, the new foundation models had never been tested on hair fall data. Third, complex models do not explain themselves. Our study addresses all three at once.");
    const cols = [
      ["FaBalanceScale", "No clear best model", "One study found an ensemble best, another found Random Forest ahead of CatBoost. Data and goals differ, so the results cannot be compared."],
      ["FaRobot", "New models, never tested here", "TabPFN and TabFM predict from the training rows without being trained, but nobody had tried them on hair fall data."],
      ["FaEyeSlash", "Black boxes", "Accurate models rarely say why. Without reasons, a doctor cannot check a risk score against clinical knowledge."],
    ];
    for (let i = 0; i < 3; i++) {
      const x = 0.5 + i * 3.075;
      card(s, x, 1.35, 2.85, 2.75, PANEL);
      await iconCircle(s, cols[i][0], x + 0.25, 1.55, 0.65, NAVY);
      txt(s, cols[i][1], { x: x + 0.25, y: 2.3, w: 2.4, h: 0.5, fontFace: HEAD, fontSize: 15, bold: true, color: NAVY });
      txt(s, cols[i][2], { x: x + 0.25, y: 2.85, w: 2.4, h: 1.2, fontSize: 12 });
    }
    card(s, 0.5, 4.3, 9.0, 0.75, NAVY);
    txt(s, "Our answer: compare CatBoost, TabPFN and TabFM on the same data, at three training sizes, and explain all three with SHAP.", { x: 0.75, y: 4.3, w: 8.5, h: 0.75, fontSize: 14, bold: true, color: WHITE, valign: "middle" });
  }

  // ---------------------------------------------------------------- 5 research questions
  {
    const s = slide("What we wanted to find out: four questions", "Each research question has one matching objective and one part of the method. We will come back to these four questions in the conclusion.");
    const q = [
      ["Can pre-trained models match a tuned CatBoost, and is the difference real?", "Same split and metrics, plus McNemar's test"],
      ["How much training data does each model need?", "Every model at 500, 2,000 and 17,284 rows"],
      ["Which features drive the risk, and do the models agree?", "SHAP for every model and every size"],
      ["What does each model cost to run?", "Record run time, memory and problems"],
    ];
    q.forEach(([t, how], i) => {
      const y = 1.35 + i * 0.93;
      card(s, 0.5, y, 9.0, 0.8, PANEL);
      circle(s, 0.65, y + 0.12, 0.56, NAVY);
      txt(s, "Q" + (i + 1), { x: 0.65, y: y + 0.12, w: 0.56, h: 0.56, fontSize: 14, bold: true, color: WHITE, align: "center", valign: "middle" });
      txt(s, t, { x: 1.45, y: y, w: 4.5, h: 0.8, fontSize: 13.5, bold: true, color: INK, valign: "middle" });
      txt(s, "How we tested it", { x: 6.15, y: y + 0.1, w: 3.2, h: 0.2, fontSize: 9.5, bold: true, color: TEAL });
      txt(s, how, { x: 6.15, y: y + 0.32, w: 3.2, h: 0.42, fontSize: 12 });
    });
  }

  // ---------------------------------------------------------------- 6 literature
  {
    const s = slide("Earlier studies were useful, but they disagree", "These are the main hair loss studies. They used different data and targets, so their accuracy numbers cannot be compared with ours. The important point is that none of them tested foundation models, and only one was built to be explainable.");
    const th = (t) => ({ text: t, options: { bold: true, color: WHITE, fill: { color: NAVY }, fontFace: BODY, fontSize: 12 } });
    const td = (t, b) => ({ text: t, options: { color: INK, fontFace: BODY, fontSize: 11.5, bold: !!b } });
    const rows = [
      [th("Study"), th("What they found")],
      [td("Widowati et al. [1]", true), td("Explainable system; keep data preparation inside cross-validation")],
      [td("Sai et al. [3]", true), td("An ensemble beat single classifiers")],
      [td("Patel et al. [4]", true), td("Random Forest beat XGBoost, CatBoost and LightGBM")],
      [td("Chen et al. [5]", true), td("Neural networks find more, but are harder to explain")],
      [td("Shakeel et al. [6]", true), td("Scalp images: SVM 91.4%, KNN 88.9%")],
    ];
    s.addTable(rows, { x: 0.5, y: 1.35, w: 5.6, colW: [1.7, 3.9], rowH: 0.56, border: { type: "solid", color: SOFT, pt: 0.75 }, valign: "middle" });
    card(s, 6.4, 1.35, 3.1, 3.4, NAVY);
    txt(s, "The gap", { x: 6.65, y: 1.5, w: 2.6, h: 0.35, fontFace: HEAD, fontSize: 17, bold: true, color: AMBER });
    txt(s, [
      { text: "Conflicting answers on the best model", options: { bullet: true, breakLine: true } },
      { text: "Foundation models untested on hair fall data", options: { bullet: true, breakLine: true } },
      { text: "Explainability treated unevenly", options: { bullet: true } },
    ], { x: 6.65, y: 1.95, w: 2.65, h: 2.6, fontSize: 13, color: WHITE, paraSpaceAfter: 9 });
  }

  // ---------------------------------------------------------------- 7 models
  {
    const s = slide("Three models, three ways of learning", "CatBoost really trains on our rows and is tuned by cross-validation. TabPFN and TabFM are pre-trained on millions of synthetic tables, so for our data they only read the training rows as examples. This is why they need little data but are slower at prediction time.");
    const cols = [
      ["CatBoost", "Learns from the data", AMBER, ["Many small decision trees, each fixing the last one's mistakes", "Tuned by grid search and 5-fold cross-validation", "Trains in seconds, small model"]],
      ["TabPFN", "Pre-trained, no training", BLUE, ["Transformer trained on millions of synthetic tables", "Reads our training rows as examples and predicts in one pass", "Needs the rows at prediction time"]],
      ["TabFM", "Google's foundation model", GREEN, ["Same idea, with attention over rows and columns", "About 6.5 GB of weights, the slowest of the three", "Needs a GPU for full-size data"]],
    ];
    cols.forEach(([name, tag, c, pts], i) => {
      const x = 0.5 + i * 3.075;
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.35, w: 2.85, h: 3.05, fill: { color: PANEL }, line: { color: SOFT, width: 0.75 }, rectRadius: 0.08 });
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.35, w: 2.85, h: 0.85, fill: { color: c }, line: { color: c, width: 0 }, rectRadius: 0.08 });
      txt(s, name, { x: x + 0.2, y: 1.42, w: 2.5, h: 0.4, fontFace: HEAD, fontSize: 19, bold: true, color: WHITE });
      txt(s, tag, { x: x + 0.2, y: 1.82, w: 2.5, h: 0.3, fontSize: 12, color: WHITE });
      txt(s, pts.map((p, k) => ({ text: p, options: { bullet: true, breakLine: k < pts.length - 1 } })), { x: x + 0.2, y: 2.4, w: 2.5, h: 1.9, fontSize: 12, paraSpaceAfter: 6 });
    });
    card(s, 0.5, 4.55, 9.0, 0.55, NAVY);
    txt(s, "Foundation model = a model that has already learned how tables work, so it needs no training on our data.", { x: 0.7, y: 4.55, w: 8.6, h: 0.55, fontSize: 13, bold: true, color: WHITE, valign: "middle" });
  }

  // ---------------------------------------------------------------- 8 dataset
  {
    const s = slide("The data: 21,606 patients, 20 features, 3 risk tiers", "The data come from a company dataset, so this is a benchmark of models, not a clinical trial. There are no missing values, no duplicates and no impossible values.");
    s.addChart(pres.charts.DOUGHNUT, [{ name: "Risk tier", labels: ["Low", "Moderate", "High"], values: D.classes }], {
      x: 0.4, y: 1.25, w: 4.2, h: 3.5, holeSize: 55, chartColors: ["7FB77E", AMBER, RED], showPercent: true, showValue: false, showLegend: true, legendPos: "b", legendFontSize: 12, legendColor: INK,
      dataLabelColor: WHITE, dataLabelFontSize: 12, dataLabelFontBold: true, showTitle: false,
    });
    const g = [
      ["Blood markers", "iron, protein, calcium, vitamin D, liver enzyme ALT, manganese, body water", TEAL],
      ["Stress and hair scores", "stress level, hair texture, keratine", BLUE],
      ["Lifestyle and history", "sleep, chemicals, water, anemia, illness, family history", AMBER],
      ["Basics", "age and gender", GREEN],
    ];
    g.forEach(([h, d, c], i) => {
      const y = 1.35 + i * 0.83;
      circle(s, 4.95, y + 0.08, 0.22, c);
      txt(s, h, { x: 5.3, y, w: 4.2, h: 0.3, fontSize: 14, bold: true, color: NAVY });
      txt(s, d, { x: 5.3, y: y + 0.3, w: 4.2, h: 0.5, fontSize: 11.5 });
    });
    card(s, 4.95, 4.6, 4.55, 0.5, PANEL);
    txt(s, "Company dataset: a benchmark, not a clinical trial.", { x: 5.1, y: 4.6, w: 4.3, h: 0.5, fontSize: 11, bold: true, color: MUTED, valign: "middle" });
  }

  // ---------------------------------------------------------------- 9 pipeline
  {
    const s = slide("The study in one picture", "Everything is a numbered step. We check and clean the data, split it once, give each model three training sizes, test all of them on the same 4,322 patients, explain them with SHAP, and finally compare and test the differences. The final runs were done on a Kaggle T4 GPU.");
    const steps = [
      ["FaDatabase", "Data", "Company dataset, 21,606 records"],
      ["FaFilter", "Clean data", "reference ranges; drop names and id"],
      ["FaCut", "Split once", "80% train (17,284), 20% test (4,322)"],
      ["FaLayerGroup", "Three sizes", "500 · 2,000 · Full training rows"],
      ["FaMicrochip", "Three models", "CatBoost, TabPFN, TabFM"],
      ["FaBullseye", "Same test set", "accuracy, F1, AUC, kappa"],
      ["FaLightbulb", "Explain", "SHAP for all nine runs"],
      ["FaChartLine", "Compare", "McNemar, run time, scaling"],
    ];
    for (let i = 0; i < 8; i++) {
      const r = Math.floor(i / 4), c = i % 4;
      const x = 0.5 + c * 2.35, y = 1.4 + r * 1.85;
      card(s, x, y, 1.95, 1.4, PANEL);
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: 1.95, h: 1.4, fill: { color: PANEL }, line: { color: SOFT, width: 0.75 }, rectRadius: 0.08 });
      await iconCircle(s, steps[i][0], x + 0.15, y + 0.15, 0.5, i < 4 ? TEAL : NAVY);
      txt(s, String(i + 1), { x: x + 1.55, y: y + 0.12, w: 0.3, h: 0.25, fontSize: 11, bold: true, color: MUTED, align: "right" });
      txt(s, steps[i][1], { x: x + 0.15, y: y + 0.72, w: 1.7, h: 0.28, fontFace: HEAD, fontSize: 13.5, bold: true, color: NAVY });
      txt(s, steps[i][2], { x: x + 0.15, y: y + 1.0, w: 1.7, h: 0.4, fontSize: 10.5, color: INK });
      if (c < 3) s.addShape(pres.shapes.LINE, { x: x + 1.95, y: y + 0.7, w: 0.4, h: 0, line: { color: MUTED, width: 1.5, endArrowType: "triangle" } });
    }
    s.addShape(pres.shapes.LINE, { x: 0.5 + 3 * 2.35 + 0.975, y: 2.8, w: 0, h: 0.2, line: { color: MUTED, width: 1.5 } });
    s.addShape(pres.shapes.LINE, { x: 0.5 + 0.975, y: 3.0, w: 3 * 2.35, h: 0, line: { color: MUTED, width: 1.5 }, flipH: false });
    s.addShape(pres.shapes.LINE, { x: 0.5 + 0.975, y: 3.0, w: 0, h: 0.25, line: { color: MUTED, width: 1.5, endArrowType: "triangle" } });
    txt(s, "Each stage is one step in our own Hairfall Lab; the final runs were executed on a Kaggle Tesla T4 GPU.", { x: 0.5, y: 4.95, w: 8.4, h: 0.25, fontSize: 10.5, color: MUTED });
  }

  // ---------------------------------------------------------------- 10 fair test
  {
    const s = slide("Six rules that keep the comparison fair", "These rules mean any difference we see comes from the models and the amount of data, not from unfair treatment. CatBoost was tuned properly so that the baseline was not handicapped, and the test patients were never used for tuning or stopping.");
    const t = [
      ["Same split", "17,284 training and 4,322 test records; fixed seed 42"],
      ["Same test patients", "Every model is scored on all 4,322; never used for tuning"],
      ["Three training sizes", "500, 2,000 and 17,284 rows for every model"],
      ["Fair baseline", "CatBoost tuned: 9 settings x 5-fold cross-validation"],
      ["Many measures", "Accuracy, macro-F1, ROC-AUC, kappa, log loss"],
      ["Real tests", "McNemar's test and 95% confidence intervals; SHAP for all"],
    ];
    t.forEach(([h, d], i) => {
      const x = 0.5 + (i % 3) * 3.075, y = 1.4 + Math.floor(i / 3) * 1.85;
      card(s, x, y, 2.85, 1.6, PANEL);
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: 2.85, h: 1.6, fill: { color: PANEL }, line: { color: SOFT, width: 0.75 }, rectRadius: 0.08 });
      circle(s, x + 0.2, y + 0.2, 0.42, TEAL);
      txt(s, String(i + 1), { x: x + 0.2, y: y + 0.2, w: 0.42, h: 0.42, fontSize: 14, bold: true, color: WHITE, align: "center", valign: "middle" });
      txt(s, h, { x: x + 0.75, y: y + 0.2, w: 1.95, h: 0.42, fontFace: HEAD, fontSize: 14, bold: true, color: NAVY, valign: "middle" });
      txt(s, d, { x: x + 0.2, y: y + 0.82, w: 2.5, h: 0.7, fontSize: 12 });
    });
  }

  // ---------------------------------------------------------------- 11 accuracy
  {
    const s = slide("With all the data, the three models are almost equal (78.2% to 78.7%)", "This chart shows the accuracy of all nine runs. With 500 or 2,000 rows the two foundation models are clearly ahead of CatBoost. With all 17,284 rows the three models are within half a percentage point of each other. Note that the vertical axis starts at 60 percent so that the differences are visible.");
    const labels = ["500 rows", "2,000 rows", "Full (17,284)"];
    s.addChart(pres.charts.BAR, ["CatBoost", "TabPFN", "TabFM"].map((m) => ({ name: m, labels, values: D.acc[m] })), {
      x: 0.4, y: 1.25, w: 6.2, h: 3.85, barDir: "col", barGrouping: "clustered", chartColors: [AMBER, BLUE, GREEN], barGapWidthPct: 55,
      showValue: true, dataLabelFormatCode: "0.0", dataLabelFontSize: 10, dataLabelColor: INK, dataLabelPosition: "outEnd",
      catAxisLabelFontSize: 12, catAxisLabelColor: INK, valAxisMinVal: 60, valAxisMaxVal: 85, valAxisMajorUnit: 5, valAxisLabelFontSize: 10, valAxisLabelColor: MUTED,
      valGridLine: { color: "E5E7EB", size: 0.5 }, catGridLine: { style: "none" }, showLegend: true, legendPos: "b", legendFontSize: 12, legendColor: INK,
      showTitle: false, valAxisTitle: "Accuracy (%)", showValAxisTitle: true, valAxisTitleFontSize: 11, valAxisTitleColor: MUTED,
    });
    txt(s, "Full training data", { x: 6.85, y: 1.35, w: 2.65, h: 0.3, fontSize: 12, bold: true, color: MUTED });
    [["TabFM", GREEN, 2], ["TabPFN", BLUE, 1], ["CatBoost", AMBER, 0]].forEach(([m, c, k], i) => {
      const y = 1.75 + i * 0.85;
      card(s, 6.85, y, 2.65, 0.72, PANEL);
      circle(s, 7.0, y + 0.22, 0.28, c);
      txt(s, D.acc[m][2].toFixed(2) + "%", { x: 7.4, y: y + 0.05, w: 2.0, h: 0.4, fontFace: HEAD, fontSize: 21, bold: true, color: NAVY });
      txt(s, m + "  ·  macro-F1 " + D.f1[m][2].toFixed(3), { x: 7.4, y: y + 0.44, w: 2.05, h: 0.22, fontSize: 10.5, color: MUTED });
    });
    txt(s, "Gap between best and worst: 0.47 points.", { x: 6.85, y: 4.4, w: 2.65, h: 0.5, fontSize: 12, bold: true, color: INK });
  }

  // ---------------------------------------------------------------- 12 training size
  {
    const s = slide("CatBoost needs lots of data; the foundation models do not", "CatBoost gains almost nine accuracy points when it gets all the data, while the foundation models gain less than two. With only 500 rows the foundation models are already better than CatBoost trained on 2,000 rows. The same behaviour in two independently built models suggests it is a property of this kind of model, though we tested only one dataset.");
    const labels = ["500", "2,000", "Full (17,284)"];
    s.addChart(pres.charts.LINE, ["CatBoost", "TabPFN", "TabFM"].map((m) => ({ name: m, labels, values: D.acc[m] })), {
      x: 0.4, y: 1.25, w: 5.9, h: 3.85, chartColors: [AMBER, BLUE, GREEN], lineSize: 3, lineDataSymbolSize: 9, showValue: false,
      catAxisLabelFontSize: 12, catAxisLabelColor: INK, valAxisMinVal: 66, valAxisMaxVal: 80, valAxisMajorUnit: 2, valAxisLabelFontSize: 10, valAxisLabelColor: MUTED,
      valGridLine: { color: "E5E7EB", size: 0.5 }, catGridLine: { style: "none" }, showLegend: true, legendPos: "b", legendFontSize: 12, legendColor: INK, showTitle: false,
      showCatAxisTitle: true, catAxisTitle: "Training rows", catAxisTitleFontSize: 11, catAxisTitleColor: MUTED, showValAxisTitle: true, valAxisTitle: "Accuracy (%)", valAxisTitleFontSize: 11, valAxisTitleColor: MUTED,
    });
    txt(s, "Gain from 500 rows to all rows", { x: 6.55, y: 1.35, w: 2.95, h: 0.3, fontSize: 12, bold: true, color: MUTED });
    [["CatBoost", AMBER], ["TabPFN", BLUE], ["TabFM", GREEN]].forEach(([m, c], i) => {
      const y = 1.75 + i * 0.95;
      card(s, 6.55, y, 2.95, 0.82, PANEL);
      txt(s, "+" + D.gain[m].toFixed(2), { x: 6.7, y: y + 0.08, w: 1.45, h: 0.6, fontFace: HEAD, fontSize: 24, bold: true, color: c, valign: "middle" });
      txt(s, m + "\nacc. points", { x: 8.2, y: y + 0.1, w: 1.25, h: 0.6, fontSize: 11, color: INK, valign: "middle" });
    });
    txt(s, "500 rows of a foundation model beat CatBoost with 2,000 rows.", { x: 6.55, y: 4.65, w: 2.95, h: 0.5, fontSize: 11.5, bold: true, color: NAVY });
  }

  // ---------------------------------------------------------------- 13 McNemar
  {
    const s = slide("Is the gap real? Yes with little data, no with all the data", "McNemar's test looks only at patients where two models disagree. With 500 and 2,000 rows both foundation models are significantly better than CatBoost, with p below 0.0001. With all the data there is no significant difference. TabPFN and TabFM never differ from each other. A non-significant result does not prove the models are equal, only that no difference was detected.");
    const th = (t) => ({ text: t, options: { bold: true, color: WHITE, fill: { color: NAVY }, fontFace: BODY, fontSize: 10.5, align: "center", valign: "middle" } });
    const rows = [[th("Rows"), th("Comparison"), th("b"), th("c"), th("p-value"), th("Real gap?")]];
    D.mcnemar.forEach((r, i) => {
      const yes = r[5];
      const cell = (t, o = {}) => ({ text: String(t), options: Object.assign({ fontFace: BODY, fontSize: 10.5, color: INK, align: "center", valign: "middle" }, o) });
      rows.push([cell(r[0]), cell(r[1], { align: "left" }), cell(r[2]), cell(r[3]), cell(r[4]), cell(yes ? "Yes" : "No", { bold: true, color: yes ? "8A5A00" : "1B6B34", fill: { color: yes ? "FCE9C7" : "DDF1E3" } })]);
    });
    s.addTable(rows, { x: 0.5, y: 1.3, w: 5.95, colW: [0.75, 2.05, 0.65, 0.65, 0.95, 0.9], rowH: 0.34, border: { type: "solid", color: SOFT, pt: 0.75 } });
    card(s, 6.7, 1.3, 2.8, 3.75, NAVY);
    txt(s, "What it means", { x: 6.9, y: 1.45, w: 2.4, h: 0.3, fontFace: HEAD, fontSize: 16, bold: true, color: AMBER });
    txt(s, [
      { text: "500 and 2,000 rows: both foundation models beat CatBoost (p < 0.0001)", options: { bullet: true, breakLine: true } },
      { text: "All rows: no significant difference (p = 0.27 and 0.23)", options: { bullet: true, breakLine: true } },
      { text: "TabPFN and TabFM: never different", options: { bullet: true } },
    ], { x: 6.9, y: 1.85, w: 2.45, h: 2.9, fontSize: 12, color: WHITE, paraSpaceAfter: 8 });
    txt(s, "b = only first model right, c = only second model right", { x: 0.5, y: 4.85, w: 5.95, h: 0.25, fontSize: 9.5, color: MUTED });
  }

  // ---------------------------------------------------------------- 14 confusion
  {
    const s = slide("When models are wrong, they miss by one tier only", "The confusion matrix shows true tiers as rows and predicted tiers as columns. Almost all mistakes are between neighbouring tiers. Calling a Low patient High happened only twice and calling a High patient Low never happened. The Moderate tier is the hardest because it sits between the other two.");
    s.addImage({ path: "cm_TabPFN_Full.png", x: 0.5, y: 1.3, w: 4.05, h: 3.6 });
    txt(s, "TabPFN, full training data", { x: 0.5, y: 4.9, w: 4.05, h: 0.25, fontSize: 10.5, color: MUTED, align: "center" });
    const st = [
      [D.cm.neigh + " of " + D.cm.errors, "errors are between neighbouring tiers", TEAL],
      [D.cm.lh + " and " + D.cm.hl, "Low called High, and High called Low", GREEN],
      ["0.71", "F1 of the Moderate tier: the hardest to classify", AMBER],
    ];
    st.forEach(([big, small, c], i) => {
      const y = 1.35 + i * 1.2;
      card(s, 4.95, y, 4.55, 1.05, PANEL);
      txt(s, big, { x: 5.1, y: y + 0.1, w: 2.2, h: 0.85, fontFace: HEAD, fontSize: 21, bold: true, color: c, valign: "middle" });
      txt(s, small, { x: 7.35, y: y + 0.1, w: 2.05, h: 0.85, fontSize: 12, valign: "middle" });
    });
    txt(s, "All three models show the same pattern.", { x: 4.95, y: 4.95, w: 4.55, h: 0.25, fontSize: 11, italic: true, color: MUTED });
  }

  // ---------------------------------------------------------------- 15 extra checks
  {
    const s = slide("Three more checks: probabilities, shared mistakes, fairness", "First, the probabilities of the foundation models are better, especially with little data. Second, the three models make mostly the same mistakes, so the limit is in the data and not in the model. Third, accuracy is similar for women and men and for the age bands, so no group is served much worse.");
    const p = D.prob;
    const cards = [
      ["FaChartLine", "Better probabilities", "0.66 to 0.50", "log loss with 500 rows: CatBoost vs TabPFN (lower is better). The gap shrinks with more data: 0.49 vs 0.47.", BLUE],
      ["FaUsers", "Shared mistakes", D.overlap.none + " patients", "wrong for all three models with full data (18%); that is 84 to 86% of each model's errors. The limit is in the data.", TEAL],
      ["FaBalanceScale", "No big group gaps", "≤ 2 points", "largest accuracy gap between women and men (1.1) and between age bands (2.0), with full data.", AMBER],
    ];
    for (let i = 0; i < 3; i++) {
      const x = 0.5 + i * 3.075;
      card(s, x, 1.35, 2.85, 3.6, PANEL);
      await iconCircle(s, cards[i][0], x + 0.25, 1.55, 0.6, cards[i][4]);
      txt(s, cards[i][1], { x: x + 0.25, y: 2.3, w: 2.4, h: 0.35, fontFace: HEAD, fontSize: 15, bold: true, color: NAVY });
      txt(s, cards[i][2], { x: x + 0.25, y: 2.7, w: 2.4, h: 0.6, fontFace: HEAD, fontSize: 22, bold: true, color: cards[i][4] });
      txt(s, cards[i][3], { x: x + 0.25, y: 3.4, w: 2.4, h: 1.4, fontSize: 11.5 });
    }
  }

  // ---------------------------------------------------------------- 16 SHAP importance
  {
    const s = slide("SHAP: iron and stress lead every model", "SHAP gives each feature a score for how much it pushed each patient's prediction up or down. In all nine analyses, iron and stress level were the top two features, followed by protein, the liver enzyme ALT, vitamin D and calcium. The rankings of the three models agree closely.");
    const f = D.shap10.f.slice().reverse().map((x) => x.replace(/_/g, " ")), v = D.shap10.v.slice().reverse();
    s.addChart(pres.charts.BAR, [{ name: "Mean |SHAP|", labels: f, values: v }], {
      x: 0.4, y: 1.25, w: 5.4, h: 3.85, barDir: "bar", chartColors: [TEAL], barGapWidthPct: 45, showValue: true, dataLabelFormatCode: "0.00", dataLabelFontSize: 10, dataLabelColor: INK,
      catAxisLabelFontSize: 11, catAxisLabelColor: INK, valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" }, showLegend: false,
      showTitle: true, title: "CatBoost, full data: average impact of each feature", titleFontSize: 11, titleColor: MUTED,
    });
    card(s, 6.05, 1.3, 3.45, 1.15, PANEL);
    txt(s, "What is SHAP?", { x: 6.25, y: 1.38, w: 3.1, h: 0.28, fontSize: 12.5, bold: true, color: TEAL });
    txt(s, "A score for how much each feature pushed a patient's risk up or down.", { x: 6.25, y: 1.68, w: 3.1, h: 0.7, fontSize: 11.5 });
    txt(s, [
      { text: "Iron and stress level: top two in all 9 analyses", options: { bullet: true, breakLine: true } },
      { text: "Then protein, liver enzyme ALT, vitamin D, calcium", options: { bullet: true, breakLine: true } },
      { text: "Same six lead in 8 of 9 analyses", options: { bullet: true, breakLine: true } },
      { text: "Rank agreement between models: " + Math.min(...D.rc).toFixed(2) + " to " + Math.max(...D.rc).toFixed(2), options: { bullet: true } },
    ], { x: 6.05, y: 2.65, w: 3.45, h: 2.4, fontSize: 12, paraSpaceAfter: 7 });
  }

  // ---------------------------------------------------------------- 17 direction
  {
    const s = slide("The direction of the effects makes clinical sense", "In the plot, each dot is one patient. Dots to the right push the prediction towards High risk, and the colour shows whether the patient's value is high or low. Low iron and high stress push risk up, while higher protein, vitamin D and calcium push it down. This agrees with the simple correlations in the data. It shows what the models learned from this company dataset, not proof of cause.");
    txt(s, "How to read the plot", { x: 0.5, y: 1.3, w: 4.6, h: 0.3, fontSize: 13, bold: true, color: TEAL });
    txt(s, "Each dot is a patient. Right of the centre = pushes towards High risk. Red = high value, blue = low value.", { x: 0.5, y: 1.62, w: 4.6, h: 0.6, fontSize: 11.5 });
    txt(s, [
      { text: "Low iron, high stress and high liver enzyme raise the risk", options: { bullet: true, breakLine: true } },
      { text: "High protein, vitamin D, calcium and manganese lower it", options: { bullet: true, breakLine: true } },
      { text: "Every yes/no risk factor pushes risk up", options: { bullet: true, breakLine: true } },
      { text: "Same directions in CatBoost, TabPFN and TabFM", options: { bullet: true } },
    ], { x: 0.5, y: 2.4, w: 4.6, h: 1.85, fontSize: 12.5, paraSpaceAfter: 6 });
    card(s, 0.5, 4.3, 4.6, 0.8, PANEL);
    txt(s, "Matches the data: stress " + D.spearman.stress_level.toFixed(2) + ", iron " + D.spearman.iron.toFixed(2) + ", protein " + D.spearman.total_protein.toFixed(2) + " (correlation with risk tier). Association, not cause.", { x: 0.65, y: 4.3, w: 4.35, h: 0.8, fontSize: 11, bold: true, color: NAVY, valign: "middle" });
    s.addImage({ path: "bee_CatBoost_Full.png", x: 5.4, y: 1.2, w: 4.09, h: 3.85 });
  }

  // ---------------------------------------------------------------- 18 cost
  {
    const s = slide("The price: foundation models are slow to run and to explain", "With the full data, CatBoost is fitted in about three seconds. TabPFN needs about five minutes and TabFM about fifty minutes to predict the test patients on a T4 GPU. Explaining them with Kernel SHAP is even slower. TabFM full-size could not run at all on our 16 GB laptop without a GPU, so we used Kaggle with memory-saving settings.");
    const c = [
      ["CatBoost", D.time.CatBoost.toFixed(1) + " s", "fit and predict", AMBER],
      ["TabPFN", "≈ 5 min", D.ptime.TabPFN.toFixed(0) + " s to predict 4,322 patients", BLUE],
      ["TabFM", "≈ 51 min", fmt(Math.round(D.ptime.TabFM)) + " s to predict 4,322 patients", GREEN],
    ];
    c.forEach(([m, big, small, col], i) => {
      const x = 0.5 + i * 3.075;
      card(s, x, 1.3, 2.85, 1.65, PANEL);
      s.addShape(pres.shapes.OVAL, { x: x + 0.22, y: 1.5, w: 0.22, h: 0.22, fill: { color: col }, line: { color: col, width: 0 } });
      txt(s, m + " (full data)", { x: x + 0.55, y: 1.47, w: 2.2, h: 0.28, fontSize: 12.5, bold: true, color: NAVY });
      txt(s, big, { x: x + 0.22, y: 1.82, w: 2.5, h: 0.6, fontFace: HEAD, fontSize: 28, bold: true, color: col });
      txt(s, small, { x: x + 0.22, y: 2.45, w: 2.5, h: 0.4, fontSize: 11 });
    });
    card(s, 0.5, 3.15, 4.4, 1.95, NAVY);
    txt(s, "Explaining costs even more", { x: 0.72, y: 3.27, w: 4.0, h: 0.3, fontFace: HEAD, fontSize: 15, bold: true, color: AMBER });
    txt(s, [
      { text: "CatBoost SHAP: 1,000 patients in 0.3 s", options: { bullet: true, breakLine: true } },
      { text: "TabPFN SHAP: 30 patients in 54 min", options: { bullet: true, breakLine: true } },
      { text: "TabFM SHAP: 20 patients in 2.4 hours", options: { bullet: true } },
    ], { x: 0.72, y: 3.65, w: 4.0, h: 1.4, fontSize: 12.5, color: WHITE, paraSpaceAfter: 6 });
    card(s, 5.1, 3.15, 4.4, 1.95, PANEL);
    txt(s, "Problems we had to solve", { x: 5.32, y: 3.27, w: 4.0, h: 0.3, fontFace: HEAD, fontSize: 15, bold: true, color: NAVY });
    txt(s, [
      { text: "TabFM full size ran out of memory on a 16 GB laptop, so it needed a GPU", options: { bullet: true, breakLine: true } },
      { text: "Memory-saving attention and automatic batch halving", options: { bullet: true, breakLine: true } },
      { text: "Package conflicts and single-row failures", options: { bullet: true } },
    ], { x: 5.32, y: 3.65, w: 4.0, h: 1.4, fontSize: 12, paraSpaceAfter: 6 });
  }

  // ---------------------------------------------------------------- 19 which model
  {
    const s = slide("What it means: which model should you choose?", "The choice depends on how much labelled data you have and where the model will run. With few rows a foundation model is much better and gives better probabilities. With plenty of data CatBoost is just as accurate, thousands of times cheaper, and works on a normal computer for one patient at a time. Explanations are possible for all, cheapest for CatBoost.");
    const th = (t) => ({ text: t, options: { bold: true, color: WHITE, fill: { color: NAVY }, fontFace: BODY, fontSize: 13, valign: "middle" } });
    const chip = (t, c) => ({ text: t, options: { bold: true, color: WHITE, fill: { color: c }, fontFace: BODY, fontSize: 13, align: "center", valign: "middle" } });
    const td = (t) => ({ text: t, options: { color: INK, fontFace: BODY, fontSize: 12, valign: "middle" } });
    const rows = [
      [th("Situation"), th("Choose"), th("Why")],
      [td("Only a few thousand labelled rows (or fewer)"), chip("TabPFN or TabFM", BLUE), td("7 to 8 points more accurate at 500 rows; better probabilities; no tuning")],
      [td("A lot of data, and a tool that scores one patient at a time"), chip("CatBoost", AMBER), td("Same accuracy with all rows, trains in seconds, small model, no GPU")],
      [td("You need a reason for every score"), chip("Any, with SHAP", TEAL), td("All three can be explained; CatBoost is exact and 0.3 s")],
      [td("You need fast, cheap deployment"), chip("CatBoost", AMBER), td("Foundation models need the training rows and a GPU at prediction time")],
    ];
    s.addTable(rows, { x: 0.5, y: 1.35, w: 9.0, colW: [3.3, 1.9, 3.8], rowH: [0.42, 0.72, 0.72, 0.72, 0.72], border: { type: "solid", color: SOFT, pt: 0.75 } });
    txt(s, "Caution: measured on one company dataset.", { x: 0.5, y: 4.95, w: 9.0, h: 0.25, fontSize: 11, italic: true, color: MUTED });
  }

  // ---------------------------------------------------------------- 20 limitations
  {
    const s = slide("What to keep in mind: the limits of this study", "We want to be open about the limits. The dataset comes from one company, so the results are about the models and not about real patients. We used one split and one seed. SHAP for the foundation models used only 30 and 20 patients. Timings come from different hardware for CatBoost and the foundation models.");
    const items = [
      ["FaDatabase", "Company data", "One company dataset, not a clinical registry. Results are not a diagnostic tool.", RED],
      ["FaCut", "One split, one seed", "Small differences at full size cannot be separated from chance.", AMBER],
      ["FaLightbulb", "Small SHAP samples", "30 and 20 patients for the foundation models; only leading features are interpreted.", AMBER],
      ["FaMicrochip", "Hardware and versions", "CatBoost on CPU, others on GPU; TabPFN and SHAP versions were not fixed.", TEAL],
      ["FaBalanceScale", "Grid and settings", "Small CatBoost grid; foundation models used default settings.", TEAL],
      ["FaSearch", "Not tested", "Ordinal models, patient-level explanations and real clinical data.", TEAL],
    ];
    for (let i = 0; i < 6; i++) {
      const x = 0.5 + (i % 3) * 3.075, y = 1.35 + Math.floor(i / 3) * 1.9;
      card(s, x, y, 2.85, 1.7, PANEL);
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: 2.85, h: 1.7, fill: { color: PANEL }, line: { color: SOFT, width: 0.75 }, rectRadius: 0.08 });
      await iconCircle(s, items[i][0], x + 0.2, y + 0.2, 0.5, items[i][3]);
      txt(s, items[i][1], { x: x + 0.85, y: y + 0.2, w: 1.9, h: 0.5, fontFace: HEAD, fontSize: 13.5, bold: true, color: NAVY, valign: "middle" });
      txt(s, items[i][2], { x: x + 0.2, y: y + 0.85, w: 2.5, h: 0.8, fontSize: 11.5 });
    }
  }

  // ---------------------------------------------------------------- 21 conclusions
  {
    const s = slide("Conclusions: answers to our four questions", "These are the four answers. One: no significant difference with all the data, but foundation models are clearly better with little data. Two: CatBoost depends much more on data. Three: iron and stress lead in every model and the directions agree. Four: CatBoost costs seconds, TabPFN minutes and TabFM close to an hour on a GPU.");
    const a = [
      ["Q1", "Performance", "With all the data no significant difference (78.2% to 78.7%); with 500 and 2,000 rows the foundation models win (p < 0.0001)."],
      ["Q2", "Training size", "CatBoost gains " + D.gain.CatBoost.toFixed(1) + " points from 500 rows to all; TabPFN and TabFM gain " + D.gain.TabPFN.toFixed(1) + " and " + D.gain.TabFM.toFixed(1) + "."],
      ["Q3", "Explanation", "Iron and stress level lead in all 9 analyses; effects point the same way and match the data."],
      ["Q4", "Cost", "CatBoost: seconds. TabPFN: about 5 minutes. TabFM: about 51 minutes on a GPU, and it needs one."],
    ];
    a.forEach(([q, h, d], i) => {
      const y = 1.35 + i * 0.93;
      card(s, 0.5, y, 9.0, 0.8, PANEL);
      circle(s, 0.65, y + 0.12, 0.56, NAVY);
      txt(s, q, { x: 0.65, y: y + 0.12, w: 0.56, h: 0.56, fontSize: 14, bold: true, color: WHITE, align: "center", valign: "middle" });
      txt(s, h, { x: 1.45, y: y, w: 1.85, h: 0.8, fontFace: HEAD, fontSize: 14, bold: true, color: NAVY, valign: "middle" });
      txt(s, d, { x: 3.35, y: y, w: 6.0, h: 0.8, fontSize: 12.5, valign: "middle" });
    });
  }

  // ---------------------------------------------------------------- 22 recommendations
  {
    const s = slide("Recommendations and what comes next", "For practice: use a foundation model when data are few, use CatBoost when data are plentiful, check cost before choosing, and always add explanations. For research: repeat with several splits, explain more patients, tune all models, try ordinal models, validate on real clinical data, and study ensembles. Thank you, I am happy to take your questions.");
    card(s, 0.5, 1.3, 4.4, 2.95, PANEL);
    txt(s, "For practice", { x: 0.72, y: 1.42, w: 4.0, h: 0.32, fontFace: HEAD, fontSize: 16, bold: true, color: TEAL });
    txt(s, [
      { text: "Few labelled rows: start with TabPFN", options: { bullet: true, breakLine: true } },
      { text: "Plenty of data: a tuned CatBoost is enough", options: { bullet: true, breakLine: true } },
      { text: "Measure run time and memory before you plan", options: { bullet: true, breakLine: true } },
      { text: "Always add SHAP; use it as decision support only", options: { bullet: true } },
    ], { x: 0.72, y: 1.85, w: 4.0, h: 2.3, fontSize: 12.5, paraSpaceAfter: 6 });
    card(s, 5.1, 1.3, 4.4, 2.95, PANEL);
    txt(s, "For further research", { x: 5.32, y: 1.42, w: 4.0, h: 0.32, fontFace: HEAD, fontSize: 16, bold: true, color: TEAL });
    txt(s, [
      { text: "Several splits and seeds, with confidence intervals", options: { bullet: true, breakLine: true } },
      { text: "Explain more patients; add patient-level plots", options: { bullet: true, breakLine: true } },
      { text: "Tune all models; try ordinal models", options: { bullet: true, breakLine: true } },
      { text: "Validate on real clinical data", options: { bullet: true, breakLine: true } },
      { text: "Ensembles and lighter, distilled models", options: { bullet: true } },
    ], { x: 5.32, y: 1.85, w: 4.0, h: 2.3, fontSize: 12.5, paraSpaceAfter: 6 });
    card(s, 0.5, 4.45, 9.0, 0.65, NAVY);
    txt(s, "Thank you  ·  Questions?", { x: 0.7, y: 4.45, w: 8.6, h: 0.65, fontFace: HEAD, fontSize: 20, bold: true, color: WHITE, valign: "middle", align: "center" });
  }

  await pres.writeFile({ fileName: OUT });
  console.log("wrote", OUT, "slides:", n);
})().catch((e) => { console.error(e); process.exit(1); });
