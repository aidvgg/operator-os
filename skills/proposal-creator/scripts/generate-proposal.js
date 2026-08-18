/**
 * LEGACY GENERATOR - SUPERSEDED as the proposal standard 2026-08-02.
 * The standard is generate-proposal-html.js (print HTML -> PDF, design source
 * of record ../references/design-standard-2026-08-02.dc.html). Run this docx
 * generator only when a client needs an editable .docx; validate with
 * scripts/docx-check and run the full SKILL.md verification either way.
 */
/**
 * Northwind Labs Proposal Generator
 *
 * Generates .docx proposals matching the legacy Northwind Labs docx house style.
 *
 * Usage: node generate-proposal.js <proposal-data.json> <output.docx>
 *
 * The JSON file should contain the proposal data structure.
 * See references/data-schema.md for the full schema.
 */

const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  ImageRun, AlignmentType, LevelFormat, ExternalHyperlink,
  HeadingLevel, BorderStyle, WidthType, ShadingType, VerticalAlign,
  PageBreak
} = require("docx");

// ─── RESOLVE ASSET PATHS ────────────────────────────────────────────────────
// Assets are bundled with the skill. Resolve relative to this script.
const SKILL_DIR = path.resolve(__dirname, "..");
const ASSETS_DIR = path.join(SKILL_DIR, "assets");

// ─── BRAND CONSTANTS ────────────────────────────────────────────────────────
const FONT = "Open Sans";
const COLOR = {
  black: "000000",
  darkGray: "2d2d2d",   // Table header background
  medGray: "434343",     // Sub-text, footer pipe text
  lightGray: "666666",   // Subtitle, meta labels
  tableRowAlt: "f2f2f2", // Alternating table row bg
  tableBorder: "cccccc",  // Table cell borders
  white: "ffffff",
  linkBlue: "1155cc",
  sectionBlue: "2e74b5",  // Heading1 style color (not used in proposals but defined)
};

// DXA units: 1440 = 1 inch
const PAGE = {
  width: 12240,   // 8.5in
  height: 15840,  // 11in
  marginTop: 1440,
  marginBottom: 1440,
  marginLeft: 1440,
  marginRight: 1440,
  contentWidth: 9360, // 12240 - 2*1440
};

// EMU units: 914400 = 1 inch
const LOGO = {
  width: 942975,  // ~1.03in
  height: 942975,
};
const DIVIDER_THIN = {
  width: 4457700, // ~4.875in
  height: 19050,
};
const DIVIDER_BOLD = {
  width: 4457700,
  height: 38100,
};

// Font sizes in half-points
const SIZE = {
  companyName: 52,  // 26pt
  subtitle: 30,     // 15pt
  sectionHeading: 32, // 16pt
  subHeading: 28,    // 14pt
  body: 22,          // 11pt
  tableHeader: 21,   // 10.5pt
  tableBody: 21,     // 10.5pt
  sigLabel: 18,      // 9pt
  footer: 22,        // 11pt
};

// ─── IMAGE LOADERS ──────────────────────────────────────────────────────────

function loadImage(filename) {
  const imgPath = path.join(ASSETS_DIR, filename);
  if (!fs.existsSync(imgPath)) {
    throw new Error(`Asset not found: ${imgPath}. Make sure assets/ contains: logo.png, divider-bold.png, divider-thin.png`);
  }
  return fs.readFileSync(imgPath);
}

// ─── REUSABLE ELEMENT BUILDERS ──────────────────────────────────────────────

function logoImage() {
  return new ImageRun({
    data: loadImage("logo.png"),
    transformation: { width: Math.round(LOGO.width / 914400 * 96), height: Math.round(LOGO.height / 914400 * 96) },
    type: "png",
  });
}

function thinDividerImage() {
  return new ImageRun({
    data: loadImage("divider-thin.png"),
    transformation: { width: Math.round(DIVIDER_THIN.width / 914400 * 96), height: Math.round(DIVIDER_THIN.height / 914400 * 96) },
    type: "png",
  });
}

function boldDividerImage() {
  return new ImageRun({
    data: loadImage("divider-bold.png"),
    transformation: { width: Math.round(DIVIDER_BOLD.width / 914400 * 96), height: Math.round(DIVIDER_BOLD.height / 914400 * 96) },
    type: "png",
  });
}

/** Section heading with thin divider underneath (on the same paragraph) */
function sectionHeading(text) {
  return new Paragraph({
    spacing: { after: 120, before: 360 },
    children: [
      new TextRun({
        text: text,
        font: FONT,
        bold: true,
        size: SIZE.sectionHeading,
        color: COLOR.black,
      }),
      thinDividerImage(),
    ],
  });
}

