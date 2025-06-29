from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from market_researcher.tools.custom_tool import (
    PDFTextExtractorTool, SerperSearchTool, MoneycontrolWebTool, HinduNewsTool
)
from market_researcher.llm_azure import AzureOpenAILLM
from pathlib import Path
import yaml

# --- BSE Market Researcher Crew ---
@CrewBase
class BSEMarketResearcher():
    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        super().__init__()
        self.llm = AzureOpenAILLM()
        self.bse_tool = MoneycontrolWebTool()
        self.serper_tool = SerperSearchTool()
        # Load only BSE tasks config
        tasks_path = Path(__file__).parent / "config" / "tasks.yaml"
        with open(tasks_path, "r", encoding="utf-8") as f:
            self.tasks_config = yaml.safe_load(f)
        # Load only BSE agents config
        agents_path = Path(__file__).parent / "config" / "agents.yaml"
        with open(agents_path, "r", encoding="utf-8") as f:
            self.agents_config = yaml.safe_load(f)

    @agent
    def bse_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['bse_researcher'],
            llm=self.llm,
            tools=[self.bse_tool, self.serper_tool],
            verbose=True
        )

    @agent
    def trend_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['trend_analyst'],
            llm=self.llm,
            tools=[self.bse_tool],
            verbose=True
        )

    @agent
    def recommendation_engine(self) -> Agent:
        return Agent(
            config=self.agents_config['recommendation_engine'],
            llm=self.llm,
            verbose=True
        )

    @task
    def fetch_bse_data(self) -> Task:
        return Task(config=self.tasks_config['fetch_bse_data'])

    @task
    def analyze_trends(self) -> Task:
        return Task(config=self.tasks_config['analyze_trends'])

    @task
    def generate_recommendations(self) -> Task:
        return Task(config=self.tasks_config['generate_recommendations'])

    @task
    def report_task(self) -> Task:
        return Task(config=self.tasks_config['report_task'], output_file='bse_report.md')

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

# --- Hindu UPSC Notes Crew ---
@CrewBase
class HinduUPSCNotesCrew():
    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        super().__init__()
        self.llm = AzureOpenAILLM()
        self.hindu_tool = HinduNewsTool()
        # Load only Hindu UPSC tasks config
        tasks_path = Path(__file__).parent / "config" / "tasks.yaml"
        with open(tasks_path, "r", encoding="utf-8") as f:
            self.tasks_config = yaml.safe_load(f)
        # Load only Hindu UPSC agents config
        agents_path = Path(__file__).parent / "config" / "agents.yaml"
        with open(agents_path, "r", encoding="utf-8") as f:
            self.agents_config = yaml.safe_load(f)

    @agent
    def hindu_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['hindu_researcher'],
            llm=self.llm,
            tools=[self.hindu_tool],
            verbose=True
        )

    @agent
    def upsc_notes_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['upsc_notes_writer'],
            llm=self.llm,
            verbose=True
        )

    @task
    def fetch_hindu_news(self) -> Task:
        return Task(config=self.tasks_config['fetch_hindu_news'])

    @task
    def generate_upsc_notes(self) -> Task:
        return Task(config=self.tasks_config['generate_upsc_notes'], output_file='upsc_notes.md')

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

# --- MCQ Generation Crew ---
@CrewBase
class MCQGenerationCrew():
    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        super().__init__()
        self.llm = AzureOpenAILLM()
        self.pdf_tool = PDFTextExtractorTool()  # Placeholder, will be set in the task
        # Load only MCQ tasks config
        tasks_path = Path(__file__).parent / "config" / "tasks.yaml"
        with open(tasks_path, "r", encoding="utf-8") as f:
            self.tasks_config = yaml.safe_load(f)
        # Load only MCQ agents config
        agents_path = Path(__file__).parent / "config" / "agents.yaml"
        with open(agents_path, "r", encoding="utf-8") as f:
            self.agents_config = yaml.safe_load(f)

    @agent
    def mcq_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['mcq_generator'],
            llm=self.llm,
            tools=[self.pdf_tool],
            verbose=True
        )

    @task
    def extract_pdf_text(self) -> Task:
        return Task(config=self.tasks_config['extract_pdf_text'])

    @task
    def generate_mcqs(self) -> Task:
        return Task(config=self.tasks_config['generate_mcqs'], output_file='mcqs.md')

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )