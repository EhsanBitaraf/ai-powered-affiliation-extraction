from collections import defaultdict
import json
import os
import random
from src.config import CLI_ALERT_POINT, DATA_FILE, OUTPUT_DIR
from src.dataset import load_dataset_mie
import pandas as pd  
import networkx as nx

# from tqdm.notebook import tqdm
from tqdm import tqdm

class CoOccurrenceCalculator:
    proccess_bar = True
    data = load_dataset_mie()
    # top_cited_articles =[]
    keyword_co_occurrence_matrix = defaultdict(int)
    topics_co_occurrence_matrix = defaultdict(int)
    countries_co_occurrence_matrix = defaultdict(int)
    authors_co_occurrence_matrix = defaultdict(int)
    universities_co_occurrence_matrix = defaultdict(int)

#region Basic Table
    
    _country_normalize_data = [
        ("United Kingdom" , "UK"),
        ("The Netherlands","Netherlands"),
        ("United States","USA"),
        ("United States of America","USA"),
        ("People's Republic of China","China"),
        ("","Empty")
    ]

    _topic_normalize_data = [
        ("test","test1")
    ]

    _topic_blacklist = [
        "=",
        "+"
    ]


    _keyword_normalize_data = [
        ("test","test1")
    ]

    _keyword_blacklist = [
        "Humans",
        "Male",
        "Female",
        "Adult",
        "Aged",
        "Middle Aged",
        "Animals",
        # Study Type
        "Self Report",
        "Cross-Sectional Studies",
        "Case-Control Studies",
        "Cohort Studies",
        "Cohort Study",
        "Retrospective Studies",
        "Prospective Studies",
        "Prospective Cohort"
    ]


    _author_blacklist = [
        "Ali",
    ]
#endregion


    def _thefourtheye(self,data):
        """
        It takes a list of dictionaries, converts each dictionary to a frozenset of tuples, and then uses
        the frozenset as a key in a dictionary, with the value being the original dictionary
        Base on [this](https://stackoverflow.com/questions/9427163/remove-duplicate-dict-in-list-in-python)

        :param data: The list of dictionaries that you want to remove duplicates from
        :return: A dictionary with the keys being the frozenset of the items in the list and the values
        being the items in the list.
        """
        return {frozenset(item.items()): item for item in data}.values()

#region Calculate Co-occurrence Matrix
    def _co_occurring_authors(self, authors):
        for i in range(len(authors)):
            for j in range(i+1, len(authors)):
                self.authors_co_occurrence_matrix[(authors[i], authors[j])] += 1

    def _co_occurring_countries(self, countries):
        for i in range(len(countries)):
            for j in range(i+1, len(countries)):
                self.countries_co_occurrence_matrix[(countries[i], countries[j])] += 1

    def _co_occurring_universities_from_structural(self, structural_affiliations):
        uni_field = "university"
        universities = []
        for c in structural_affiliations:
            if c[uni_field] is not None:
                if c[uni_field] != "":
                    if c[uni_field] != "No Uni" or c[uni_field] != "University":
                        universities.append(c[uni_field])
        for i in range(len(universities)):
            for j in range(i+1, len(universities)):
                if isinstance(universities[i],str) and isinstance(universities[j],str):
                    # because of this:
                    # {'country': 'FR', 'institute': ['INSERM', 'Sorbonne Universités', 'Université Paris 13'], 'department': ['U1142', 'UMR_S 1142'], 'university': ['UPMC Univ Paris 06', 'Sorbonne Paris Cité'], 'city': ['Paris', 'Villetaneuse'], 'postalcode': None, 'email': None, 'Status': 'Ok'}
                    self.universities_co_occurrence_matrix[(universities[i], universities[j])] += 1

    def _co_occurring_countries_from_structural(self, structural_affiliations):
        countries = []
        for c in structural_affiliations:
            countries.append(c['country'])
        for i in range(len(countries)):
            for j in range(i+1, len(countries)):
                self.countries_co_occurrence_matrix[(countries[i], countries[j])] += 1

    def _co_occurring_keywords(self, keywords):
        for i in range(len(keywords)):
            for j in range(i+1, len(keywords)):
                self.keyword_co_occurrence_matrix[(keywords[i], keywords[j])] += 1

    def _co_occurring_topics(self, topics):
        """
        The function `_co_occurring_topics` calculates the co-occurrence matrix of topics in a list.
        
        :param topics: It looks like the code snippet you provided is a method that calculates the
        co-occurring topics based on a list of topics. The method iterates through the list of topics and
        updates a topics_co_occurrence_matrix with the count of co-occurrences between each pair of topics
        """
        for i in range(len(topics)):
            for j in range(i+1, len(topics)):
                self.topics_co_occurrence_matrix[(topics[i], topics[j])] += 1
