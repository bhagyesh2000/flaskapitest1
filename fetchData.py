import pandas as pd
from neo4j import GraphDatabase
import matplotlib.pyplot as plt
from neo4j import GraphDatabase
import pandas as pd
from py2neo import Graph
from IPython.core.display import display, HTML, Javascript
import neo4jupyter

def possibleproblem():
    d = {'Problem': ["Liver Cirrhosis", "Acute Hepatitis", "Constusions"], 'Odds_Ratio': [15.3, 18.6, 20.3],}
    books = pd.DataFrame(data=d)
    

    return books

def possibleproblememexample():
    #d = {'Problems': [{"Problem" :"Liver Cirrhosis"}, { "Problem" :"Acute Hepatitis"},{ "Problem" :"Constusions"}]}
    #d = {'Problem': ["Liver Cirrhosis", "Acute Hepatitis", "Constusions"],}
    #books = pd.DataFrame(data=d)

    #import getpass
    #password = getpass.getpass("\nPlease enter the Neo4j database password to continue \n")
    password = 'FUjaBMKHBigyHtjaD9il71GV4GVGAsi7YBWtIBn-Cyo'    
    driver=GraphDatabase.driver(uri="neo4j+s://1d23f23f.databases.neo4j.io:7687", auth=('neo4j',password))
    session=driver.session()

    query = "MATCH (s:Problem) RETURN s.name AS Problem "

    with session:
        result = session.read_transaction( lambda tx: 
            tx.run(
            query,
            ).data()
        )
    df = pd.DataFrame(result)
    #display(df)
    return df

def diagnostics():
    d = {'s.name': ["Magnesium", "MCH"], 'Odds_Ratio': [3.2401, 2.5975],}
    books = pd.DataFrame(data=d)
    

    return books

def treatments():
    d = {'s.name': ["Thiamine", "Folic Acid"], 'r.Odds_Ratio': [9.71, 5.78],}
    books = pd.DataFrame(data=d)
    

    return books

def possibleproblemExplaination():
    d = {'s.name': ["Liver Cirrhosis", "Acute Hepatitis", "Constusions"], 'r.Odds_Ratio': [15.3, 18.6, 20.3],}
    books = pd.DataFrame(data=d)
    

    return books

def documentation():
    d = {'s.name': ["Liver Cirrhosis", "Acute Hepatitis", "Constusions"], 'r.Odds_Ratio': [15.3, 18.6, 20.3],}
    books = pd.DataFrame(data=d)
    

    return books

def possibleproblememexampleparameter(pproblem):
    password = 'FUjaBMKHBigyHtjaD9il71GV4GVGAsi7YBWtIBn-Cyo'    
    driver=GraphDatabase.driver(uri="neo4j+s://1d23f23f.databases.neo4j.io:7687", auth=('neo4j',password))
    #password = 'neo'    
    #driver=GraphDatabase.driver(uri="bolt://localhost:7687", auth=('neo4j',password))
    session=driver.session()

    query = "MATCH (n:Src_Prob)-[r:Possible_Problem]->(s) WHERE n.name IN $pprob RETURN s,r,n"
    #query = "MATCH (n:Src_Prob)-[r:Possible_Problem]->(s) WHERE n.name IN $pprob RETURN s.name as Problem, n.name as Source_Problem, r.Odds_Ratio as Odds_Ratio"
    with session:
        result = session.read_transaction( lambda tx: 
            tx.run(
            query, 
            pprob = pproblem
            ).data()
        )
    session.close()
    df = pd.DataFrame(result)
    #display(df)
    return df 


def diagnosticsexampleparameter(diagnose):
    password = 'FUjaBMKHBigyHtjaD9il71GV4GVGAsi7YBWtIBn-Cyo'    
    driver=GraphDatabase.driver(uri="neo4j+s://1d23f23f.databases.neo4j.io:7687", auth=('neo4j',password))
    #password = 'neo'    
    #driver=GraphDatabase.driver(uri="bolt://localhost:7687", auth=('neo4j',password))
    session=driver.session()

    #query = "MATCH (n:Src_Prob {name:'"+src+"'})-[r:Possible_Problem]->(s) RETURN s.name"
    query = "MATCH (n:Problem)-[r:Diagnosis]->(s) WHERE n.name IN $dia RETURN s.name as Diagnosis, n.name as Problem, r.Odds_Ratio as Odds_Ratio"
    with session:
        result = session.read_transaction( lambda tx: 
            tx.run(
            query, 
            dia = diagnose
            ).data()
        )
            
        df = pd.DataFrame(result)
        #display(df)
        return df 
   
    
