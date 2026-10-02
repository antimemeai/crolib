"""Produce compact, reviewed application-lane catalogue and acquisition log."""
import json,pathlib,collections
ROOT=pathlib.Path('/Users/patrickbeam/projects/crolib')
LANE=ROOT/'papers/lanes/applications'
rows=json.loads((ROOT/'context/acquisition/applications/collected.json').read_text())
notes={
 'shavelson1993':'Acquired original CRESST CSE Technical Report361, March1993, associated with the journal article. Its author ordering differs from the journal citation; it is not asserted to be the exact publisher version.',
 'bachman1995':'Acquired ERIC ED368154 deposited conference-paper version from the 1993 Language Testing Research Colloquium; catalogue cites the1995 journal article. Version/pagination differences may matter.',
 'jackson2022':'University of East Anglia author manuscript acquired; journal metadata verified against New Zealand Journal of Psychology51(2),53–64(2022). No DOI identified.',
 'jackson-confounds2016':'Birkbeck accepted manuscript acquired; title and DOI corrected against header and King’s College London primary publication record.',
 'lin-guide2015':'Cambridge Michigan Language Assessments primary working-paper PDF acquired; abstract/method sections compare rating-slot and rater-block transformations for sparse ratings.',
 'judge2026':'arXiv preprint PDF acquired. Full crossed judgment dataset, calculator and audit code are author-on-request according to the PDF; no public release was acquired. The arXiv abstract and PDF contain differing numerical counts, so no count is treated as independently validated.',
 'brand2026':'arXiv preprint PDF acquired. Zenodo links describe aggregate data; response-level iteration inputs are available only on reasonable request according to the PDF. Appendix code is present in the paper, but no complete response-level replication bundle is acquired.',
 'ddr2026':'arXiv preprint PDF acquired; root separately pinned agent-reliability-engineering-lab source archive. Gaussian/binary variance-scale comparability and omitted interactions need independent review before use as numerical reference.',
 'liu-gt2026':'SSRN fulltext delivery blocked. Primary SSRN abstract and root-pinned Gtheory4LLM documentation/data provenance inspected; public annotation OSF deposit K9CAJ linked. No full manuscript review is claimed.',
 'rocha2026':'Primary author-manuscript fulltext XML acquired from Europe PMC after publisher PDF access failed. Original publisher identifies article as open access.',
 'rast-clayson2026':'Primary author-manuscript fulltext XML acquired from Europe PMC; associated public OSF5rn6u data/code separately acquired as eeg-location-scale reference files.',
 'iced2018':'Primary fulltext XML acquired. OSFt68my worked myelin CSV and OSF8n24x derived resting-state connectivity CSVs separately acquired; see software records.',
 'fmri-clarification2017':'Primary PMC HTML fulltext acquired. Record year is2018 issue publication although the stable internal slug retains2017 from online-publication discovery.',
 'connectomic2017':'Primary PMC HTML fulltext acquired. Record year is2019 issue publication; stable slug retains an earlier discovery-year label.'}
