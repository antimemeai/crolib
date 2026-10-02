import json
from pathlib import Path

lane=Path(__file__).parent
root=lane.resolve().parents[2]
records=json.loads((lane/'catalogue.json').read_text())
logs=json.loads((lane/'search-log.json').read_text())
for record,attempts in json.loads((lane/'extras.json').read_text()):
    if not any(r['id']==record['id'] for r in records):records.append(record)
    logs.append({'id':record['id'],'attempts':attempts})

# Hand verification against the primary publisher/university/ERIC pages and
# acquired article headers, for Crossref responses unavailable in this pass.
verified={
'henderson-1953':('Estimation of Variance and Covariance Components',['C. R. Henderson'],1953),
'hartley-rao-1967':('Maximum-likelihood estimation for the mixed analysis of variance model',['H. O. Hartley','J. N. K. Rao'],1967),
'rao-linear-models-1972':('Estimation of Variance and Covariance Components in Linear Models',['C. R. Rao'],1972),
'corbeil-searle-1976':('Restricted Maximum Likelihood (REML) Estimation of Variance Components in the Mixed Model',['R. R. Corbeil','S. R. Searle'],1976),
'brennan-variance-1994':('Variance Components in Generalizability Theory',['Robert L. Brennan'],1994),
'chiu-wolfe-sparse-2002':('A Method for Analyzing Sparse Data Matrices in the Generalizability Theory Framework',['Christopher W. T. Chiu','Edward W. Wolfe'],2002),
'marcoulides-sem-1996':('Estimating variance components in generalizability theory: The covariance structure analysis approach',['George A. Marcoulides'],1996),
'jiang-lme4-2018':('Using the Linear Mixed-Effect Model Framework to Estimate Generalizability Variance Components in R: A lme4 Package Application',['Zhehan Jiang'],2018),
'lopilato-bayes-2015':('Updating Generalizability Theory in Management Research: Bayesian Estimation of Variance Components',['Alexander C. LoPilato','Nathan T. Carter','Mo Wang'],2015),
'gelman-priors-2006':('Prior distributions for variance parameters in hierarchical models',['Andrew Gelman'],2006),
'ten-hove-multilevel-2022':('Interrater Reliability for Multilevel Data: A Generalizability Theory Approach',['Debby ten Hove','Terrence D. Jorgensen','L. Andries van der Ark'],2022),
'ten-hove-incomplete-2025':('How to Estimate Intraclass Correlation Coefficients for Interrater Reliability from Planned Incomplete Data',['Debby ten Hove','Terrence D. Jorgensen','L. Andries van der Ark'],2025),
'huebner-lucht-r-2019':('Generalizability Theory in R',['Alan Huebner','Marisa Lucht'],2019),
'huebner-mixed-2025':('Mixed Model Generalizability Theory: A Case Study and Tutorial',['Alan Huebner','Gustaf B. Skar','Mengchen Huang'],2025),
'jiang-auxiliary-2018':('Improving generalizability coefficient estimate accuracy: A way to incorporate auxiliary information',['Zhehan Jiang','Kevin Walker','Dexin Shi','Jian Cao'],2018),
'laenen-repeated-2006':('Generalized reliability estimation using repeated measurements',['Annouschka Laenen','Tony Vangeneugden','Helena Geys','Geert Molenberghs'],2006),
'molenberghs-hierarchical-2007':('Estimating reliability and generalizability from hierarchical biomedical data',['Geert Molenberghs','Annouschka Laenen','Tony Vangeneugden'],2007),
'bates-lme4-2015':('Fitting Linear Mixed-Effects Models Using lme4',['Douglas Bates','Martin Mächler','Ben Bolker','Steve Walker'],2015),
'jiang-ci-2022':('A Monte Carlo Study of Confidence Interval Methods for Generalizability Coefficient',['Zhehan Jiang','Mark Raymond','Christine DiStefano','Dexin Shi','Ren Liu','Junhua Sun'],2022),
'rockwood-jeon-2022':('Modern applications of cross-classified random effects models in social and behavioral research: Illustration with R package PLmixed',['Sijia Huang','Minjeong Jeon'],2022),
'laenen-thesis-2008':('Psychometric Validation of Continuous Rating Scales from Complex Data',['Annouschka Laenen'],2008),
'huynh-incomplete-1977':('Estimation of the KR20 Reliability Coefficient When Data Are Incomplete',['Huynh Huynh'],1977),
'choi-dissertation-2013':('Advances in Combining Generalizability Theory and Item Response Theory',['Jinnie Choi'],2013),
'swallow-monahan-1984':('Monte Carlo Comparison of ANOVA, MIVQUE, REML, and ML Estimators of Variance Components',['William H. Swallow','John F. Monahan'],1984)
}
read={
'henderson-1953':'Acquired scanned PDF; bibliographic cover inspected. Primary university indexed introduction read through web search; body lacks a searchable text layer. Full mathematical paper not yet read.',
'corbeil-searle-1976':'Local fulltext: abstract and introductory likelihood partition/model sections read; remaining derivations not yet audited.',
'harville-1977':'Local fulltext: section 8.2 ANOVA-like methods, MINQUE/REML relationship, and constraints/numerical passages read; not a full-paper audit.',
'gelman-priors-2006':'Local fulltext abstract and introduction read; variance-prior recommendation checked against author-hosted primary PDF.',
'self-liang-1987':'Primary author-university abstract read and local PDF acquired; full proof not yet audited.',
'jiang-skorupski-bayes-2018':'Local fulltext: model/design, BUGS data mapping, simulated missingness example, supplementary ZIP location and prior discussion read; code not executed.',
'jiang-mixed-format-2024':'Local fulltext: joint Stan construction, covariance mapping, application, data-dependent prior procedure and OSF availability read; code not executed.',
'ten-hove-multilevel-2022':'Primary fulltext model decomposition, ICC formulas, fixed/random discussion and estimation sections read. Article and mathematical supplement acquired.',
'ten-hove-incomplete-2025':'Publisher fulltext abstract, estimator-comparison discussion and real-data example inspected through web tool. Local PDF request blocked; no claim of local possession.',
'huebner-lucht-r-2019':'Local fulltext: design/ANOVA/D-study formula tables, illustrative calculations and reproducible data discussion read. Code not executed.',
'huebner-mixed-2025':'Local PDF title, abstract/summary and fixed/multivariate discussion inspected; full derivations not audited.',
'brennan-complex-2022':'Primary fulltext abstract, universe/error covariance definitions, confounding discussion and estimation caveats inspected; local HTML preserved.',
'jiang-ci-2022':'Primary publisher abstract and appendix tables inspected; local complete PMC HTML acquired. Method implementation not audited.',
'rockwood-jeon-2022':'Primary fulltext GT section and Brennan.3.2 illustration inspected; local PDF acquired.',
'lin-sparse-2017':'Local PDF abstract plus primary fulltext rating/subdividing method description inspected; implementation not audited.',
'huynh-incomplete-1977':'Original ERIC PDF title and OCR abstract inspected; primary ERIC abstract checked. Mathematical body not yet audited.',
'swallow-monahan-1984':'Author university-hosted primary PDF abstract and one-way model/estimator setup inspected; local PDF acquired.',
'choi-dissertation-2013':'University primary fulltext indexed passages on Huynh data, four estimators and response scales inspected through web search. Local PDF blocked.'
}
retry=json.loads((lane/'retries.json').read_text())
for r in records:
    slug=r['id'].removeprefix('estimation-')
    if slug in verified:
        r['title'],r['authors'],r['year']=verified[slug]
    if slug in read:r['evidence']=read[slug]
    else:r['evidence']='Primary publisher/university abstract or bibliographic metadata inspected; full mathematical text not yet read.'
    if slug=='jiang-ci-2022':r['doi']='10.1177/00131644211033899';r['source_url']='https://doi.org/'+r['doi']
    if slug=='swallow-monahan-1984':r['doi']='10.1080/00401706.1984.10487921';r['source_url']='https://doi.org/'+r['doi']
    if slug=='huynh-incomplete-1977':r['source_url']='https://eric.ed.gov/?id=ED154003'
    if slug=='choi-dissertation-2013':r['source_url']='https://escholarship.org/uc/item/7qv174cb'
    for rr in retry:
        if rr['id']==r['id'] and 'result' in rr:
            result=rr['result'];r['status']='acquired';r['local_path']='papers/downloads/estimation/'+slug+'.pdf';r['fulltext_url']=result['source_url'];r['acquisition_note']='Acquired alternate university/author-hosted copy; original bytes and provenance retained; private research copy.'
    if not r['title'] or not r['authors'] or not r['year']:raise ValueError('Unverified metadata '+r['id'])
