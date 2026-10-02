"""Apply reviewed bibliographic-version corrections to retained working records.
Run after metadata collection and before finalize.py. Idempotent; no network/code execution.
"""
import copy,json,pathlib,re
ROOT=pathlib.Path(__file__).resolve().parents[3]
p=ROOT/'context/acquisition/applications/collected.json'
rows=json.loads(p.read_text());by={r['slug']:r for r in rows}
variants=[('shavelson1993','shavelson-report1993',1993,
 'Sampling Variability of Performance Assessments (CSE Technical Report 361)',
 ['Richard J. Shavelson','Xiaohong Gao','Gail P. Baxter'],
 'https://cresst.org/wp-content/uploads/TECH361.pdf',
 'March 1993 CSE Technical Report 361; report author order is Shavelson, Gao, Baxter. Related September 1993 journal article has different author order and is separately catalogued; this report does not establish acquisition of that final article.'),
 ('bachman1995','bachman-conference1993',1993,
 'Investigating Variability in Tasks and Rater Judgments in a Performance Test of Foreign Language Speaking (1993 conference paper, ERIC ED368154)',
 ['Lyle F. Bachman','Brian K. Lynch','Maureen Mason'],
 'https://eric.ed.gov/?id=ED368154',
 'August 1993 conference paper, ERIC ED368154, Language Testing Research Colloquium 15, Cambridge, 2–4 August 1993. Related 1995 journal article is separately catalogued; this PDF does not establish acquisition of that final article.')]
for original,slug,year,title,authors,url,note in variants:
 r=by[original]
 if slug not in by:
  v=copy.deepcopy(r);v.update(slug=slug,title=title,authors=authors,year=year,doi=None,source_url=url,status='acquired')
  v['evidence_override']='Acquired complete primary report/conference PDF; inspected title page, abstract and selected design discussion. This is a targeted reading of the precursor document, not the final journal article.'
  v['acquisition_note_override']=note;rows.append(v);by[slug]=v
 r.update(status='metadata_only',local_path=None,fulltext_url=None,attempts=[])
 r['evidence_override']='Final journal bibliographic identity verified against publisher-deposited Crossref DOI metadata. Full text of this journal version was not acquired or read; an associated precursor is catalogued separately.'
 r['acquisition_note_override']='Final journal version remains an acquisition gap. See applications-'+slug+' for the independently identified acquired precursor; do not count its PDF as this DOI article.'
by['baldwin2015']['title']=re.sub(r'<[^>]+>','',by['baldwin2015']['title'])
by['teacher-time']['authors']=['Derek C. Briggs','Jessica L. Alzen']
by['fmri-clarification2017']['authors']=['Tyrone D. Cannon','Hengyi Cao','Daniel H. Mathalon','Dylan G. Gee','on behalf of the NAPLS consortium']
p.write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
print('Reviewed versions separated; title markup and primary author metadata corrected.')
