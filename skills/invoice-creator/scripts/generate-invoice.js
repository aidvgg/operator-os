/**
 * LEGACY GENERATOR - SUPERSEDED as the invoice standard 2026-08-02.
 * The standard is generate-invoice-html.js (print HTML -> PDF, design source
 * of record ../references/design-standard-2026-08-02.dc.html). Run this docx
 * generator only when a client needs an editable .docx; validate with
 * scripts/docx-check and run the full SKILL.md verification either way.
 */
/**
 * Northwind Labs Invoice Generator
 *
 * Generates a branded .docx invoice that matches the pre-2026-08-02 house style
 * (logo mark, dark #2d2d2d header tables, Open Sans, thin/bold dividers), the
 * visual language it shared with proposal-creator's legacy docx generator, in
 * an invoice layout.
 *
 * Usage: node generate-invoice.js <invoice-data.json> <output.docx>
 *
 * IMPORTANT: the invoice NUMBER must come from
 *   knowledge/business/invoices/INVOICE-LEDGER.md  (the "NEXT INVOICE NUMBER" block).
 * Never hardcode or guess it. See that file's protocol.
 */

const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  ImageRun, AlignmentType, BorderStyle, WidthType, ShadingType, ExternalHyperlink,
} = require("docx");

// ─── ASSETS ─────────────────────────────────────────────────────────────────
const SKILL_DIR = path.resolve(__dirname, "..");
const ASSETS_DIR = path.join(SKILL_DIR, "assets");

// ─── BRAND CONSTANTS (mirror proposal-creator) ───────────────────────────────
const FONT = "Open Sans";
const COLOR = {
  black: "000000",
  darkGray: "2d2d2d",
  medGray: "434343",
  lightGray: "666666",
  tableRowAlt: "f2f2f2",
  tableBorder: "cccccc",
  white: "ffffff",
  linkBlue: "1155cc",
};
const PAGE = {
  width: 12240, height: 15840,
  marginTop: 1440, marginBottom: 1440, marginLeft: 1440, marginRight: 1440,
  contentWidth: 9360,
};
const LOGO = { width: 942975, height: 942975 };
const DIVIDER_THIN = { width: 4457700, height: 19050 };
const DIVIDER_BOLD = { width: 4457700, height: 38100 };
const SIZE = {
  companyName: 52, subtitle: 30, sectionHeading: 32, subHeading: 28,
  body: 22, small: 19, tableHeader: 21, tableBody: 21, amountDue: 36, footer: 22,
};

// ─── IMAGE LOADERS ────────────────────────────────────────────────────────────
function loadImage(filename) {
  const imgPath = path.join(ASSETS_DIR, filename);
  if (!fs.existsSync(imgPath)) {
    throw new Error(`Asset not found: ${imgPath}. assets/ must contain logo.png, divider-bold.png, divider-thin.png`);
  }
  return fs.readFileSync(imgPath);
}
function img(file, dim) {
  return new ImageRun({
    data: loadImage(file),
    transformation: { width: Math.round(dim.width / 914400 * 96), height: Math.round(dim.height / 914400 * 96) },
    type: "png",
  });
}
// assets/logo.png ships as a neutral placeholder mark; swap it for your own.
const logoImage = () => img("logo.png", LOGO);
const thinDivider = () => img("divider-thin.png", DIVIDER_THIN);
const boldDivider = () => img("divider-bold.png", DIVIDER_BOLD);

// ─── PARAGRAPH HELPERS ────────────────────────────────────────────────────────
function sectionHeading(text) {
  return new Paragraph({
    spacing: { after: 120, before: 360 },
    children: [
      new TextRun({ text, font: FONT, bold: true, size: SIZE.sectionHeading, color: COLOR.black }),
      thinDivider(),
    ],
  });
}
function body(text, opts = {}) {
  const { bold = false, indent = 0, after = 120, color = COLOR.black, size = SIZE.body } = opts;
  return new Paragraph({
    spacing: { after },
    indent: indent ? { left: indent } : undefined,
    children: [new TextRun({ text, font: FONT, size, bold, color })],
  });
}
const spacer = (after = 80) => new Paragraph({ spacing: { after }, children: [] });

