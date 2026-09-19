---
title: Building your client evidence workbook
description:
  The first tutorial — choose one of the five client homes, build the four-sheet
  workbook every later week writes into, and fill one row of it properly
week: 1
date: 2027-02-25
teachers:
  - harriet-oyelaran
related:
  - lectures/week-01
spec:
  - you have chosen one of the five client homes and written down why
  - your workbook has four sheets — client facts, climate normals, measurement register, assumption log — with the column names given below
  - sheet 1 carries at least eight client facts, each with a status of known, estimate or unknown, and a source
  - sheet 2 carries twelve rows of long-term climate normals with the Bureau of Meteorology station number named
  - sheet 4 carries at least one assumption with its basis and where it came from
  - you can say, without looking it up, which sheet the simulated monitoring year will go on when it arrives in week 7
---

## What this tutorial is for

You are a graduate engineer at Common Ground, and today you pick up a file. By
the end of the session you have a client, a place to keep everything you learn
about them, and one row in it done properly.

**Story stage.** Week 1 of the scoping half. Nothing has been measured. Every
number you write today is either a published figure, a fact the client told you,
or something you have marked as not yet known — and the last category is the one
that eventually becomes Assignment 1.

This week is **ungraded practice**. Nothing is submitted. But weeks 2 to 11 all
write into the workbook you build here, so a student who skips it starts week 2
with nowhere to put the answer.

## What the client evidence workbook is

**It is your own spreadsheet.** Excel, Google Sheets, LibreOffice, Numbers —
whichever you already use. It is not a feature of this website, there is nothing
to log into, and nobody collects it. This site publishes; you compute.

It has **four sheets**, and keeping them separate matters more than anything else
you will do today:

| Sheet | What goes on it | Why it is separate |
|---|---|---|
| 1. Client facts | The home as it is: areas, tenure, inventory, constraints, the client's priorities | These are given. They do not change all semester |
| 2. Climate normals | Twelve rows of long-term Bureau of Meteorology statistics for your home's station | **Sourced long-term averages.** Not this year, not any year — the average of all years of record |
| 3. Measurement register | One row per thing you would measure, and the decision it would settle | This sheet *becomes* Assignment 1 |
| 4. Assumption log | Every number you used but did not measure, with where it came from | So that in week 10 you can still say why a figure is what it is |

**A fifth sheet arrives in week 7** and must not be mixed into sheet 2. That is
the *simulated monitoring year* — a month-by-month record of what a year of
measurement at your home produced. Climate normals say what an average February
does; the monitoring year says what one particular February did. Averaging them
together destroys both.

## Open these first

- **[The five client homes](/clients/)** — five intake dossiers. You are choosing
  one of these and keeping it for the whole course.
- **The CSV templates** below. Download all four; they carry the column names and
  one worked example row each.
- **[The measurement primer](/method/measurement/)** — you do not need it today,
  but sheet 3's columns come from it.

### Download the templates

| Sheet | File |
|---|---|
| 1. Client facts | [TEMPLATE-1-client-facts.csv](/data/workbook/TEMPLATE-1-client-facts.csv) |
| 2. Climate normals | [TEMPLATE-2-climate-normals.csv](/data/workbook/TEMPLATE-2-climate-normals.csv) |
| 3. Measurement register | [TEMPLATE-3-measurement-register.csv](/data/workbook/TEMPLATE-3-measurement-register.csv) |
| 4. Assumption log | [TEMPLATE-4-assumption-log.csv](/data/workbook/TEMPLATE-4-assumption-log.csv) |

Open each in your spreadsheet program and paste it into its own sheet of one
file. Each template's first line is a comment describing the sheet; keep it or
delete it, it does not matter. The next row contains the column headings.
Below those are Canberra example values and blank rows. Keep the headings,
remove the example marker where present, and replace the example values with
your own home's values.

If you would rather type the sheets out than download them, the column names are
in the tables below and that is all the templates contain.

## Do this

**1. Choose your home (10 minutes).** Open [the clients page](/clients/) and read
the five intake notes. Five presets, no cap on how many students take each.
Different constraints make different homes easier or harder in context; the
site-specific reference bands are a diagnostic comparison, not proof of equal
grading outcomes. Write your choice and one sentence of reason on sheet 1.

**2. Fill sheet 1 from the dossier (25 minutes).** Your home's page carries
everything on this sheet. Eight rows minimum. Every row needs a **status** and a
**source**:

- **known** — the dossier states it. Source: the clients page.
- **estimate** — the dossier states it *and says it is an estimate*, like the
  slope read off a contour map. Copy that word across; do not promote it.
- **unknown** — the dossier lists it under "what nobody yet knows". Enter the row
  with an empty value. **These rows are the seed of Assignment 1.**

