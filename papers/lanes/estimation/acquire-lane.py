"""Research-only catalogue builder; downloads sources without running their code."""
import concurrent.futures
import importlib.util
import json
from pathlib import Path
import urllib.request
import urllib.parse
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('acquire', ROOT / 'scripts/acquire.py')
acquisition = importlib.util.module_from_spec(spec)
spec.loader.exec_module(acquisition)
lane = ROOT / 'papers/lanes/estimation'

def process(candidate):
    slug, doi, fulltext, relevance = candidate
    logs = []
    metadata = {}
    if doi:
        url = 'https://api.crossref.org/works/' + urllib.parse.quote(doi, safe='')
        try:
            with urllib.request.urlopen(url, timeout=25) as response:
                metadata = json.load(response)['message']
            logs.append({'url':url,'result':'metadata_verified'})
        except Exception as error:
            logs.append({'url':url,'result':'failed','reason':str(error)})
    extension = 'html' if 'pmc.ncbi' in fulltext else 'pdf'
    destination = ROOT / 'papers/downloads/estimation' / (slug+'.'+extension)
    result = None
    try:
        if destination.exists():
            result = json.loads(destination.with_name(destination.name+'.source.json').read_text())
        else:
            completed = subprocess.run([sys.executable,str(ROOT/'scripts/acquire.py'),fulltext,str(destination),'--kind',extension,'--timeout','12'],capture_output=True,text=True,timeout=20)
            if completed.returncode:
                raise ValueError(completed.stderr.strip())
            result=json.loads(completed.stdout)
        logs.append({'url':fulltext,'result':'acquired','path':str(destination.relative_to(ROOT))})
    except Exception as error:
        logs.append({'url':fulltext,'result':'failed','reason':str(error)})
    date = metadata.get('published-print',metadata.get('published',metadata.get('published-online',{}))).get('date-parts',[[None]])[0][0]
    record = {'id':'estimation-'+slug,'title':metadata.get('title',[slug])[0],
              'authors':[' '.join(filter(None,[a.get('given'),a.get('family')])) for a in metadata.get('author',[])],
              'year':date, 'doi':doi, 'source_url':metadata.get('URL',fulltext),'fulltext_url':fulltext,
              'local_path':str(destination.relative_to(ROOT)) if result else None,
              'status':'acquired' if result else 'access_blocked',
              'topics':['variance-components','generic-foundation' if 'foundation' in relevance else 'generalizability-theory'],
              'relevance':relevance,
              'evidence':'Publisher/university abstract or metadata inspected; downloaded bytes not yet substantively read.' if metadata else 'Search primary-source listing inspected; metadata needs manual confirmation.',
              'acquisition_note':'Local research copy; do not redistribute acquired article without checking its license.' if result else logs[-1]['reason']}
    return record,logs

if __name__=='__main__':
    candidates=json.loads((lane/'candidates.json').read_text())
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        results=[]
        for result in pool.map(process,candidates):
            results.append(result)
            (lane/'catalogue.json').write_text(json.dumps([r for r,l in results],indent=2)+'\n')
            (lane/'search-log.json').write_text(json.dumps([{'id':r['id'],'attempts':l} for r,l in results],indent=2)+'\n')
    (lane/'catalogue.json').write_text(json.dumps([r for r,l in results],indent=2)+'\n')
    (lane/'search-log.json').write_text(json.dumps([{'id':r['id'],'attempts':l} for r,l in results],indent=2)+'\n')
    print(json.dumps({'records':len(results),'acquired':sum(r['status']=='acquired' for r,l in results)}))