def treatmentsexampleparameter(treatment):
    password = 'FUjaBMKHBigyHtjaD9il71GV4GVGAsi7YBWtIBn-Cyo'    
    driver=GraphDatabase.driver(uri="neo4j+s://1d23f23f.databases.neo4j.io:7687", auth=('neo4j',password))
    #password = 'neo'    
    #driver=GraphDatabase.driver(uri="bolt://localhost:7687", auth=('neo4j',password))
    session=driver.session()

    #query = "MATCH (n:Src_Prob {name:'"+src+"'})-[r:Possible_Problem]->(s) RETURN s.name"
    query = "MATCH (n:Problem)-[r:Treatment]->(s) WHERE n.name IN $treat RETURN s.name as Treatment, n.name as Problem, r.Odds_Ratio as Odds_Ratio"
    with session:
        result = session.read_transaction( lambda tx: 
            tx.run(
            query, 
            treat = treatment
            ).data()
        )
        df = pd.DataFrame(result)
        #display(df)
        return df 
    
    
def comorbidities_of_CUI(cui_prob_list): 
    
    driver=GraphDatabase.driver(uri="bolt://76.251.77.235:7687", auth=('neo4j', 'NikeshIsCool')) 
    session=driver.session() 
    
    query = ''' 
    MATCH (prob1:Problem)<-[:HAD_PROBLEM]-(pt:Patients) 
    WHERE prob1.cui in {cui_prob_list} 
    WITH distinct(pt) AS patients 
    MATCH (patients)-[:HAD_PROBLEM]->(prob2:Problem) 
    WITH prob2.cui AS CUIs, count(prob2) AS Number 
    MATCH (c:Concept) 
    WHERE c.cui IN CUIs AND c.cui_pref_term IS NOT NULL  
    RETURN c.term as Potential_Problem, c.cui AS CUI, Number 
    ORDER BY Number DESC 
    '''.format(cui_prob_list=cui_prob_list) 
    comorbidities = session.run(query) 
    comorbidities = pd.DataFrame([dict(record) for record in comorbidities]) 
    
    query = ''' 
    MATCH (excluded:Problem) 
    WHERE excluded.cui in {cui_prob_list} 
    WITH collect(excluded) as excluded 
    MATCH (pt:Patients)-[:HAD_PROBLEM]->(prob:Problem) 
    WITH excluded, pt, collect(prob) as problems 
    WHERE NONE (prob in problems where prob in excluded) 
    MATCH (pt)-[:HAD_PROBLEM]-(prob2:Problem) 
    WITH prob2.cui AS CUIs, count(prob2) AS Number 
    MATCH (c:Concept) 
    WHERE c.cui IN CUIs AND c.cui_pref_term IS NOT NULL  
    RETURN c.term as Potential_Problem, c.cui AS CUI, Number 
    ORDER BY Number DESC 
    '''.format(cui_prob_list=cui_prob_list) 
    gen_problems = session.run(query) 
    gen_problems = pd.DataFrame([dict(record) for record in gen_problems]) 
    gen_pop_total = sum(gen_problems['Number']) 
    gen_problems['Gen_pop_proportion'] = gen_problems['Number']/gen_pop_total 
    gen_problems = gen_problems[gen_problems['Number'] > 25] 
    comorb_total = sum(comorbidities['Number']) 
    comorbidities['Comorbidities_proportion'] = comorbidities['Number']/comorb_total 
    comorbidities = comorbidities[comorbidities['Number'] > 75/len(cui_prob_list)] 

    # Merge the "Gen_pop_proportion" column from gen_problems into comorbidities 
    comorbidities = pd.merge(comorbidities, gen_problems, on=['CUI', 'Potential_Problem']) 
    comorbidities.head() 
    comorbidities['Odds_Ratio'] = (comorbidities['Comorbidities_proportion']/comorbidities['Gen_pop_proportion']) 
    comorbidities.sort_values(by='Odds_Ratio', ascending=False, inplace=True) 
    return comorbidities.loc[:,['CUI','Potential_Problem', 'Odds_Ratio']].head(10) 



def getproblems(cui_prob_list):
    driver=GraphDatabase.driver(uri="bolt://76.251.77.235:7687", auth=('neo4j', 'NikeshIsCool')) 
    session=driver.session()

    query = " MATCH (n:Problem) RETURN DISTINCT n.cui as CUI,n.description as Problem LIMIT 15 "
    with session:
        result = session.read_transaction( lambda tx: 
            tx.run(
            query,
            cui_prob_list = cui_prob_list
            ).data()
        )
        df = pd.DataFrame(result)
        #display(df)
        return df