#endregion

#region convert to df        
                    
    def _co_occurence_keywords_to_df(self):
        df = pd.DataFrame.from_records([list(pair) + [count] for pair, count in self.keyword_co_occurrence_matrix.items()]).rename({0:'Keyword1', 1:'Keyword2',2:'Count'}, axis=1).set_index(['Keyword1','Keyword2'])
        df['Count'] = df['Count'].astype(int)
        return df

    def _co_occurence_topics_to_df(self):
        df = pd.DataFrame.from_records([list(pair) + [count] for pair, count in self.topics_co_occurrence_matrix.items()]).rename({0:'Topics1', 1:'Topics2',2:'Count'}, axis=1).set_index(['Topics1','Topics2'])
        df['Count'] = df['Count'].astype(int)
        return df

    def _co_occurence_countries_to_df(self):
        df = pd.DataFrame.from_records([list(pair) + [count] for pair, count in self.countries_co_occurrence_matrix.items()]).rename({0:'Country1', 1:'Country2',2:'Count'}, axis=1).set_index(['Country1','Country2'])
        df['Count'] = df['Count'].astype(int)
        return df
    
#endregion


#region cleanzing functions
      
    def _normalize_country(self, country_text:str):
        if country_text is None:
            return "None"
        if country_text == "":
            return "None"
        country = str.lower(country_text)
        for a,b in self._country_normalize_data:
            if str.lower(country) == str.lower(a):
                return b

        return country_text

    def _normalize_topic(self, topic_text:str):
        if topic_text == "":
            return ""
        topic = str.lower(topic_text)
        for a,b in self._topic_normalize_data:
            if topic == str.lower(a):
                return b

        return topic_text

    def _topic_in_blacklist(self, topic_text:str):
        if topic_text == "":
            return False
        topic = str.lower(topic_text)        
        for t in self._topic_blacklist:
            if str.lower(t) == topic:
                return True
        return False

    def _normalize_keyword(self, keyword_text:str):
        if keyword_text == "":
            return ""
        keyword = str.lower(keyword_text)
        for a,b in self._keyword_normalize_data:
            if keyword == str.lower(a):
                return str.lower(b)

        return str.lower(keyword_text)

    def _keyword_in_blacklist(self, keyword_text:str):
        if keyword_text == "":
            return False
        keyword = str.lower(keyword_text)
        for t in self._keyword_blacklist:
            if str.lower(t) == keyword:
                return True
        return False        

    def _author_in_blacklist(self, author_text:str):
        if author_text == "":
            return False
        author = str.lower(author_text)
        for t in self._author_blacklist:
            if str.lower(t) == author:
                return True
        return False   

    def _normalize_topics(self,topics):
        new_topics = []
        topics = list(dict.fromkeys(topics))
        for t in topics:
            t = str.lower(t)
            ts = str.split(t," ")
            for topic in ts: # Delete like '='
                if len(topic) < 2:
                    pass
                else:
                    new_topics.append(topic)
        return new_topics

 #endregion  


