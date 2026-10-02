"""Owned research orchestration; no reference code is executed."""
import concurrent.futures, json, pathlib, subprocess, urllib.request, urllib.parse
ROOT = pathlib.Path('/Users/patrickbeam/projects/crolib')
LANE = ROOT / 'papers/lanes/applications'
CONTEXT = ROOT / 'context/acquisition/applications'
CONTEXT.mkdir(parents=True, exist_ok=True)
def get_json(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent':'crolib-literature-survey/0.1'}), timeout=10) as response:
        return json.load(response)
def enrich(row):
    try:
        if row.get('pmc'):
            results=get_json('https://www.ebi.ac.uk/europepmc/webservices/rest/search?query='+urllib.parse.quote('PMCID:'+row['pmc'])+'&format=json&resultType=core')['resultList']['result']
            if results:
                p=results[0]
                row.update(title=p['title'].rstrip('.'),authors=[a.get('fullName') or ' '.join([a.get('firstName',''),a.get('lastName','')]).strip() or a.get('collectiveName','Unknown collective author') for a in p.get('authorList',{}).get('author',[])],year=int(p['pubYear']),doi=p.get('doi',row.get('doi')))
                row['abstract']=p.get('abstractText','')
                row['metadata_evidence']='Europe PMC primary bibliographic record and abstract'
        elif row.get('doi') and not row['doi'].startswith('10.48550/'):
            p=get_json('https://api.crossref.org/works/'+urllib.parse.quote(row['doi'],safe=''))['message']
            row.update(title=p['title'][0],authors=[' '.join([a.get('given',''),a.get('family','')]).strip() for a in p.get('author',[])])
            row['metadata_evidence']='Publisher-deposited Crossref DOI metadata, plus primary abstract/page when noted'
    except Exception as e:
        row['metadata_failure']=str(e)
    return row
def acquire(row):
    attempts=[]
    for url in row.get('candidates',[]):
        kind='text' if 'fullTextXML' in url else ('html' if url.endswith('/?report=xml') else 'pdf')
        ext='.xml' if kind=='text' else ('.html' if kind=='html' else '.pdf')
        target='papers/downloads/applications/'+row['slug']+ext
        try:
            run=subprocess.run(['python3',str(ROOT/'scripts/acquire.py'),url,target,'--kind',kind,'--timeout','12'],cwd=ROOT,capture_output=True,text=True,timeout=22)
            attempts.append({'url':url,'exit_code':run.returncode,'result':(run.stdout+run.stderr).strip()[-1800:]})
            if run.returncode==0 and kind=='html':
                body=(ROOT/target).read_text(errors='replace')
                if len(body)<30000 or 'Checking your browser before accessing' in body:
                    attempts[-1]['validation']='Not an acquired article; challenge/short HTML'
                    continue
            if run.returncode==0:
                row.update(local_path=target,fulltext_url=url,status='acquired')
                if ext=='.pdf':
                    subprocess.run(['pdftotext','-layout',str(ROOT/target),str(ROOT/target).replace('.pdf','.txt')],capture_output=True,timeout=10)
                break
        except Exception as e:
            attempts.append({'url':url,'error':str(e)})
    row.setdefault('status','access_blocked' if attempts else 'metadata_only')
    row.setdefault('local_path',None)
    row.setdefault('fulltext_url',row.get('candidates',[None])[0] if row.get('candidates') else None)
    row['attempts']=attempts
    return row
if __name__=='__main__':
    rows=json.loads((LANE/'candidates.json').read_text())
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        rows=list(pool.map(enrich,rows))
    (CONTEXT/'enriched.json').write_text(json.dumps(rows,indent=2))
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        rows=list(pool.map(acquire,rows))
    (CONTEXT/'collected.json').write_text(json.dumps(rows,indent=2))
    print(json.dumps({'works':len(rows),'acquired':sum(r['status']=='acquired' for r in rows)}))