/** Sub-heading (e.g., "SEO Management", "Website Maintenance") */
function subHeading(text) {
  return new Paragraph({
    spacing: { after: 80, before: 320 },
    children: [
      new TextRun({
        text: text,
        font: FONT,
        bold: true,
        size: SIZE.subHeading,
        color: COLOR.medGray,
      }),
    ],
  });
}

/** Normal body paragraph */
function bodyParagraph(text, options = {}) {
  const { bold = false, indent = 0, spacingAfter = 120 } = options;
  return new Paragraph({
    spacing: { after: spacingAfter },
    indent: indent ? { left: indent } : { left: 0, firstLine: 0 },
    children: [
      new TextRun({
        text: text,
        font: FONT,
        size: SIZE.body,
        bold: bold,
      }),
    ],
  });
}

/** Empty spacer paragraph */
function spacer(after = 80) {
  return new Paragraph({ spacing: { after }, children: [] });
}

// ─── TABLE BUILDERS ─────────────────────────────────────────────────────────

const cellBorders = {
  top: { style: BorderStyle.SINGLE, size: 4, color: COLOR.tableBorder },
  bottom: { style: BorderStyle.SINGLE, size: 4, color: COLOR.tableBorder },
  left: { style: BorderStyle.SINGLE, size: 4, color: COLOR.tableBorder },
  right: { style: BorderStyle.SINGLE, size: 4, color: COLOR.tableBorder },
};

const cellMargins = {
  top: 80,
  bottom: 80,
  left: 120,
  right: 120,
};

function headerCell(text, width) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    borders: cellBorders,
    shading: { fill: COLOR.darkGray, type: ShadingType.CLEAR },
    margins: cellMargins,
    children: [
      new Paragraph({
        children: [
          new TextRun({
            text: text,
            font: FONT,
            bold: true,
            color: COLOR.white,
            size: SIZE.tableHeader,
          }),
        ],
      }),
    ],
  });
}

function bodyCell(text, width, options = {}) {
  const { bold = false, isAlt = false, color = COLOR.black } = options;
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    borders: cellBorders,
    shading: isAlt ? { fill: COLOR.tableRowAlt, type: ShadingType.CLEAR } : { fill: COLOR.white, type: ShadingType.CLEAR },
    margins: cellMargins,
    children: [
      new Paragraph({
        children: [
          new TextRun({
            text: text,
            font: FONT,
            size: SIZE.tableBody,
            bold: bold,
            color: color,
          }),
        ],
      }),
    ],
  });
}

/**
 * Build a 2-column service table.
 * @param {string} header1 - First column header (e.g., "Service")
 * @param {string} header2 - Second column header (e.g., "Description")
 * @param {Array<[string, string]>} rows - Array of [col1, col2] pairs
 * @param {number} col1Width - Width of first column in DXA (default 3000)
 */
function serviceTable(header1, header2, rows, col1Width = 3000) {
  const col2Width = PAGE.contentWidth - col1Width;
  return new Table({
    width: { size: PAGE.contentWidth, type: WidthType.DXA },
    columnWidths: [col1Width, col2Width],
    rows: [
      new TableRow({
        children: [
          headerCell(header1, col1Width),
          headerCell(header2, col2Width),
        ],
      }),
      ...rows.map(([c1, c2], i) =>
        new TableRow({
          children: [
            bodyCell(c1, col1Width, { bold: true, isAlt: i % 2 === 1 }),
            bodyCell(c2, col2Width, { isAlt: i % 2 === 1 }),
          ],
        })
      ),
    ],
  });
}

/**
 * Build the investment/pricing table.
 * @param {Array<{description: string, amount: string, bold?: boolean}>} lineItems
 */
function investmentTable(lineItems) {
  const col1Width = 6360;
  const col2Width = 3000;
  return new Table({
    width: { size: PAGE.contentWidth, type: WidthType.DXA },
    columnWidths: [col1Width, col2Width],
    rows: [
      new TableRow({
        children: [
          headerCell("Description", col1Width),
          headerCell("Amount (USD)", col2Width),
        ],
      }),
      ...lineItems.map((item, i) =>
        new TableRow({
          children: [
            bodyCell(item.description, col1Width, { bold: !!item.bold, isAlt: i % 2 === 1 }),
            bodyCell(item.amount, col2Width, { bold: !!item.bold, isAlt: i % 2 === 1 }),
          ],
        })
      ),
    ],
  });
}

/**
 * Build the signature/acceptance table.
 * Two columns: CLIENT and NORTHWIND LABS, each with Signature/Name/Date lines.
 */
