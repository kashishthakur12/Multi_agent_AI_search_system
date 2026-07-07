# Multi_agent_AI_search_system
Multi-agent AI research system with search, reader, writer, and critic agents, built with LangChain/LangGraph and a Streamlit UI.
A multi-agent AI research pipeline that automates the process of researching a topic end-to-end. 
A search agent finds recent, relevant sources; a reader agent scrapes the most useful page for 
deeper content; a writer chain drafts a structured report from the combined research; and a 
critic chain reviews the report and provides feedback. Includes a Streamlit UI for running the 
pipeline interactively and viewing results at each stage.

Multi_agent_AI_search_system/
│
├── agents.py           # Defines the search agent, reader agent, writer chain, and critic chain
├── pipeline.py          # Orchestrates the multi-agent pipeline (search → read → write → critique)
├── tools.py              # Custom tools used by the agents (e.g. web search, scraping)
├── app.py                 # Streamlit UI for running the pipeline interactively
├── requirement.txt   # Python dependencies
├── .env                       # API keys / environment variables (not committed — see .gitignore)
├── .gitignore              # Files/folders excluded from version control
└── README.md         # Project documentation