// ─── TABLE PRIMITIVES ─────────────────────────────────────────────────────────
const cellBorders = {
  top: { style: BorderStyle.SINGLE, size: 4, color: COLOR.tableBorder },
  bottom: { style: BorderStyle.SINGLE, size: 4, color: COLOR.tableBorder },
  left: { style: BorderStyle.SINGLE, size: 4, color: COLOR.tableBorder },
  right: { style: BorderStyle.SINGLE, size: 4, color: COLOR.tableBorder },
};
const noBorders = {
  top: { style: BorderStyle.NONE, size: 0 }, bottom: { style: BorderStyle.NONE, size: 0 },
  left: { style: BorderStyle.NONE, size: 0 }, right: { style: BorderStyle.NONE, size: 0 },
};
const cellMargins = { top: 80, bottom: 80, left: 120, right: 120 };

function headerCell(text, width, align = AlignmentType.LEFT) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA }, borders: cellBorders,
    shading: { fill: COLOR.darkGray, type: ShadingType.CLEAR }, margins: cellMargins,
    children: [new Paragraph({ alignment: align, children: [new TextRun({ text, font: FONT, bold: true, color: COLOR.white, size: SIZE.tableHeader })] })],
  });
}
function bodyCell(text, width, opts = {}) {
  const { bold = false, isAlt = false, color = COLOR.black, align = AlignmentType.LEFT } = opts;
  return new TableCell({
    width: { size: width, type: WidthType.DXA }, borders: cellBorders,
    shading: { fill: isAlt ? COLOR.tableRowAlt : COLOR.white, type: ShadingType.CLEAR }, margins: cellMargins,
    children: [new Paragraph({ alignment: align, children: [new TextRun({ text, font: FONT, size: SIZE.tableBody, bold, color })] })],
  });
}

/** Borderless 2-column block (e.g. From | Invoice meta, Bill-To | Amount due). */
function infoRow(leftParas, rightParas) {
  const col = PAGE.contentWidth / 2;
  const cell = (paras) => new TableCell({ width: { size: col, type: WidthType.DXA }, borders: noBorders, margins: cellMargins, children: paras });
  return new Table({
    width: { size: PAGE.contentWidth, type: WidthType.DXA }, columnWidths: [col, col],
    borders: noBorders,
    rows: [new TableRow({ children: [cell(leftParas), cell(rightParas)] })],
  });
}
function label(text) {
  return new Paragraph({ spacing: { after: 40 }, children: [new TextRun({ text, font: FONT, bold: true, size: SIZE.small, color: COLOR.lightGray })] });
}
function line(text, opts = {}) {
  const { bold = false, size = SIZE.body, color = COLOR.black } = opts;
  return new Paragraph({ spacing: { after: 20, line: 300 }, children: [new TextRun({ text, font: FONT, bold, size, color })] });
}

/** Line-items table: Description | Amount (USD) right-aligned, with a bold Total row. */
function lineItemsTable(lineItems, total) {
  const c1 = 6360, c2 = 3000;
  const rows = [
    new TableRow({ children: [headerCell("Description", c1), headerCell("Amount (USD)", c2, AlignmentType.RIGHT)] }),
    ...lineItems.map((it, i) => new TableRow({ children: [
      bodyCell(it.description, c1, { isAlt: i % 2 === 1 }),
      bodyCell(it.amount, c2, { isAlt: i % 2 === 1, align: AlignmentType.RIGHT }),
    ] })),
    new TableRow({ children: [
      bodyCell("Total", c1, { bold: true }),
      bodyCell(total, c2, { bold: true, align: AlignmentType.RIGHT }),
    ] }),
  ];
  return new Table({ width: { size: PAGE.contentWidth, type: WidthType.DXA }, columnWidths: [c1, c2], rows });
}

/** Payment-details table: [label, value] rows; bold shaded label cell, plain value cell. */
function paymentDetailsTable(rows) {
  const c1 = 3300, c2 = PAGE.contentWidth - c1;
  return new Table({
    width: { size: PAGE.contentWidth, type: WidthType.DXA }, columnWidths: [c1, c2],
    rows: rows.map(([labelText, valueText]) => new TableRow({ children: [
      bodyCell(labelText, c1, { bold: true, isAlt: true }),
      bodyCell(valueText, c2, { isAlt: false }),
    ] })),
  });
}

