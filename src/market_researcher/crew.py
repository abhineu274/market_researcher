from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from market_researcher.tools.custom_tool import BSEWebTool, SerperSearchTool, MoneycontrolWebTool  # Example: your web tool for BSE
from market_researcher.llm_azure import AzureOpenAILLM

@CrewBase
class BSEMarketResearcher():
    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        super().__init__()
        self.llm = AzureOpenAILLM()
        self.bse_tool = MoneycontrolWebTool()
        self.serper_tool = SerperSearchTool()

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