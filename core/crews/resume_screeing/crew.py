from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from core.tools import basic_llm


@CrewBase
class ResumeScreeningCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def resume_screening_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["resume_screening_agent"],
            verbose=True,
            llm=basic_llm,
        )

    @task
    def resume_screening_task(self) -> Task:
        return Task(
            config=self.tasks_config["resume_screening_task"],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )