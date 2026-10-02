import collect,json,concurrent.futures,urllib.parse
rows=json.loads((collect.CONTEXT/'collected.json').read_text())
extra=[
dict(slug='pharmacy-osce2021',title='Validation evidence from Generalizability Theory for an Objective Structured Clinical Examination',year=2021,doi='10.24926/iip.v12i1.2110',authors=['Michael J. Peeters','Michael K. Cor','Sarah E. Petite','Matthew N. Schroeder'],topics=['pharmacy','OSCE','stations','raters'],relevance='Companion primary pharmacy OSCE application; station/rater design for criterion decisions.'),
dict(slug='pharmacy-quizzes2021',title='Validation evidence from Generalizability Theory for a clinical-science module: Improving test reliability with quizzes',year=2021,doi='10.24926/iip.v12i1.2235',authors=['Michael J. Peeters','Michael K. Cor','Erin D. Maki'],topics=['pharmacy','examinations','quizzes','composites'],relevance='Companion application combining quiz and examination observations for course decisions.'),
dict(slug='lin-guide2015',title='A Practical Guide to Investigating Score Reliability under a Generalizability Theory Framework',year=2015,doi=None,authors=['Chih-Kai Lin'],topics=['language','tutorial','design-planning'],relevance='CaMLA Working Papers 2015-01: applied language-assessment tutorial with worked examples.',source_url='https://michiganassessment.org/wp-content/uploads/2020/02/20.02.pdf.Res_.ApracticalGuidetoInvestigatingScoreReliabilityunderaGeneralizabilityTheoryFramework.pdf',candidates=['https://michiganassessment.org/wp-content/uploads/2020/02/20.02.pdf.Res_.ApracticalGuidetoInvestigatingScoreReliabilityunderaGeneralizabilityTheoryFramework.pdf']),
dict(slug='gee2015',title='Reliability of an fMRI paradigm for emotional processing in a multisite longitudinal study',year=2015,doi='10.1002/hbm.22791',authors=[],topics=['neuroimaging','fMRI','sites','sessions','follow-up-clarification'],relevance='Original traveling-subject emotional-task reliability study; read together with Cannon et al.2018 clarification of target design.',source_url='https://doi.org/10.1002/hbm.22791',candidates=['https://bpb-us-e1.wpmucdn.com/sites.uw.edu/dist/c/18634/files/2022/08/HBM-36-2558.pdf'],pmc='PMC4478164'),
dict(slug='noble2017',title='Influences on the Test–Retest Reliability of Functional Connectivity MRI and its Relationship with Behavioral Utility',year=2017,doi='10.1093/cercor/bhx230',authors=[],topics=['neuroimaging','functional-connectivity','runs','sessions'],relevance='Explicit three-way person/session/run GT plus behavioral utility; acquisition and processing choices can affect reliability and validity differently.')]
def prepare(r):
 if r.get('doi'):
  r['source_url']='https://doi.org/'+r['doi']
  try:
   p=collect.get_json('https://www.ebi.ac.uk/europepmc/webservices/rest/search?query='+urllib.parse.quote('DOI:'+r['doi'])+'&format=json&resultType=core')['resultList']['result']
   if p and p[0].get('pmcid'):
    r['pmc']=p[0]['pmcid'];r['candidates']=['https://www.ebi.ac.uk/europepmc/webservices/rest/'+r['pmc']+'/fullTextXML','https://pmc.ncbi.nlm.nih.gov/articles/'+r['pmc']+'/?report=xml']
  except Exception as e:r['discovery_error']=str(e)
 r.setdefault('candidates',[])
 return collect.acquire(collect.enrich(r))
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 extra=list(pool.map(prepare,extra))
existing={r['slug'] for r in rows}
rows.extend(r for r in extra if r['slug'] not in existing)
for r in rows:
 if r['slug']=='fmri-clarification2017':r=collect.enrich(r)
 if r['slug']=='erp-retest2021':
  old=r.get('attempts',[]);r['candidates']=['https://scholarsarchive.byu.edu/cgi/viewcontent.cgi?article=6836&context=facpub'];r.pop('status',None);r=collect.acquire(r);r['attempts']=old+r['attempts']
(collect.CONTEXT/'collected.json').write_text(json.dumps(rows,indent=2))
print(json.dumps({'works':len(rows),'acquired':sum(r['status']=='acquired' for r in rows)}))