catalogue=[]
for r in rows:
 acquired=r['status']=='acquired'
 evidence=('Primary full text acquired; inspected title/author metadata, abstract or introductory passages, and selected design/variance discussion excerpts. This is a targeted reading, not an end-to-end mathematical validation.' if acquired else 'Primary bibliographic metadata and available publisher/author abstract or preview inspected; no local full text acquired.')
 if r['slug']=='putka-hoffman2013':evidence='Publisher DOI metadata plus primary follow-on paper citation/discussion inspected; original full text blocked. Original-method details remain a reading gap.'
 if r['slug']=='briesch2014':evidence='Primary publisher abstract, introduction, and worked student-engagement example preview inspected; PDF acquisition blocked.'
 if r['slug']=='liu-gt2026':evidence='Primary SSRN abstract/metadata and author-maintained Gtheory4LLM README and validation-scope documentation inspected; fulltext delivery blocked.'
 evidence=r.get('evidence_override',evidence)
 attempts=r.get('attempts',[])
 failures=sum(bool(a.get('error')) or a.get('exit_code',0)!=0 or bool(a.get('validation')) for a in attempts)
 note=notes.get(r['slug'],'Original primary or author-deposited fulltext bytes preserved with adjacent source_url/final_url/SHA-256/byte-count acquisition record.' if acquired else 'Fulltext requests failed or returned a challenge. See search-log.json for exact attempted URLs and error output; institutional/author access may be needed.')
 note=r.get('acquisition_note_override',note)
 if failures:note+=' Failed attempts recorded: '+str(failures)+'.'
 catalogue.append(dict(id='applications-'+r['slug'],title=r['title'].rstrip('.'),authors=r['authors'],year=r['year'],doi=r.get('doi'),source_url=r['source_url'],fulltext_url=r.get('fulltext_url'),local_path=r.get('local_path'),status=r['status'],topics=r['topics'],relevance=r['relevance'],evidence=evidence,acquisition_note=note))
(LANE/'catalogue.json').write_text(json.dumps(catalogue,indent=2,ensure_ascii=False)+'\n')
queries=[
 'generalizability theory education performance assessment Shavelson Baxter Gao1993 pdf',
 'generalizability theory language assessment In nami Koizumi2016 tasks raters meta analysis',
 'generalizability theory workplace assessment Crossley Davies Humphris Jolly2002',
 'generalizability theory neuroimaging fMRI reliability generalizability study',
 'generalizability theory personality state trait Medvedev generalizability mindfulness',
 'generalizability theory information retrieval Urbano Marrero Mizzaro test collection reliability',
 'generalizability theory ERP Clayson Miller2017 reliability toolbox DOI',
 'generalizability theory Baldwin2015 ERP personality reliability',
 'generalizability theory Big Five Inventory Arterberry Martens Cadigan2014',
 'Lakes Hoyt2009 generalizability theory child behavior reliability',
 'Briesch Swaminathan Welsh Chafouleas2014 generalizability practical guide pdf uconn',
 'Generalizability theory for the perplexed pdf mcmaster',
 'Beyond classical metrics pdf Rocha',
 'generalizability LLM reliability fairness',
 'Generalizability OSCE1998 Regehr checklist global',
 'Generalizability workplace Crossley2011',
 'Clarifying the Scope G Theory Jackson2022',
 'Generalizability theory Bachman Lynch Mason',
 'A review of Generalizability Theory1976 2013',
 'generalizability Putka Hoffman2013',
 'generalizability Urbano2015 robustness statistical assumptions',
 'Hill Charalambous Kraft2012 generalizability',
 'On the Measurement of Test Collection Reliability doi pdf',
 'Assessing reliability in neuroimaging research ICED PMC',
 'Generalizability theory Briesch filetype:pdf site:neu.edu',
 'Generalizability theory for the perplexed filetype:pdf site:edu',
 'Task and rater effects pdf site:ac.jp',
 'When Rater Reliability Is Not Enough filetype:pdf site:edu',
 'Measuring Mindfulness Medvedev filetype:pdf site:ac.nz',
 'ERP Reliability Analysis pdf Clayson Miller2017',
 'Enhancing generalizability theory Rast pdf',
 'Everything That You Have Ever Been Told Jackson2016 doi',
 'ERP Reliability Analysis filetype:pdf site:peterclayson.com',
 'test-retest reliability of ERP scores part1 filetype:pdf site:edu',
 '10.24926/iip.v12i1.2110 PMC',
 '10.24926/iip.v12i1.2235 PMC',
 'A Practical Guide to Investigating Score Reliability Lin2015',
 'Reliability of an fMRI paradigm Clarification authors doi',
 'Influences on the Test–Retest Reliability doi',
 'Reliability of an fMRI paradigm for emotional processing2015 DOI']
