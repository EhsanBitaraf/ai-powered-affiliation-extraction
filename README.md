# AI-Powered Affiliation Insights: LLM-Based Bibliometric Study of European Medical Informatics Conferences

This repository contains detailed bibliometric analyses of MIE Conferences to be published at MIE 2025.

<cente>
<div style="text-align: center;">
  <img src="/docs/glasgow.png" alt="MIE 2025 Conference" width="400" height="266">
</div>
</cente>
# Table of contents

- [Result](#result)
  - [General Information](#general-information)
  - [Publication and citation trend](#publication-and-citation-trend)
  - [Authors](#authors)
  - [Countries](#countries)
  - [Institute](#institute)
  - [University](#university)
  - [Keywords](#keywords)
- [Data Availability](#data-availability)
- [Citation](#citing)
- [Contributors](#contributors)
- [License](#license)
---

In this repository, we have used the [conference MIE dataset](https://doi.org/10.6084/m9.figshare.27174759) and transformed the affiliation information into a structured form through a pipeline designed with langflow (Fig. 1) using the gpt-3.5-turbo-0125 model. We used a [prompt](/docs/prompt1.md) for this purpose and received the outputs in json form. Then we analyzed it

*Fig 1. The pipeline of langflow*

![Fig 1. The pipeline of langflow](/docs/langflow-pipeline.png)


# Results
All output is generated using the Python programming language and is available [here](/bibliometric-analysis.ipynb).

## General Information
This section provides a quantitative overview of the dataset analyzed, including the total number of publications, authors, citations, average citations per publication, and the diversity of contributing countries and institutions. It establishes the scope and scale of the research landscape covered by the bibliometric study

| Index | Value |
| --- | --- |
| Total Publications | 4606 |
| Total Authors | 11308 |
| Total Citations | 6191 |
| Average Citations | 1.34 |
| Total Countries | 95 |
| Total Universities | 352 |
| Total Unclean Universities | 1553 |


## Publication and citation trend
**The top 10 most cited works of literature**  
This part highlights the most influential articles by citation count, showcasing key contributions that have had significant impact within the field.

![](/output/top_most_cited_article.png)


**Annual and Cumulative Publication Trends**  
This visualization tracks how the number of publications has changed over time, both annually and cumulatively, revealing patterns of growth and periods of increased research activity.

![](/output/annual_and_cumulative_publication_trends.png)


**Articles with No Citations vs At Least One Citation by Year**  
This chart compares the number of uncited articles to those with at least one citation each year, offering insight into the visibility and influence of conference outputs over time.

![](/output/articles_with_no_citations_vs_at_least_one_citation_by_year.png)



**Trends in Citation Patterns and Future Predictions**  
This section analyzes how citations accumulate annually and cumulatively, and may include projections to anticipate future citation trends, helping to assess the evolving impact of the field.

![](/output/annual_and_cumulative_citation_trends.png)


## Authors
**Top Authors by Articles and Citations**  
This section lists the most cited authors, identifying key contributors and research leaders whose work has shaped the field’s development.

![](/output/authors_comparison_tables.png)


## Countries

This section examines the geographical distribution of research output and impact, showing which countries contribute most to publications and citations, and how their roles have evolved over time. It also visualizes collaboration patterns and research productivity through various charts and maps

![](/output/country_comparison_tables.png)

![](/output/top_10_countries_by_publication.png)

**Percentage of Annual Publications by Top 10 Countries**  
This visualization displays the share of annual publications from the leading countries, illustrating shifts in research leadership and international engagement.

![](/output/percentage_of_annual_publications_by_top_10_countries_stacked_column.png)

**Bubble chart to visualize the top 10 countries**  
These bubble charts provide a comparative, visual representation of the top publishing countries, making it easy to spot dominant players and emerging contributors.


![](/output/top_annual_publications_by_top_10_countries_bubble.png)
![](/output/top_10_countries_and_others_by_annual_publications_bubble.png)


**Citation per Article Index by Country**  
This section compares countries based on the average citations per article, highlighting differences in research impact and influence.

![](/output/top_25_countries_citation_per_article_index.png)


**Heatmap of Top 10 Country Co-occurrence**  
The heatmap illustrates collaboration intensity among the top countries, revealing international research networks and partnerships.

![](/output/top_10_country_co_occurrence_heatmap.png)


**Number of Articles geomap**  
This map visualizes the global distribution of published articles, offering a spatial perspective on research activity.

![](/output/articles_by_country_map.png)

**Countries Collabration**  
This network analysis file and visualization show how often countries collaborate, mapping the structure of international research cooperation

![VOSviewer](/output/vos_viewer_countries_co_occurrence.png)


## Institute

This section presents data on research output and citation impact at the institutional level, allowing comparison of the most productive and influential institutes in the field.

![institutions_comparison_tables](/output/institutions_comparison_table.png)

## University

Here, the focus narrows to universities, showing their publication and citation metrics, as well as their collaboration networks, often visualized using network analysis tools like VOSviewer.

![](/output/universities_comparison_tables.png)

![VOSviewer](/output/vos_viewer_universities_co_occurrence0.png)

## Keywords

This section analyzes the most frequently used keywords in publications, revealing major research topics, emerging trends, and thematic evolution over time. Network visualizations further illustrate how topics are interconnected within the field

![](/output/top_keywords_in_annual_publications.png)

![VOSviewer](/output/vos_viewer_keyword_co_occurrence.png)

# Data Availability
After modifying the [MIE Dataset](https://doi.org/10.6084/m9.figshare.27174759) and using LLM, a new structure called `structural_affiliations` was added to the previous dataset, which contains the following fields. The final dataset can be found [here](/data/dataset-mie.json).

structural_affiliations fields sample:
```json
  "structural_affiliations": [
      {
          "country": "",
          "institute": "",
          "department": "",
          "university": "",
          "city": "",
          "postalcode": "",
          "email": "",
          "Status": "",
          "universityf": ""
      }
  ]
```

![Repo Size](https://img.shields.io/github/repo-size/EhsanBitaraf/ai-powered-affiliation-extraction)

# Citation
If you use this article or the dataset in a scientific publication, we would appreciate references to the following [paper](https://doi.org/10.3233/shti250474):

Biblatex entry:

```latex
@article{bitaraf-2025,
	author = {Bitaraf, Ehsan and Jafarpour, Maryam},
	journal = {Studies in health technology and informatics},
	month = {5},
	title = {{AI-Powered Affiliation Insights: LLM-Based Bibliometric Study of European Medical Informatics Conferences}},
	year = {2025},
	doi = {10.3233/shti250474},
	url = {https://doi.org/10.3233/shti250474},
}
```

# Contributors

Please see our [contributing guidelines](CONTRIBUTING.md) for more details on how to get involved.

---

# License

This Repository is available under the [CC0-1.0 license](LICENSE).