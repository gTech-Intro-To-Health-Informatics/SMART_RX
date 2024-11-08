import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from crewai_tools import tool
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")



os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

chatbot_agent = Agent(
    role="Pharma Chatbot",
    goal="Answer patient's questions about prescribed medication using drug list, patient history, and query",
    verbose=True,
    memory=False,
    backstory="You assist patients by answering their queries about medications based on their history and current concerns.",
)

controller_agent = Agent(
    role="Conversation Controller",
    goal="Ensure the conversation stays on the topic of prescribed medications.",
    verbose=True,
    memory=False,
    backstory="You ensure that the patient stays focused on relevant medical topics."
)

@tool
def filter_tool(input: str) -> str:
    """Useful to filter the output from displaying to the user"""
    return " "

pcp_flagging_agent = Agent(
    role="PCP Flagging",
    goal="Monitor for issues in the conversation that require PCP attention.",
    verbose=True,
    memory=False,
    backstory="You flag the conversation if a patient's concern requires further review.",
    tools=[filter_tool],
    allow_delegation=False
)

drug_info_task = Task(
    description="Respond to patient queries: {patient_query} for additional context, this is the whole conversation: {conversation_history}, using the provided drug list: {drug_list} and patient history: {patient_history}.",
    expected_output="Clear answers regarding the medication prescribed by the PCP, based on the patient's query.",
    agent=chatbot_agent,
)

conversation_control_task = Task(
    description="Monitor the conversation to ensure it stays within the scope of the patient query: {patient_query}, provided drug list: {drug_list}, and patient history: {patient_history}.",
    expected_output="A well-controlled conversation that doesn't stray from the topic of prescribed drugs and the patient's query.",
    agent=controller_agent,
)

flagging_task = Task(
    description="Monitor for any issues or concerns related to the patient query: {patient_query}, drug list: {drug_list}, or patient history: {patient_history} that require a PCP's review and flag them.",
    expected_output="Flag the conversation for the PCP if necessary based on patient concerns.",
    agent=pcp_flagging_agent,
)


crew = Crew(
    manager_llm=ChatOpenAI(temperature=0, model="gpt-4"),
    agents=[chatbot_agent, controller_agent, pcp_flagging_agent],
    tasks=[drug_info_task, conversation_control_task, flagging_task],
    process=Process.sequential  # Sequentially run the tasks for each interaction
)

def pharma_chat(drug_list, patient_history, conversation_history, patient_query):
    conversation_history.append({'role': 'user', 'content': patient_query})

    inputs = {
        'drug_list': drug_list,
        'patient_history': patient_history,
        'patient_query': patient_query,
        'conversation_history': conversation_history
    }

    result = crew.kickoff(inputs=inputs)
    print(f"Pharma Chatbot: {result}")
    print("\n")
    conversation_history.append({'role': 'Pharma Chatbot', 'content': f"{result}" })
    return  conversation_history
ph = [{'role': 'user', 'content': 'Can I take Metformin and Adderall at the same time?'}, {'role': 'Pharma Chatbot', 'content': "It is advisable to flag this conversation for the PCP's review. While it is generally considered safe to take Metformin and Adderall together, your history of hypertension is a concern. Stimulants like Adderall can potentially increase blood pressure, which requires careful monitoring in patients with hypertension. Regular follow-up with your healthcare provider is crucial, as they can assess your overall health and make any necessary adjustments to your medication regimen. Please ensure you stay in contact with your PCP about any unusual symptoms or side effects you may experience while on these medications."}]

# print(pharma_chat(['Metformin', 'Adderall'], 'Patient has a history of hypertension and ADHD', ph, 'What if i get the flu while taking Metformin and Adderall?'))
