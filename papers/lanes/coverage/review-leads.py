#!/usr/bin/env python3
"""Apply explicit bibliographic review; retain machine statuses and all rejected candidates."""
import json,re,html
from pathlib import Path
p=Path('papers/lanes/coverage/lead-resolution.json');x=json.loads(p.read_text())
# Each choice is a reviewed metadata identity, never evidence of acquired/read fulltext.
choices={
7:('10.3102/10769986010001019','Publisher and JSTOR register the same title, author, year and journal; retain publisher DOI and alternate DOI.'),
8:('10.3102/10769986011003197','Publisher/JSTOR same bibliographic work; alternate DOI retained.'),
12:('10.3102/10769986007004311','Publisher/JSTOR same bibliographic work; primary publisher DOI independently checked.'),
77:('10.1214/ss/1177013815','Select exact original article title; reject distinct Rejoinder and Comment records.'),
83:('10.1177/002224379703400206','Publisher/JSTOR same title, author, year and journal; alternate DOI retained.'),
92:('10.2307/2530013','Select Biometrics journal article; reject same-title DTIC report as a distinct version.'),
110:('10.3102/00346543047002267','Publisher/JSTOR same 1977 journal article; 1975 ERIC conference report is separately catalogued.'),
153:('10.1111/j.2517-6161.1949.tb00023.x','Royal Statistical Society Series B container agrees with citation; Cambridge Philosophical Society article is distinct.'),
155:('10.1177/002224378702400102','Publisher/JSTOR same title, author, year and journal; alternate DOI retained.'),
156:('10.3102/10769986016003157','Publisher/JSTOR same article. Citation volume 3 is inconsistent with primary registry volume 16.'),
166:('10.1111/j.1745-3984.1993.tb00424.x','Select JEM journal article; PsycEXTRA dataset registration is a distinct record.'),
169:('10.3102/00346543046004553','Publisher/JSTOR same title, author, year and journal; alternate DOI retained.'),
174:('10.1111/j.1745-3984.1991.tb00356.x','Select cited JEM article; same-title ETS report is a distinct version.'),
186:('10.3102/00346543040005663','Publisher/JSTOR same title, author, year and journal; alternate DOI retained.'),
242:('10.1177/0013164404266386','Select journal article; PsycEXTRA dataset record is distinct.'),
6:('10.1177/026553229501200206','Registry print and online dates are 1995; CASMA citation says 1994. Exact title/authors/journal/volume/pages identifies work; catalogue primary year 1995, preserve original citation.'),
69:('10.1177/0013164494054003017','Registry title includes journal section prefix Validity Studies; substantive title, author, year and journal agree.'),
176:('10.3102/10769986003004319','Primary title includes Multifacet omitted in bibliography; title/author/year/journal match reviewed; JSTOR alternate DOI retained.'),
192:('10.1111/1469-8986.3620233','Bibliographic title omits and normal sleepers; reviewed full title/author/year/journal; Cambridge parallel registration retained as candidate.'),
196:('10.1177/0013164411412590','Full DOI registry: online 2011, print June2012; bibliography uses print year.'),
200:('10.1177/0265532214542994','Full DOI registry: online August2014, print January2015; bibliography uses print year.'),
228:('10.1177/0013164414539163','Full DOI registry: online June2014, print April2015; primary ETS and PubMed independently confirm 2015 issue.'),
230:('10.1177/0013164408322005','Full DOI registry: online July2008, print February2009; bibliography uses print year.'),
272:('10.1207/s15328015tlm1801_2','Registry title includes APPLIED RESEARCH journal section prefix; substantive title/author/year/journal agree.'),
275:('10.1177/0013164411408074','Full DOI registry: online July2011, print February2012; bibliography uses print year.'),
286:('10.1177/0265532216638890','Full DOI registry: online August2016, print April2017; bibliography uses print year.'),
290:('10.1177/0146621614563067','Acquired decisions lane author manuscript confirms 2015 journal issue versus 2014 online registry date.'),
296:('10.1177/0013164419846936','Primary University Alabama manuscript cover confirms 2020 issue80(1)67–90, copyright2019/online2019.'),
300:('10.1177/0265532214560257','Primary SAGE page independently verifies online December2014 versus April2015 issue32(2)259–281.'),
313:('10.1177/1073191116641182','Full DOI registry: online April2016, print January2018; bibliography uses print year.'),
315:('10.1080/00223891.2017.1296455','Primary PubMed28418721 verifies online April2017 and print Jan-Feb2018,100(1)53–67.'),
117:('10.1080/00401706.1968.10490601','Parsed title truncated at quoted period; full citation matches primary-registry title/author/year/container.'),
139:('10.1177/001316445701700407','Primary title has plural Standard Errors; reviewed same author/year/journal/pages, distinct1959reply excluded.'),
140:('10.1177/001316445901900208','Primary title lacks terminal question mark; reviewed same author/year/journal, distinct1957question excluded.'),
175:('10.1111/j.1745-3984.1977.tb00050.x','Parsed title truncated at quoted period; full citation matches primary-registry title/author/year/container.'),
281:('10.1002/j.2333-8504.2008.tb02087.x','Primary title includes HTML trademark/superscript markup; cleaned full title/authors/year/ETS report container match.'),
269:('10.1007/978-1-4939-0317-7','Primary registered book title omits subtitle Methods and Practices; title/authors/year/type agree; edition is third2014.')}
for z in x:
 n=int(z['lead_id'].split('-')[-1]);z['machine_resolution_status']=z.get('machine_resolution_status',z['resolution_status'])
 if n in choices:
  doi,note=choices[n];c=next(c for c in z['registry_candidates']if c['doi'].lower()==doi.lower());z.update(resolution_status='reviewed_registry_match',selected_doi=doi,review_note=note)
  cache=Path('context/acquisition/coverage')/(doi.replace('/','-')+'.json')
  if cache.exists():
   v=json.loads(cache.read_text());years=[v[k]['date-parts'][0][0]for k in ['published-print','published-online']if v.get(k,{}).get('date-parts')]
   if z['bibliography_year']in years:z['selected_publication_year']=z['bibliography_year']
  if n in [290,296,300,315]:z['selected_publication_year']=z['bibliography_year']
  z['reviewed_alternate_dois']=[a['doi']for a in z['registry_candidates']if a['doi']!=doi and a['title_similarity']==c['title_similarity'] and a['year']==c['year'] and a['type']==c['type'] and a['container']==c['container'] and a['authors']==c['authors']]
 if n==31:z['review_note']='1996 NCES chapter is acquired within ED399300. Returned 1995 Brennan-and-Johnson journal article is a distinct work; no DOI mapping selected.'
 if n in [211,227]:z['review_note']='Year/edition mismatch unresolved; do not identify bibliography edition with digital DOI edition without further publisher history.'
p.write_text(json.dumps(x,indent=2)+'\n')
from collections import Counter
print(Counter(z['resolution_status']for z in x))
