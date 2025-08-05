import yaml, os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import CrewBase, agent, crew, task

load_dotenv()

@CrewBase
class EligibilityCrew:
    def __init__(self):
        self.agents_cfg = yaml.safe_load(open("config/agents.yaml"))
        self.tasks_cfg = yaml.safe_load(open("config/tasks.yaml"))

        # Initiaize LLM
        self.OPENAI_KEY = os.getenv("OPENAI_API_KEY")
        self.llm  = LLM(model="gpt-4", api_key=self.OPENAI_KEY)

    @agent
    def data_ingestor(self) -> Agent:
        return Agent(
            llm = self.llm,
            config=self.agents_cfg["data_ingestor"],
            verbose=True
        )

    @agent
    def evaluator(self) -> Agent:
        return Agent(
            llm = self.llm,
            config=self.agents_cfg["evaluator"],
            reasoning=True,
            verbose=True
        )

    @agent
    def recommender(self) -> Agent:
        return Agent(
            llm = self.llm,
            config=self.agents_cfg["recommender"],
            reasoning=True,
            verbose=True
        )

    @agent
    def enablement_advisor(self) -> Agent:
        return Agent(
            llm = self.llm,
            config=self.agents_cfg["enablement_advisor"],
            reasoning=True,
            verbose=True
        )

    @task
    def process_application(self) -> Task:
        return Task(config=self.tasks_cfg["process_application"])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.data_ingestor(),
                self.evaluator(),
                self.recommender(),
                self.enablement_advisor()
            ],
            tasks=[self.process_application()],
            process=Process.sequential,
            verbose=True
        )