Here is the whole of the example row set, for the Canberra home, from
[its dossier](/clients/canberra/):

| field | value | unit | status | source |
|---|---|---|---|---|
| client_home | Canberra (Taylor) | | known | /clients/canberra/ |
| household | two adults and two children aged 9 to 13 | persons | known | course demand convention |
| parcel_area | 800 | m² | known | /clients/canberra/ |
| roof_plan_area | 295.7 | m² | known | /clients/canberra/ |
| roof_connected_to_storage_now | 41.6 | m² | known | /clients/canberra/ |
| growing_envelope | 442.9 | m² | known | /clients/canberra/ |
| existing_storage | 5 | kL | known | /clients/canberra/ (2009 poly tank, garage roof) |
| slope | 3 | % fall to street | **estimate** | ACT contour map, via the dossier |
| soil_texture_zone_G1 | *(blank)* | texture class | **unknown** | to be measured |

Note the third and fourth rows. **Roof plan area is 295.7 m² and the roof
connected to storage is 41.6 m².** They are different quantities and a design
that confuses them is wrong by a factor of seven. Keep them as separate rows for
the rest of the course.

**3. Fill sheet 2 — twelve rows of climate normals (30 minutes).** Your home's
long-term statistics are published as a CSV, one per home. They are sourced from
the Bureau of Meteorology for your home's station, and the file's first line says
so.

| Home | Station | File |
|---|---|---|
| Canberra | 070014 | [BOM-long-term-070014.csv](/data/release-b/canberra/BOM-long-term-070014.csv) |
| Alice Springs | 015590 | [BOM-long-term-015590.csv](/data/release-b/alice-springs/BOM-long-term-015590.csv) |
| Brisbane | 040214 | [BOM-long-term-040214.csv](/data/release-b/brisbane/BOM-long-term-040214.csv) |
| Adelaide | 023000 | [BOM-long-term-023000.csv](/data/release-b/adelaide/BOM-long-term-023000.csv) |
| Darwin | 014015 | [BOM-long-term-014015.csv](/data/release-b/darwin/BOM-long-term-014015.csv) |

These files sit in the same folder the week 7 findings will come from. **They are
not part of the measured year.** The sourced file's first line begins
`# SOURCED:`; every synthetic file's begins `# SYNTHETIC`. Learn to look at line
one before you use a file — it is the habit this course cares about most.

The Canberra January row, filled:

| month | rain_mm | tmax_c | tmin_c | eto_mm | effective_rain_mm | source |
|---|---|---|---|---|---|---|
| Jan | 58.5 | 28.0 | 13.2 | 186 | 25.1 | BoM station 070014, all years of record |

Check the units as you go. `rain_mm` is a monthly **total** in millimetres;
`eto_mm` is monthly **reference evapotranspiration**, also millimetres — the
depth of water a reference grass surface would lose in that month. `tmax_c` is
the mean daily maximum, not the hottest day ever recorded. **`effective_rain_mm`
is always smaller than `rain_mm`**: it is the part that reaches the roots, after
runoff and deep drainage. Week 2's lecture derives it. If your sheet ever shows
effective rain equal to or greater than total rain, you have pasted a column into
the wrong place.

**4. Start sheet 4 with one assumption (10 minutes).** Every course-supplied
number that is not a measurement goes here. Start with the demand convention,
which is the one you will use every week:

| id | the_figure | value | unit | basis | where_it_came_from | date |
|---|---|---|---|---|---|---|
| A01 | indoor water use per person | 150 | L/person/day | course assumption | course demand convention, /method/ | 2027-02-25 |

**5. Swap and find the unsourced row (15 minutes).** Trade workbooks with
somebody on a different home. Find one row on theirs with no source, or with a
status that flatters it. There is always one. That is the entire exercise and it
is the reason the swap is in the session rather than the homework.

## The output

**A four-sheet client evidence workbook**, with one home chosen, sheet 1 filled
from the dossier, twelve sourced rows on sheet 2, and at least one assumption
logged on sheet 4.

## Check your own before you leave

Run these on your own file, in order:

1. Does every row on sheet 1 have a status **and** a source?
2. Is there at least one row with status `unknown` and an empty value?
3. Does sheet 2 have exactly twelve rows and a station number?
4. On sheet 2, is `effective_rain_mm` less than `rain_mm` in every one of the
   twelve rows?
5. Do roof plan area and connected roof area appear as two different rows with
   two different numbers?
6. Could someone else open your file and say where any single number came from?

## Where it goes next

Week 2 computes an irrigation demand curve from sheet 2 and writes the result
beside it. Every tutorial from here to week 11 opens the same file.

You keep the workbook; nobody collects it. Bring it to every session.