def PotentialComorbidities(cui_prob_list):
    driver=GraphDatabase.driver(uri="bolt://76.251.77.235:7687", auth=('neo4j', 'NikeshIsCool')) 
    session=driver.session()

    query = '''
    MATCH (prob1:Problem)<-[:HAD_PROBLEM]-(pt:Patients)
    WHERE prob1.cui in {cui_prob_list}
    WITH distinct(pt) AS patients
    MATCH (patients)-[:HAD_PROBLEM]->(prob2:Problem)
    WITH prob2.cui AS CUIs, count(prob2) AS Number
    MATCH (c:Concept)
    WHERE c.cui IN CUIs AND c.cui_pref_term IS NOT NULL 
    RETURN c.term as `PotentialProblem`, c.cui AS CUI, Number
    ORDER BY Number DESC
    '''.format(cui_prob_list=cui_prob_list)
    comorbidities = session.run(query)
    comorbidities = pd.DataFrame([dict(record) for record in comorbidities])
    
    query = '''
    MATCH (excluded:Problem)
    WHERE excluded.cui in {cui_prob_list}
    WITH collect(excluded) as excluded
    MATCH (pt:Patients)-[:HAD_PROBLEM]->(prob:Problem)
    WITH excluded, pt, collect(prob) as problems
    WHERE NONE (prob in problems where prob in excluded)
    MATCH (pt)-[:HAD_PROBLEM]-(prob2:Problem)
    WITH prob2.cui AS CUIs, count(prob2) AS Number
    MATCH (c:Concept)
    WHERE c.cui IN CUIs AND c.cui_pref_term IS NOT NULL 
    RETURN c.term as `PotentialProblem`, c.cui AS CUI, Number
    ORDER BY Number DESC
    '''.format(cui_prob_list=cui_prob_list)
    gen_problems = session.run(query)
    gen_problems = pd.DataFrame([dict(record) for record in gen_problems])
    
    gen_pop_total = sum(gen_problems['Number'])
    gen_problems['Gen_pop_proportion'] = gen_problems['Number']/gen_pop_total
    
    gen_problems = gen_problems[gen_problems['Number'] > 25]
    
    comorb_total = sum(comorbidities['Number'])
    comorbidities['Comorbidities_proportion'] = comorbidities['Number']/comorb_total
    
    comorbidities = comorbidities[comorbidities['Number'] > 75/len(cui_prob_list)]
    
    # Merge the "Gen_pop_proportion" column from gen_problems into comorbidities
    comorbidities = pd.merge(comorbidities, gen_problems, on=['CUI', 'PotentialProblem'])
    
    comorbidities.head()
    
    comorbidities['OddsRatio'] = (comorbidities['Comorbidities_proportion']/comorbidities['Gen_pop_proportion'])
    comorbidities.sort_values(by='OddsRatio', ascending=False, inplace=True)
    
    return comorbidities.loc[:,['CUI','PotentialProblem', 'OddsRatio']].head(10)