function signatureTable() {
  const colWidth = PAGE.contentWidth / 2;
  const noBorders = {
    top: { style: BorderStyle.NONE, size: 0 },
    bottom: { style: BorderStyle.NONE, size: 0 },
    left: { style: BorderStyle.NONE, size: 0 },
    right: { style: BorderStyle.NONE, size: 0 },
  };

  function sigCell(children) {
    return new TableCell({
      width: { size: colWidth, type: WidthType.DXA },
      borders: noBorders,
      margins: cellMargins,
      children: children,
    });
  }

  function sigLabel(text) {
    return new Paragraph({
      spacing: { before: 200 },
      children: [
        new TextRun({ text: text, font: FONT, color: COLOR.lightGray, size: SIZE.sigLabel }),
      ],
    });
  }

  function sigLine() {
    return new Paragraph({
      spacing: { after: 0 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: COLOR.tableBorder, space: 1 } },
      children: [new TextRun({ text: " ", font: FONT, size: 28 })],
    });
  }

  return new Table({
    width: { size: PAGE.contentWidth, type: WidthType.DXA },
    columnWidths: [colWidth, colWidth],
    rows: [
      // Header row
      new TableRow({
        children: [
          sigCell([
            new Paragraph({
              children: [new TextRun({ text: "CLIENT", font: FONT, bold: true, size: SIZE.body })],
            }),
          ]),
          sigCell([
            new Paragraph({
              children: [new TextRun({ text: "NORTHWIND LABS", font: FONT, bold: true, size: SIZE.body })],
            }),
          ]),
        ],
      }),
      // Signature lines
      new TableRow({
        children: [
          sigCell([sigLine(), sigLabel("Signature")]),
          sigCell([sigLine(), sigLabel("Signature")]),
        ],
      }),
      // Name & Title lines
      new TableRow({
        children: [
          sigCell([sigLine(), sigLabel("Name & Title")]),
          sigCell([sigLine(), sigLabel("Name & Title")]),
        ],
      }),
      // Date lines
      new TableRow({
        children: [
          sigCell([sigLine(), sigLabel("Date")]),
          sigCell([sigLine(), sigLabel("Date")]),
        ],
      }),
    ],
  });
}

// ─── MAIN DOCUMENT BUILDER ──────────────────────────────────────────────────