#region export VOSviewer
        
    def export_vos_viewer_countries_co_occurring(self,
                                                 link_weight_limit = 0,
                                                 degree_limit= 0 ):
        G = nx.Graph()
        # Add nodes and edges based on co-occurrence matrix
        for pair, count in self.countries_co_occurrence_matrix.items():
            keyword1, keyword2 = pair
            keyword1 = self._normalize_country(keyword1)
            keyword2 = self._normalize_country(keyword2)
            if link_weight_limit == 0: # unlimited
                G.add_edge(keyword1, keyword2, weight=count)
            else:
                if  count > link_weight_limit:  
                    G.add_edge(keyword1, keyword2, weight=count)

        # Remove nodes with degree less than 10
        nodes_to_remove = [node for node, degree in dict(G.degree()).items() if degree < degree_limit]
        G.remove_nodes_from(nodes_to_remove)

        print(f"countries_co_occurring graph have {G.number_of_nodes()} nodes.")
        graph_data = {
        "network": {
            "items": [{"id": node,
                        "label": node,
                        "x": round(random.uniform(-1.1515,0.200),4),
                        "y": round(random.uniform(-1.1515,0.200),4)} for node, node_name in G.nodes(data="label")],
            "links": [{"source_id": source, "target_id": target, "strength": data["weight"]} for source, target, data in G.edges(data=True)]
        }
    }

        # Convert the dictionary to JSON format and save it to a file
        with open(os.path.join(OUTPUT_DIR ,"vos_viewer_countries_co_occurrence.json"), 'w') as outfile:
            json.dump(graph_data, outfile, indent=4)


    def export_vos_viewer_universities_co_occurring(self,
                                                 link_weight_limit = 0,
                                                 degree_limit= 0 ):
        G = nx.Graph()
        # Add nodes and edges based on co-occurrence matrix
        for pair, count in self.universities_co_occurrence_matrix.items():
            keyword1, keyword2 = pair
            # keyword1 = self._normalize_country(keyword1)
            # keyword2 = self._normalize_country(keyword2)
            if link_weight_limit == 0: # unlimited
                G.add_edge(keyword1, keyword2, weight=count)
            else:
                if  count > link_weight_limit:  
                    G.add_edge(keyword1, keyword2, weight=count)

        # Remove nodes with degree less than degree_limit
        nodes_to_remove = [node for node, degree in dict(G.degree()).items() if degree < degree_limit]
        G.remove_nodes_from(nodes_to_remove)

        print(f"universities_co_occurring graph have {G.number_of_nodes()} nodes.")
        graph_data = {
        "network": {
            "items": [{"id": node,
                        "label": node,
                        "x": round(random.uniform(-1.1515,0.200),4),
                        "y": round(random.uniform(-1.1515,0.200),4)} for node, node_name in G.nodes(data="label")],
            "links": [{"source_id": source, "target_id": target, "strength": data["weight"]} for source, target, data in G.edges(data=True)]
        }
    }

        # Convert the dictionary to JSON format and save it to a file
        with open(os.path.join(OUTPUT_DIR ,"vos_viewer_universities_co_occurrence.json"), 'w') as outfile:
            json.dump(graph_data, outfile, indent=4)


    def export_vos_viewer_topics_co_occurring(self,
                                                 link_weight_limit = 0,
                                                 degree_limit= 0 ):
        G = nx.Graph()
        # Add nodes and edges based on co-occurrence matrix
        for pair, count in self.topics_co_occurrence_matrix.items():
            keyword1, keyword2 = pair
            if self._topic_in_blacklist(keyword1) or self._topic_in_blacklist(keyword2):
                pass
            else:
                keyword1 = self._normalize_topic(keyword1)
                keyword2 = self._normalize_topic(keyword2)
                if link_weight_limit == 0: # unlimited
                    G.add_edge(keyword1, keyword2, weight=count)
                else:
                    if  count > link_weight_limit:  
                        G.add_edge(keyword1, keyword2, weight=count)

        
        # Remove nodes with degree less than 10
        nodes_to_remove = [node for node, degree in dict(G.degree()).items() if degree < degree_limit]
        G.remove_nodes_from(nodes_to_remove)

        print(f"topics_co_occurring graph have {G.number_of_nodes()} nodes.")
        graph_data = {
        "network": {
            "items": [{"id": node,
                        "label": node,
                        "x": round(random.uniform(-1.1515,0.200),4),
                        "y": round(random.uniform(-1.1515,0.200),4)} for node, node_name in G.nodes(data="label")],
            "links": [{"source_id": source, "target_id": target, "strength": data["weight"]} for source, target, data in G.edges(data=True)]
        }
    }

        # Convert the dictionary to JSON format and save it to a file
        with open(os.path.join(OUTPUT_DIR ,"vos_viewer_topics_co_occurrence.json"), 'w') as outfile:
            json.dump(graph_data, outfile, indent=4)


    def export_vos_viewer_keywords_co_occurring(self,
                                                 link_weight_limit = 0,
                                                 degree_limit= 0 ):
        G = nx.Graph()
        # Add nodes and edges based on co-occurrence matrix
        for pair, count in self.keyword_co_occurrence_matrix.items():
            keyword1, keyword2 = pair
            if self._keyword_in_blacklist(keyword1) or self._keyword_in_blacklist(keyword2):
                pass
            else:
                keyword1 = self._normalize_keyword(keyword1)
                keyword2 = self._normalize_keyword(keyword2)
                if link_weight_limit == 0: # unlimited
                    G.add_edge(keyword1, keyword2, weight=count)
                else:
                    if  count > link_weight_limit:  
                        G.add_edge(keyword1, keyword2, weight=count)


        # Remove nodes with degree less than 10
        nodes_to_remove = [node for node, degree in dict(G.degree()).items() if degree < degree_limit]
        G.remove_nodes_from(nodes_to_remove)

        nx.write_gml(G, os.path.join(OUTPUT_DIR ,"networkx_keywords_co_occurrence.gml"))
        print(f"keywords_co_occurring graph have {G.number_of_nodes()} nodes.")
        graph_data = {
        "network": {
            "items": [{"id": node,
                        "label": node,
                        "x": round(random.uniform(-1.1515,0.200),4),
                        "y": round(random.uniform(-1.1515,0.200),4)} for node, node_name in G.nodes(data="label")],
            "links": [{"source_id": source, "target_id": target, "strength": data["weight"]} for source, target, data in G.edges(data=True)]
        }
    }

        # Convert the dictionary to JSON format and save it to a file
        with open(os.path.join(OUTPUT_DIR ,"vos_viewer_keyword_co_occurrence.json"), 'w') as outfile:
            json.dump(graph_data, outfile, indent=4)


    def export_vos_viewer_authors_co_occurring(self,
                                                 link_weight_limit = 0,
                                                 degree_limit= 0 ):
        G = nx.Graph()
        # Add nodes and edges based on co-occurrence matrix
        for pair, count in self.authors_co_occurrence_matrix.items():
            keyword1, keyword2 = pair
            if self._author_in_blacklist(keyword1) or self._author_in_blacklist(keyword2):
                pass
            else:
                # keyword1 = self._normalize_topic(keyword1)
                # keyword2 = self._normalize_topic(keyword2)
                if link_weight_limit == 0: # unlimited
                    G.add_edge(keyword1, keyword2, weight=count)
                else:
                    if  count > link_weight_limit:  
                        G.add_edge(keyword1, keyword2, weight=count)

        
        # Remove nodes with degree less than 10
        nodes_to_remove = [node for node, degree in dict(G.degree()).items() if degree < degree_limit]
        G.remove_nodes_from(nodes_to_remove)


        nx.write_gml(G, os.path.join(OUTPUT_DIR ,"networkx_authors_co_occurrence.gml"))
        print(f"authors_co_occurring graph have {G.number_of_nodes()} nodes.")
        graph_data = {
        "network": {
            "items": [{"id": node,
                        "label": node,
                        "x": round(random.uniform(-1.1515,0.200),4),
                        "y": round(random.uniform(-1.1515,0.200),4)} for node, node_name in G.nodes(data="label")],
            "links": [{"source_id": source, "target_id": target, "strength": data["weight"]} for source, target, data in G.edges(data=True)]
        }
    }

        # Convert the dictionary to JSON format and save it to a file
        with open(os.path.join(OUTPUT_DIR ,"vos_viewer_authors_co_occurrence.json"), 'w') as outfile:
            json.dump(graph_data, outfile, indent=4)