log=dict(lane='applications',searched_at='2026-10-02',scope='Education/performance/language/medical OSCE/workplace/personality/state-trait/psychophysiology/neuroimaging/information retrieval/AI evaluations',search_log_kind='Query-family synopsis with exact per-URL acquisition attempts; not a raw browser-event transcript',query_families=queries,discovery_sources=['primary publisher pages','author university repositories','NIH PubMed/PMC','Europe PMC API','Crossref publisher-deposited metadata','ERIC','CRESST','arXiv','SSRN','author-maintained reference READMEs and bibliographies'],bibliography_expansion=['Pharmacy primer refs42–44 -> OSCE/exams/quizzes companions','PsyRAT bibliography -> ERA2017/retest2021/subject2021/difference2021/Rocha2026/Rast2026','gt4ireval README -> Urbano2013 -> Urbano2016 stochastic robustness','ICED primary fulltext -> OSFt68my and8n24x','Rast2026 primary fulltext -> OSF5rn6u','Mindfulness2017 publisher references -> BFI2014 and state/trait distinctions'],metadata_corrections=['Guessed Noble DOI bhx109 resolved to unrelated paper; rejected and replaced with verified bhx230. No unrelated paper remains in catalogue.','Jackson2016 manuscript header corrected provisional title; primary KCL record verifies10.1037/apl0000102.','Lin2015 guide is a primary sparse-rating simulation comparison, not merely a generic introduction.','EPMC query field corrected from EXT_ID to PMCID; author-consortium metadata handled explicitly.','Stable internal discovery slugs retain earlier years, but catalogue uses verified issue-publication years.'],acquisitions=[dict(id='applications-'+r['slug'],status=r['status'],attempts=r.get('attempts',[]),metadata_failure=r.get('metadata_failure')) for r in rows],dataset_sources=['https://osf.io/t68my/','https://osf.io/5rn6u/','https://osf.io/8n24x/'],data_corrections=['OSFt68my contains one myelin CSV, not a methods/code bundle.','OSF8n24x contains small derived edge CSVs, not raw neuroimages; initial100-file default cap extended to200 with parent authorization.'],limitations=['Representative systematic domain map, not a complete census of every application paper.','Local fulltext failures do not imply legal unavailability; publisher challenges,404s,timeouts and author-request materials distinguished in attempts.','No downloaded reference code executed; no dependency adopted.','Full raw working bibliographic responses retained in ignored context/acquisition/applications.'])
search_path=LANE/'search-log.json'
if search_path.exists():
 previous=json.loads(search_path.read_text())
 for key in ['data_corrections','metadata_corrections','bibliography_expansion','limitations']:
  log[key]=list(dict.fromkeys(log[key]+previous.get(key,[])))
log['reference_acquisition']=[]
for identifier in ['iced-methods','eeg-location-scale','iced-example-data']:
 record_path=pathlib.Path('papers/software/records')/(identifier+'.json')
 if not (ROOT/record_path).exists():continue
 record=json.loads((ROOT/record_path).read_text())
 log['reference_acquisition'].append(dict(id=identifier,source_url=record['source_url'],
  files_acquired=len(record['files']),failed_files=record.get('failed_files',[]),
  bytes=sum(f['bytes'] for f in record['files']),record_path=str(record_path),
  listing_url=record.get('listing_url'),listed_entries=record.get('listed_entries'),
  duplicate_file_ids=record.get('duplicate_file_ids',[]),path_conflicts=record.get('path_conflicts',[])))
if search_path.exists():
 log['reference_acquisition'] += [item for item in previous.get('reference_acquisition',[])
  if item['id'] not in {entry['id'] for entry in log['reference_acquisition']}]
search_path.write_text(json.dumps(log,indent=2,ensure_ascii=False)+'\n')
assert len({r['id'] for r in catalogue})==len(catalogue)
for r in catalogue:
 assert r['authors'] and r['title'] and r['source_url']
 if r['status']=='acquired':assert (ROOT/r['local_path']).is_file()
print(dict(collections.Counter(r['status'] for r in catalogue)),len(catalogue))