function buildProposal(data) {
  /**
   * data = {
   *   clientName: "Beacon Health",
   *   projectTitle: "12-Month Ops Automation Retainer",
   *   projectDescription: "Ops automation and reporting upkeep, 12-month retainer",
   *   date: "28 Jul 2026",
   *   sentBy: "Sam Rivera",
   *   contactEmail: "sam@northwindlabs.example",
   *   proposalType: "Service Retainer Proposal",  // footer descriptor
   *
   *   overview: "This proposal outlines...",
   *   overviewExtra: "All services will be...",  // optional second paragraph
   *
   *   scopeSections: [
   *     {
   *       title: "Automation upkeep",
   *       services: [
   *         { service: "Run monitoring", description: "Daily checks on every scheduled job..." },
   *       ]
   *     },
   *   ],
   *
   *   investment: {
   *     lineItems: [
   *       { description: "Monthly automation upkeep", amount: "$1,500" },
   *       { description: "Monthly retainer total", amount: "$2,100", bold: true },
   *     ],
   *     note: "All amounts are in US Dollars..."
   *   },
   *
   *   whatThisCovers: [
   *     "All scheduled runs monitored, with failures triaged the same day",
   *   ],
   *
   *   additionalWork: "Any work beyond the scope...",
   *
   *   paymentTerms: [
   *     "$2,100 USD/month, invoiced at the start of each calendar month",
   *   ],
   *
   *   termsAndConditions: [
   *     "Either party may terminate with 30 days' written notice...",
   *   ],
   *
   *   // Optional: custom sections before acceptance
   *   customSections: [
   *     { heading: "TIMELINE", content: "Work will begin..." }
   *   ],
   * }
   */

  const children = [];

  // ── COVER / HEADER ──────────────────────────────────────────────────
  // Logo
  children.push(
    new Paragraph({
      children: [logoImage()],
    })
  );

  // Spacer
  children.push(spacer(60));

  // Company name
  children.push(
    new Paragraph({
      spacing: { after: 60 },
      children: [
        new TextRun({
          text: "NORTHWIND LABS",
          font: FONT,
          bold: true,
          size: SIZE.companyName,
        }),
      ],
    })
  );

  // Project title + thin divider
  children.push(
    new Paragraph({
      spacing: { after: 320 },
      children: [
        new TextRun({
          text: data.projectTitle,
          font: FONT,
          color: COLOR.lightGray,
          size: SIZE.subtitle,
        }),
        thinDividerImage(),
      ],
    })
  );

  // Meta fields
  const metaFields = [
    ["Client: ", data.clientName],
    ["Project: ", data.projectDescription],
    ["Date: ", data.date],
    ["Sent by: ", data.sentBy],
  ];
  for (const [label, value] of metaFields) {
    children.push(
      new Paragraph({
        spacing: { line: 360 },
        children: [
          new TextRun({ text: label, font: FONT, size: SIZE.body }),
          new TextRun({ text: value }),
        ],
      })
    );
  }

  // Spacer + bold divider
  children.push(spacer(80));
  children.push(new Paragraph({ children: [boldDividerImage()] }));

  // ── OVERVIEW ────────────────────────────────────────────────────────
  children.push(spacer(0));
  children.push(sectionHeading("OVERVIEW"));
  children.push(spacer(0));
  children.push(bodyParagraph(data.overview));
  if (data.overviewExtra) {
    children.push(bodyParagraph(data.overviewExtra));
  }

  // ── SCOPE OF WORK ──────────────────────────────────────────────────
  children.push(sectionHeading("SCOPE OF WORK"));
  children.push(spacer(0));

  for (const section of (data.scopeSections || [])) {
    children.push(subHeading(section.title));
    const rows = section.services.map(s => [s.service, s.description]);
    children.push(serviceTable("Service", "Description", rows));
    children.push(spacer(120));
  }

  // ── INVESTMENT ─────────────────────────────────────────────────────
  children.push(sectionHeading("INVESTMENT"));
  children.push(spacer(0));
  children.push(investmentTable(data.investment.lineItems));
  if (data.investment.note) {
    children.push(spacer(60));
    children.push(bodyParagraph(data.investment.note));
  }

  // ── WHAT THIS COVERS ───────────────────────────────────────────────
  if (data.whatThisCovers && data.whatThisCovers.length > 0) {
    children.push(sectionHeading("WHAT THIS COVERS"));
    // These are rendered as a check-mark style list using bullets
    for (const item of data.whatThisCovers) {
      children.push(
        new Paragraph({
          numbering: { reference: "checkBullets", level: 0 },
          spacing: { line: 360, before: 0, after: 0 },
          indent: { left: 720, hanging: 360 },
          children: [
            new TextRun({
              text: item,
              font: FONT,
              size: SIZE.body,
              color: COLOR.black,
            }),
          ],
        })
      );
    }
  }

  // ── ADDITIONAL WORK ────────────────────────────────────────────────
  if (data.additionalWork) {
    children.push(sectionHeading("ADDITIONAL WORK"));
    children.push(
      new Paragraph({
        spacing: { after: 120 },
        indent: { left: 720 },
        children: [
          new TextRun({
            text: data.additionalWork,
            font: FONT,
            size: SIZE.body,
          }),
        ],
      })
    );
  }

  // ── PAYMENT TERMS ──────────────────────────────────────────────────
  if (data.paymentTerms && data.paymentTerms.length > 0) {
    children.push(sectionHeading("PAYMENT TERMS"));
    data.paymentTerms.forEach((term, i) => {
      children.push(
        new Paragraph({
          numbering: { reference: "paymentNumbers", level: 0 },
          spacing: { line: 360, before: 0, after: 0 },
          indent: { left: 720, hanging: 360 },
          children: [
            new TextRun({
              text: term,
              font: FONT,
              size: SIZE.body,
            }),
          ],
        })
      );
    });
  }

  // ── TERMS & CONDITIONS ─────────────────────────────────────────────
  if (data.termsAndConditions && data.termsAndConditions.length > 0) {
    children.push(sectionHeading("TERMS & CONDITIONS"));
    for (const term of data.termsAndConditions) {
      children.push(
        new Paragraph({
          numbering: { reference: "termsBullets", level: 0 },
          spacing: { line: 360, before: 0, after: 0 },
          indent: { left: 720, hanging: 360 },
          children: [
            new TextRun({
              text: term,
              font: FONT,
              size: SIZE.body,
            }),
          ],
        })
      );
    }
  }

  // ── CUSTOM SECTIONS (optional) ─────────────────────────────────────
  if (data.customSections) {
    for (const cs of data.customSections) {
      children.push(sectionHeading(cs.heading));
      if (typeof cs.content === "string") {
        children.push(bodyParagraph(cs.content));
      } else if (Array.isArray(cs.content)) {
        // Array of strings = bullet list
        for (const item of cs.content) {
          children.push(
            new Paragraph({
              numbering: { reference: "customBullets", level: 0 },
              spacing: { line: 360, before: 0, after: 0 },
              indent: { left: 720, hanging: 360 },
              children: [
                new TextRun({ text: item, font: FONT, size: SIZE.body }),
              ],
            })
          );
        }
      }
      // If it has a table property
      if (cs.table) {
        const rows = cs.table.rows.map(r => [r[0], r[1]]);
        children.push(serviceTable(cs.table.headers[0], cs.table.headers[1], rows, cs.table.col1Width || 3000));
      }
    }
  }

  // ── ACCEPTANCE ─────────────────────────────────────────────────────
  children.push(spacer(0));
  children.push(sectionHeading("ACCEPTANCE"));
  children.push(spacer(0));
  children.push(
    bodyParagraph("By signing below, both parties agree to the scope of work, pricing, and terms outlined in this proposal.")
  );
  children.push(spacer(120));
  children.push(signatureTable());

  // ── FOOTER ─────────────────────────────────────────────────────────
  children.push(spacer(200));
  children.push(new Paragraph({ children: [thinDividerImage()] }));
  children.push(spacer(80));

  const proposalType = data.proposalType || "Service Retainer Proposal";
  children.push(
    new Paragraph({
      children: [
        new TextRun({
          text: "NORTHWIND LABS ",
          font: FONT,
          bold: true,
          size: SIZE.footer,
        }),
        new TextRun({
          text: `| ${proposalType}`,
          font: FONT,
          color: COLOR.medGray,
          size: SIZE.footer,
        }),
      ],
    })
  );

  const contactEmail = data.contactEmail || "sam@northwindlabs.example";
  children.push(
    new Paragraph({
      children: [
        new TextRun({
          text: "For questions or clarifications, please ",
          font: FONT,
          color: COLOR.medGray,
          size: SIZE.footer,
        }),
        new ExternalHyperlink({
          link: `mailto:${contactEmail}`,
          children: [
            new TextRun({
              text: "contact me",
              color: COLOR.linkBlue,
              underline: { type: "single" },
            }),
          ],
        }),
      ],
    })
  );

  // ── ASSEMBLE DOCUMENT ──────────────────────────────────────────────
  const doc = new Document({
    styles: {
      default: {
        document: {
          run: { font: FONT, size: SIZE.body },
        },
      },
      paragraphStyles: [
        {
          id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { size: SIZE.sectionHeading, bold: true, font: FONT, color: COLOR.sectionBlue },
          paragraph: { spacing: { before: 240, after: 240 }, outlineLevel: 0 },
        },
        {
          id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { size: SIZE.sectionHeading, bold: false, font: FONT, color: COLOR.black },
          paragraph: { spacing: { after: 120, before: 360 }, outlineLevel: 1 },
        },
        {
          id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { size: SIZE.subHeading, bold: false, font: FONT, color: COLOR.medGray },
          paragraph: { spacing: { after: 80, before: 320 }, outlineLevel: 2 },
        },
      ],
    },
    numbering: {
      config: [
        {
          reference: "checkBullets",
          levels: [{
            level: 0, format: LevelFormat.BULLET, text: "\u2713",
            alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } },
          }],
        },
        {
          reference: "termsBullets",
          levels: [{
            level: 0, format: LevelFormat.BULLET, text: "\u2022",
            alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } },
          }],
        },
        {
          reference: "customBullets",
          levels: [{
            level: 0, format: LevelFormat.BULLET, text: "\u2022",
            alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } },
          }],
        },
        {
          reference: "paymentNumbers",
          levels: [{
            level: 0, format: LevelFormat.DECIMAL, text: "%1.",
            alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } },
          }],
        },
      ],
    },
    sections: [{
      properties: {
        page: {
          size: { width: PAGE.width, height: PAGE.height },
          margin: {
            top: PAGE.marginTop,
            bottom: PAGE.marginBottom,
            left: PAGE.marginLeft,
            right: PAGE.marginRight,
          },
        },
      },
      children: children,
    }],
  });

  return doc;
}

// ─── CLI ENTRY POINT ────────────────────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2);

  if (args.length < 2) {
    console.error("Usage: node generate-proposal.js <proposal-data.json> <output.docx>");
    process.exit(1);
  }

  const [dataPath, outputPath] = args;

  const raw = fs.readFileSync(dataPath, "utf-8");
  const data = JSON.parse(raw);

  const doc = buildProposal(data);
  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync(outputPath, buffer);

  console.log(`✓ Proposal generated: ${outputPath}`);
}

main().catch(err => {
  console.error("Error:", err.message);
  process.exit(1);
});

module.exports = { buildProposal };