// ─── DOCUMENT BUILDER ─────────────────────────────────────────────────────────
function buildInvoice(d) {
  const children = [];

  // Header: logo + company + subtitle
  children.push(new Paragraph({ children: [logoImage()] }));
  children.push(spacer(60));
  children.push(new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "NORTHWIND LABS", font: FONT, bold: true, size: SIZE.companyName })] }));
  children.push(new Paragraph({
    spacing: { after: 280 },
    children: [new TextRun({ text: `Invoice ${d.invoiceNumber}`, font: FONT, color: COLOR.lightGray, size: SIZE.subtitle }), thinDivider()],
  }));

  // From | Invoice meta
  const fromParas = [label("FROM"), line(d.from.name, { bold: true }), ...d.from.lines.map(t => line(t, { size: SIZE.small, color: COLOR.medGray }))];
  if (d.from.email) {
    fromParas.push(new Paragraph({ spacing: { after: 20, line: 300 }, children: [
      new ExternalHyperlink({ link: `mailto:${d.from.email}`, children: [new TextRun({ text: d.from.email, font: FONT, size: SIZE.small, color: COLOR.linkBlue, underline: { type: "single" } })] }),
    ] }));
  }
  const metaParas = [
    label("INVOICE DETAILS"),
    line(`Invoice #:  ${d.invoiceNumber}`),
    line(`Date issued:  ${d.dateIssued}`),
    line(`Due date:  ${d.dueDate}`),
  ];
  if (d.terms) metaParas.push(line(`Terms:  ${d.terms}`));
  children.push(infoRow(fromParas, metaParas));
  children.push(spacer(80));

  // Bill To | Amount due
  const billParas = [label("BILL TO"), line(d.billTo.name, { bold: true }), ...d.billTo.lines.map(t => line(t, { size: SIZE.small, color: COLOR.medGray }))];
  const dueParas = [
    label("AMOUNT DUE"),
    new Paragraph({ spacing: { after: 20 }, children: [new TextRun({ text: d.total, font: FONT, bold: true, size: SIZE.amountDue })] }),
    line(`Due ${d.dueDate}`, { size: SIZE.small, color: COLOR.medGray }),
  ];
  children.push(infoRow(billParas, dueParas));

  // Bold divider
  children.push(spacer(120));
  children.push(new Paragraph({ children: [boldDivider()] }));
  children.push(spacer(40));

  // Line items
  children.push(lineItemsTable(d.lineItems, d.total));
  if (d.currencyNote) { children.push(spacer(60)); children.push(body(d.currencyNote, { size: SIZE.small, color: COLOR.medGray })); }
  if (d.scheduleNote) { children.push(body(d.scheduleNote, { size: SIZE.small, color: COLOR.medGray })); }

  // Payment
  children.push(sectionHeading("PAYMENT"));
  children.push(spacer(0));
  (d.paymentInstructions || []).forEach(t => children.push(body(t, { after: 40 })));
  if (d.paymentTable && d.paymentTable.length) {
    children.push(spacer(40));
    children.push(paymentDetailsTable(d.paymentTable.map(r => Array.isArray(r) ? r : [r.label, r.value])));
  }

  // Notes (optional)
  if (d.notes && d.notes.length) {
    children.push(sectionHeading("NOTES"));
    children.push(spacer(0));
    d.notes.forEach(t => children.push(body(t, { after: 40 })));
  }

  // Footer
  children.push(spacer(220));
  children.push(new Paragraph({ children: [thinDivider()] }));
  children.push(spacer(80));
  children.push(new Paragraph({ children: [
    new TextRun({ text: "NORTHWIND LABS ", font: FONT, bold: true, size: SIZE.footer }),
    new TextRun({ text: `| Invoice ${d.invoiceNumber}`, font: FONT, color: COLOR.medGray, size: SIZE.footer }),
  ] }));
  const email = d.from.email || "sam@northwindlabs.example";
  children.push(new Paragraph({ children: [
    new TextRun({ text: "Questions about this invoice? Please ", font: FONT, color: COLOR.medGray, size: SIZE.footer }),
    new ExternalHyperlink({ link: `mailto:${email}`, children: [new TextRun({ text: "contact me", color: COLOR.linkBlue, underline: { type: "single" } })] }),
  ] }));

  return new Document({
    styles: { default: { document: { run: { font: FONT, size: SIZE.body } } } },
    sections: [{
      properties: { page: { size: { width: PAGE.width, height: PAGE.height }, margin: { top: PAGE.marginTop, bottom: PAGE.marginBottom, left: PAGE.marginLeft, right: PAGE.marginRight } } },
      children,
    }],
  });
}

// ─── CLI ──────────────────────────────────────────────────────────────────────
async function main() {
  const args = process.argv.slice(2);
  if (args.length < 2) { console.error("Usage: node generate-invoice.js <invoice-data.json> <output.docx>"); process.exit(1); }
  const [dataPath, outputPath] = args;
  const data = JSON.parse(fs.readFileSync(dataPath, "utf-8"));
  const doc = buildInvoice(data);
  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync(outputPath, buffer);
  console.log(`✓ Invoice generated: ${outputPath}`);
}
main().catch(err => { console.error("Error:", err.message); process.exit(1); });

module.exports = { buildInvoice };