#endregion

    def calculate_all(self):
        limit = 0
        if limit !=0:
            print(f"Run calculate_all with limit {limit}.")
            pbar = tqdm(total=limit)
        else:
            print("Run calculate_all unlimited.")
            pbar = tqdm(total=len(self.data))
        n = 0 
        
        for a in self.data:
            if limit !=0:
                if n > limit:
                    break

            n = n + 1
            pbar.update(1)

            # analyze the co-occurring keywords
            self._co_occurring_keywords(a['keywords'])    

            # analyze the co-occurring topics
            a['new_topics'] = self._normalize_topics(a['topics'])
            self._co_occurring_topics(a['new_topics'])

            # # analyze the co-occurring countries for old field
            # countries = a['affiliation_countries']
            # self._co_occurring_countries(countries)


            # analyze the co-occurring countries
            structural_affiliations = a['structural_affiliations']
            self._co_occurring_countries_from_structural(structural_affiliations)


            # analyze the co-occurring universities
            structural_affiliations = a['structural_affiliations']
            self._co_occurring_universities_from_structural(structural_affiliations)

            

            # analyze the co-occurring author
            names = a['authors']
            self._co_occurring_authors(names)

    def plot_all_in_output(self):
        self.export_vos_viewer_keywords_co_occurring(degree_limit= 10,link_weight_limit=3)

        self.export_vos_viewer_topics_co_occurring(degree_limit= 10,link_weight_limit=3)

        self.export_vos_viewer_countries_co_occurring()

        # # co-authorship map
        self.export_vos_viewer_authors_co_occurring(degree_limit= 5,link_weight_limit=1)

        self.export_vos_viewer_universities_co_occurring(degree_limit= 2,link_weight_limit=1)