# Data sources

Verified October 8, 2026. All 14 supplied values match GoPro's original SEC filings.
The tables report camera units in thousands. Divide by 1,000 to obtain millions.
The CSV's source IDs identify these filings.

| Source ID | Original filing and table location | Annual observations verified, in thousands |
| --- | --- | --- |
| GPRO_S1_2014 | [GoPro Form S-1, filed May 19, 2014](https://www.sec.gov/Archives/edgar/data/1500435/000119312514204902/d552193ds1.htm), MD&A, Key business metrics, printed p. 56, row Units shipped | 2011: 1,145; 2012: 2,316; 2013: 3,849 |
| GPRO_10K_2016 | [GoPro FY2016 Form 10-K](https://www.sec.gov/Archives/edgar/data/1500435/000150043517000013/gpro2016-12x3110xk.htm), Item 7, MD&A, Revenue, printed p. 39, row Units shipped | 2014: 5,180; 2015: 6,584; 2016: 4,762 |
| GPRO_10K_2018 | [GoPro FY2018 Form 10-K](https://www.sec.gov/Archives/edgar/data/1500435/000150043519000013/gpro2018-12x3110xk.htm), Item 7, MD&A, Revenue, printed p. 48, row Camera units shipped | 2017: 4,303; 2018: 4,337; also confirms 2016: 4,762 |
| GPRO_10K_2020 | [GoPro FY2020 Form 10-K](https://www.sec.gov/Archives/edgar/data/1500435/000150043521000020/gpro-20201231.htm), Item 7, MD&A, Revenue, printed p. 49, row Camera units shipped | 2019: 4,260; 2020: 2,820; also confirms 2018: 4,337 |
| GPRO_10K_2021 | [GoPro FY2021 Form 10-K](https://www.sec.gov/Archives/edgar/data/1500435/000150043522000016/gpro-20211231.htm), Item 7, MD&A, Revenue, row Camera units shipped; also Full year and fourth quarter 2021 financial performance | 2021: 3,145; also confirms 2020: 2,820 and 2019: 4,260 |
| GPRO_10K_2024 | [GoPro FY2024 Form 10-K](https://www.sec.gov/Archives/edgar/data/1500435/000162828025013046/gpro-20241231.htm), Item 7, MD&A, Revenue, printed p. 41, row Camera units shipped | 2022: 2,810; 2023: 2,984; 2024: 2,431 |

Use the annual columns, not Q4 or three-month columns. Comparative-year disclosures allow several years to be checked in one filing. Source IDs in the CSV identify the actual filing used, which can be later than the observation year.

## Definition and limitations

The metric is camera shipments net of returns. The 2014 S-1 and FY2016 report
describe packaged cameras; the FY2018 report explicitly includes cameras bundled
with drones, excluding standalone drones, mounts and accessories. Later reports
retain the net-camera-shipment definition with shorter wording.

Shipments are not unique first-time adopters. They can include repeat purchases,
upgrades and channel inventory. GoPro's S-1 records product launches before 2011,
so the sample starts after diffusion began. Figures cover worldwide GoPro cameras,
not one model or the whole action-camera market.

## Other references

- [TIME: HOVERAir X1 ProMax](https://time.com/collections/best-inventions-2025/7318494/hoverair-x1-promax/), October 9, 2025: product selection.
- `DS-223-Bass-model.pdf`, Karen Hovhannisyan, AUA: Method 1 on slide 34; separate market potential on slide 40.
- [Goldman Sachs](https://www.goldmansachs.com/insights/articles/the-creator-economy-could-approach-half-a-trillion-dollars-by-2027), April 19, 2023: estimated 50 million global creators. This is a dated industry estimate, not a measured HOVERAir audience.
- [HOVERAir launch announcement](https://hoverair.com/blogs/news/hoverair-launches-worlds-first-8k-flying-action-camera), August 26, 2024: campaign timing and $699 ProMax MSRP.

The 10%, 20% and 20% market-size fractions are author-chosen Fermi assumptions,
conditional on each preceding group. They are not published statistics. The forecast
covers the creator segment, uses a fixed market, and assumes no repeat adoption.
The ten-year horizon is an analytical choice.