for rr in retry:logs.append({'id':rr['id'],'attempts':[rr]})
logs.append({'scope':'web_searches','date':'2026-10-02','queries':['GT unbalanced Brennan urGENOVA Henderson REML','Bayesian GT variance components negative estimates','Henderson 1953 Rao MINQUE Patterson Thompson 1971','Marcoulides 1987 1990 variance estimation','Chiu Wolfe sparse 2002','GT mixed-model Jiang 2018','Bayesian multivariate GT Jiang Skorupski','GT planned incomplete ICC ten Hove 2025','Huynh incomplete KR20 ERIC','Sparse language Lin 2017','GT boundary negative variance Fyans','Harville ML REML primary PDF','Brennan 1994 variance components bibliography'],'bibliography_expansion':['Brennan 1994 publisher references','Marcoulides 1990 publisher references','Chiu Wolfe 2002 publisher references','Jiang 2022 publisher references','Local Brennan Liao 2020 first-sixty-years catalogue'],'note':'Initial acquisition worker interrupted after a hostname exceeded socket timeout; acquired artifacts retained; final acquisition pass uses subprocess wall timeouts.'})
(lane/'catalogue.json').write_text(json.dumps(records,indent=2)+'\n')
(lane/'search-log.json').write_text(json.dumps(logs,indent=2)+'\n')
print(json.dumps({'catalogued_works':len(records),'acquired_works':sum(r['status']=='acquired' for r in records),'blocked_works':sum(r['status']=='access_blocked' for r in records),'supplements':1}))
