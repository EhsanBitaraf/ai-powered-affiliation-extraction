# AI-Powered Affiliation Insights: LLM-Based Bibliometric Study of European Medical Informatics Conferences

This repository contains detailed bibliometric analyses of MIE Conferences to be published at MIE 2025.


---

In this repository, we have used the [conference MIE dataset](https://doi.org/10.6084/m9.figshare.27174759) and transformed the affiliation information into a structured form through a pipeline designed with langflow (Fig. 1) using the gpt-3.5-turbo-0125 model. We used a [prompt](/docs/prompt1.md) for this purpose and received the outputs in json form. Then we analyzed it

*Fig 1. The pipeline of langflow*

![Fig 1. The pipeline of langflow](/docs/langflow-pipeline.png)


# Result

![](/output/vos_viewer_countries_co_occurrence.png)