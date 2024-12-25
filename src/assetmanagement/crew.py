from assetmanagement.tools.custom_tool import stock_news, stock_price_1m, stock_price_1y, income_stmt, balance_sheet, insider_transactions, macro_economic_data, stock_info, cash_flow, option_chain
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool
from crewai.agents.parser import AgentAction, AgentFinish
import streamlit as st
from typing import Union, List, Tuple, Dict
import os
import assetmanagement.emoji as emoji

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

LLM.set_verbose=True
scrape_tool = ScrapeWebsiteTool()

#sLLM = LLM(model="ollama/gemma2:9b", base_url="http://localhost:11434")
#sLLM = LLM(model="ollama/llama3:latest", base_url="http://localhost:11434")
#sLLM = LLM(model="anthropic/claude-3-5-sonnet-20240620",api_key=os.environ["ANTHROPIC_API_KEY"])
sLLM = LLM(model="gpt-4o",api_key=os.environ["OPENAI_API_KEY"])

@CrewBase
class Assetmanagement():
	"""Assetmanagement crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
 
	def step_callback(
        self,
        agent_output: Union[str, List[Tuple[Dict, str]], AgentFinish],
        agent_name,
        *args,
    ):	
		with st.chat_message("AI"):
			emoji = self.getAgentEmoji(agent_name)
			if isinstance(agent_output, AgentAction):
				with st.expander(f"{agent_name} Tought"):
					st.write(f"{emoji} {agent_name}")
					if agent_output.tool:
						st.write(f"Tool Used: {agent_output.tool}")
						st.write(f"Tool input: {agent_output.tool_input}")
					if agent_output.text:
						st.write(f"Message: {agent_output.text}")
					if agent_output.result:
						st.write(f"Result: {agent_output.result}")
    
			elif isinstance(agent_output, AgentFinish):
				st.write(f"{emoji} {agent_name}")
				if agent_output.thought:
					st.write(agent_output.thought)
				if agent_output.output:
					st.write(agent_output.output)
			else:
				st.write(type(agent_output))
				st.write(agent_output)
     
	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			tools=[
				scrape_tool,
				stock_news
			],
			llm=sLLM,
			step_callback=lambda step: self.step_callback(step, "Researcher")
		)
  
	@agent
	def	macro_strategist(self) -> Agent:
		return Agent(
			config=self.agents_config['macro_strategist'],
			tools=[
				macro_economic_data,
			],
			llm=sLLM,
			step_callback=lambda step: self.step_callback(step, "Macro Strategist")
		)

	@agent
	def technical_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['technical_analyst'],
			tools=[
				stock_price_1m,
				stock_price_1y,
			],
			llm=sLLM,
   			step_callback=lambda step: self.step_callback(step, "Technical Analyst")
		)

	@agent
	def financial_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['financial_analyst'],
			tools=[
				income_stmt,
				balance_sheet,
				insider_transactions,
				cash_flow,
				option_chain,
				stock_info
			],
			llm=sLLM,
			step_callback=lambda step: self.step_callback(step, "Financial Analyst")
		)
	
	@agent
	def hedge_fund_manager(self) -> Agent:
		return Agent(
			config=self.agents_config['hedge_fund_manager'],
			verbose=True,
			llm=sLLM,
			step_callback=lambda step: self.step_callback(step, "Hedge Fund Manager")
		)
	@agent
	def translator(self) -> Agent:
		return Agent(
			config=self.agents_config['translator'],
			llm=sLLM,
			step_callback=lambda step: self.step_callback(step, "Translator")
		)
  
	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
 
	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
		)
  
	@task
	def macro_strategist_task(self) -> Task:
		return Task(
			config=self.tasks_config['macro_strategist_task'],
			output_file='reports/macro_report.md',
		)

	@task
	def technical_analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['technical_analysis_task'],
			output_file='reports/technical_report.md',
		)

	@task
	def financial_analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['financial_analysis_task'],
			output_file='reports/financial_report.md',
		)

	@task
	def investment_recommendation_task(self) -> Task:
		return Task(
			config=self.tasks_config['investment_recommendation_task'],
			output_file='reports/investment_recommendation.md',
		)
	
	@task
	def translate_task(self) -> Task:
		return Task(
			config=self.tasks_config['translate_task'],
			output_file='reports/investment_recommendation_kr.md',
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Assetmanagement crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
  
	def	getAgentEmoji(self, agent_name):
		emojis = {
			"Researcher": emoji.SANTA,
			"Macro Strategist": emoji.ELSA,
			"Technical Analyst": emoji.RUDOLF,
			"Financial Analyst": emoji.SNOWMAN,
			"Hedge Fund Manager": emoji.KEVIN,
			"Translator": emoji.PENGSU
		}
		return emojis.get(agent_name, "🤖")
