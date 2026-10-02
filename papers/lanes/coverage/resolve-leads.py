#!/usr/bin/env python3
"""Read-only primary-registry audit of a finite author bibliography; never acquire candidate fulltexts."""
import concurrent.futures,json,re,time,urllib.error,urllib.parse,urllib.request,threading,unicodedata
from pathlib import Path
from difflib import SequenceMatcher
leads=json.loads(Path('papers/bibliography-leads.json').read_text())
prior={x['lead_id']:x for x in json.loads(Path('papers/bibliography-coverage.json').read_text())}
lock=threading.Lock();last=[0.]
def norm(s):return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',s.lower()).encode('ascii','ignore').decode())
def f(x):
 citation=x['citation'];r={'lead_id':x['id'],'citation':citation,'bibliography_year':x['year'],'mechanical_catalogue_candidates':prior[x['id']]['candidate_catalogue_ids']}
 cache=Path('context/acquisition/coverage')/(x['id']+'.json')
 query=urllib.parse.urlencode({'rows':3,'query.bibliographic':citation,'select':'DOI,title,author,published,type,container-title,URL,link'})
 u='https://api.crossref.org/works?'+query;r['registry_query_url']=u
 data=None
 for attempt in range(3):
  try:
   if cache.exists():data=json.loads(cache.read_text());break
   with lock:
    pause=max(0,1.2-(time.monotonic()-last[0]));time.sleep(pause);last[0]=time.monotonic()
   req=urllib.request.Request(u,headers={'User-Agent':'crolib-bibliography-audit/0.1','Accept':'application/json'})
   data=json.load(urllib.request.urlopen(req,timeout=25));cache.write_text(json.dumps(data,indent=2));break
  except Exception as e:
   r['error']=str(e)
   if '429' not in str(e):break
   time.sleep(5*(attempt+1))
 if data is None:r['resolution_status']='registry_error';return r
 r.pop('error',None)
 m=re.search(r'\(\d{4}[a-z]?[^)]*\)\.?\s*(.+)',citation)
 leadtitle=m.group(1).split('. ')[0].strip() if m else citation
 first=citation.split(',')[0]
 cand=[]
 for z in data['message']['items']:
  title=' '.join(z.get('title',[]));authors=[(a.get('given','')+' '+a.get('family','')).strip() for a in z.get('author',[])]
  year=(z.get('published',{}).get('date-parts') or [[None]])[0][0]
  nt,nl=norm(title),norm(leadtitle)
  score=SequenceMatcher(None,nt,nl).ratio()
  auth=bool(authors and norm(first) in norm(authors[0]))
  candidate={'title':title,'authors':authors,'year':year,'doi':z['DOI'],'source_url':z.get('URL'),'type':z.get('type'),'container':z.get('container-title',[]),'links':z.get('link',[]),'title_similarity':round(score,4),'first_author_agrees':auth,'year_difference':None if year is None or x['year'] is None else year-x['year']}
  cand.append(candidate)
 r['parsed_lead_title']=leadtitle;r['registry_candidates']=cand
 good=[z for z in cand if z['title_similarity']>=.94 and z['first_author_agrees'] and z['year_difference']==0]
 close=[z for z in cand if z['title_similarity']>=.90 and z['first_author_agrees'] and z['year_difference'] is not None and abs(z['year_difference'])<=2]
 if len(good)==1:r['resolution_status']='strong_registry_match';r['selected_doi']=good[0]['doi'];r['note']='Title/firstauthor/year match registry; metadata evidence only, no fulltext claim. Check edition/version before merging.'
 elif len(good)>1:r['resolution_status']='ambiguous_registry_match';r['note']='Multiple matching records; do not select automatically.'
 elif close:r['resolution_status']='candidate_needs_review';r['note']='Title/author close but year or typography differs; not counted as verified.'
 else:r['resolution_status']='unresolved_registry';r['note']='No sufficiently specific title/author/year registry match in three returned candidates.'
 return r
results=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 for i,z in enumerate(pool.map(f,leads),1):
  results.append(z)
  if i%20==0 or i==len(leads):
   Path('papers/lanes/coverage/lead-resolution.json').write_text(json.dumps(results,indent=2)+'\n');print('Resolved',i,flush=True)
from collections import Counter
print(Counter(z['resolution_status'] for z in results))