def LikelyAbnormalLabs(cui_prob_list):
    driver=GraphDatabase.driver(uri="bolt://76.251.77.235:7687", auth=('neo4j', 'NikeshIsCool')) 
    session=driver.session()

    query = '''
    MATCH (prob1:Problem)<-[:HAD_PROBLEM]-(pt:Patients)
    WHERE prob1.cui in {cui_prob_list}
    WITH distinct(pt) AS patients
    MATCH (d:D_Labitems)-[:DESCRIBES]->(n:Labevents)<-[:HAD]-(patients)
    RETURN d.itemid AS ITEMID, d.label as `AbnormalLab`, d.fluid as `Source`, COUNT(n.flag = 'abnormal') AS abnormal, COUNT(n) as total
    ORDER BY total DESC
    '''.format(cui_prob_list=cui_prob_list)
    with_prob_labs = session.run(query)
    with_prob_labs = pd.DataFrame([dict(record) for record in with_prob_labs])
    
    query = '''
    MATCH (excluded:Problem)
    WHERE excluded.cui in {cui_prob_list}
    WITH collect(excluded) as excluded
    MATCH (pt:Patients)-[:HAD_PROBLEM]->(prob:Problem)
    WITH excluded, pt, collect(prob) as problems
    WHERE NONE (prob in problems where prob in excluded)
    MATCH (d:D_Labitems)-[:DESCRIBES]->(n:Labevents)<-[:HAD]-(pt)
    RETURN d.itemid AS ITEMID, COUNT(n.flag = 'abnormal') AS abnormal, COUNT(n) as total
    ORDER BY total DESC
    '''.format(cui_prob_list=cui_prob_list)
    without_prob_labs = session.run(query)
    without_prob_labs = pd.DataFrame([dict(record) for record in without_prob_labs])
    
    without_prob_labs = without_prob_labs[without_prob_labs['abnormal'] > 10]
    without_prob_labs['without_prob_proportion_abnl'] = without_prob_labs['abnormal']/without_prob_labs['total']
    
    with_prob_labs = with_prob_labs[with_prob_labs['abnormal'] > 10]
    with_prob_labs['with_prob_proportion_abnl'] = with_prob_labs['abnormal']/with_prob_labs['total']
        
    # Merge the "Gen_pop_proportion" column from gen_problems into comorbidities
    with_prob_labs = pd.merge(with_prob_labs, without_prob_labs, on=['ITEMID'])
    
    with_prob_labs['OddsRatio'] = (with_prob_labs['with_prob_proportion_abnl']/with_prob_labs['without_prob_proportion_abnl'])
    with_prob_labs.sort_values(by='OddsRatio', ascending=False, inplace=True)
    
    return with_prob_labs.loc[:,['AbnormalLab', 'Source', 'OddsRatio']].head(10)

def LikelyPrescriptions(cui_prob_list):
    driver=GraphDatabase.driver(uri="bolt://76.251.77.235:7687", auth=('neo4j', 'NikeshIsCool')) 
    session=driver.session()

    query = '''
    MATCH (prob1:Problem)<-[:HAD_PROBLEM]-(pt:Patients)
    WHERE prob1.cui in {cui_prob_list}
    WITH distinct(pt) AS patients
    MATCH (patients)-[:HAD]->(rx:Prescriptions)
    RETURN rx.drug AS Drug, count(rx.drug) as Number
    ORDER BY Number DESC
    '''.format(cui_prob_list=cui_prob_list)
    with_prob_Rx = session.run(query)
    with_prob_Rx = pd.DataFrame([dict(record) for record in with_prob_Rx])
    
    query = '''
    MATCH (prob1:Problem)<-[:HAD_PROBLEM]-(pt:Patients)
    WHERE NOT prob1.cui in {cui_prob_list}
    WITH distinct(pt) AS patients
    MATCH (patients)-[:HAD]->(rx:Prescriptions)
    RETURN rx.drug AS Drug, count(rx.drug) as Number
    ORDER BY Number DESC
    '''.format(cui_prob_list=cui_prob_list)
    without_prob_Rx = session.run(query)
    without_prob_Rx = pd.DataFrame([dict(record) for record in without_prob_Rx])
       
    without_prob_total = sum(without_prob_Rx['Number'])
    without_prob_Rx['without_prob_proportion'] = without_prob_Rx['Number']/without_prob_total
    
    without_prob_Rx = without_prob_Rx[without_prob_Rx['Number'] > 30]
        
    with_prob_total = sum(with_prob_Rx['Number'])
    with_prob_Rx['with_prob_proportion'] = with_prob_Rx['Number']/with_prob_total
        
    with_prob_Rx = with_prob_Rx[with_prob_Rx['Number'] > 20]
    
    # Merge the "Gen_pop_proportion" column from gen_problems into comorbidities
    with_prob_Rx = pd.merge(with_prob_Rx, without_prob_Rx, on=['Drug'])
    
    with_prob_Rx['OddsRatio'] = (with_prob_Rx['with_prob_proportion']/with_prob_Rx['without_prob_proportion'])
    with_prob_Rx.sort_values(by='OddsRatio', ascending=False, inplace=True)
    
    return with_prob_Rx.loc[:,['Drug','OddsRatio']].head(10)

def nodedisplay():
    g=Graph('neo4j+s://1d23f23f.databases.neo4j.io:7687', auth=("neo4j", "FUjaBMKHBigyHtjaD9il71GV4GVGAsi7YBWtIBn-Cyo"))
    options = {"Src_Prob": "name", "Problem": "name", "Diagnosis": "name", "Treatment": "name"}


    query = """
        MATCH (n)-[r]->(m)
        RETURN n ,
            id(n),
            r,
            m ,
            id(m)
        """
    test = neo4jupyter.draw(g,options,query, physics=False)
    return test.data 