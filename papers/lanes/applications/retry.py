import collect,json,concurrent.futures
rows=json.loads((collect.CONTEXT/'collected.json').read_text())
updates={
 'hill2012':dict(authors=['Heather C. Hill','Charalambos Y. Charalambous','Matthew A. Kraft'],candidates=['https://scholar.harvard.edu/sites/scholar.harvard.edu/files/mkraft/files/hill_charalambous_kraft_2012._when_rater_reliability_is_not_enough_-_edr..pdf']),
 'jackson-confounds2016':dict(title='Everything that you have ever been told about assessment center ratings is confounded',doi='10.1037/apl0000102',authors=['Duncan J. R. Jackson','George Michaelides','Chris Dewberry','Young-Jae Kim']),
 'llm-writing2025':dict(authors=['Dan Song','Won-Chan Lee','Hong Jiao']),
 'llm-writing-journal2025':dict(doi='10.1016/j.caeai.2025.100481'),
 'iced2018':dict(pmc='PMC6044907',candidates=[collect.epmc('PMC6044907')] if hasattr(collect,'epmc') else ['https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6044907/fullTextXML']),
 'rocha2026':dict(pmc='PMC13156807',candidates=['https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13156807/fullTextXML']),
 'rast-clayson2026':dict(pmc='PMC13410726',candidates=['https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13410726/fullTextXML']),
 'selfcompassion2021':dict(doi='10.1007/s12671-020-01522-3',authors=['Oleg N. Medvedev','Anastasia T. Dailianis','Yoon-Suk Hwang','Christian U. Krägeloh','Nirbhay N. Singh']),
 'bachman1995':dict(authors=['Lyle F. Bachman','Brian K. Lynch','Maureen Mason']),
 'baldwin2015':dict(authors=['Scott A. Baldwin','Michael J. Larson','Peter E. Clayson']),
 'putka-hoffman2013':dict(authors=['Dan J. Putka','Brian J. Hoffman']),
 'erp-retest2021':dict(authors=['Peter E. Clayson','Kaylie A. Carbine','Scott A. Baldwin','Joseph A. Olsen','Michael J. Larson']),
 'erp-subject2021':dict(authors=['Peter E. Clayson','Christopher J. Brush','Greg Hajcak'])}
for r in rows:
 r.update(updates.get(r['slug'],{}))
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 rows=list(pool.map(collect.enrich,rows))
def retry(r):
 if r['status']=='acquired':return r
 previous=r.get('attempts',[])
 r.pop('status',None)
 if r.get('pmc') and r['slug'] not in updates:
  r['candidates']=['https://pmc.ncbi.nlm.nih.gov/articles/'+r['pmc']+'/?report=xml']
 r=collect.acquire(r)
 r['attempts']=previous+r['attempts']
 return r
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 rows=list(pool.map(retry,rows))
(collect.CONTEXT/'collected.json').write_text(json.dumps(rows,indent=2))
print(json.dumps({'works':len(rows),'acquired':sum(r['status']=='acquired' for r in rows)}))
