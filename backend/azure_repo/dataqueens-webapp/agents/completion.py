from agents.imports import AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT
from langchain_openai import AzureChatOpenAI


LLM_CHAT = AzureChatOpenAI(
    azure_deployment="gpt-4", 
    api_version="2024-02-01",
    temperature=0.4,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

def complete_old(prompt: str) -> dict:
    """Does what the user says!"""
    messages = [
        (
        "system",
        """As an insurance specialist for autonomous vehicles (AV), your task is to draft tailored insurance policies based on a user's profile and their specific AV model. Consider that the AV can operate independently without the user's direct control, which may lead to autonomous accidents. Your objective is to create the most advantageous insurance policy that maximizes revenue and minimizes risks for the insurance company, while also ensuring it is competitive and appealing enough to retain the customer over other providers.

            Please format your response in JSON, including distinct sections with titles and detailed content. 
            Please form 3 different insurance policies, one named "Total insurance", the second "Ecnomic insurance"
            while the third "Balanced insurance". 
            In each policy, there are different sections,
            each section should address different aspects of the policy, and the title is the name of the insurance.
            Please make the metadata and sections of each inusrance refelcts its title. Here is the structure to follow:

            {
            "title": "Customized AV Insurance Policy",
            "sections": [
                {
                "section_title": "Coverage and Clauses",
                "section_content": "Details the specific coverage items and clauses relevant to autonomous operation and user control scenarios."
                },
                {
                "section_title": "Liability and Responsibilities",
                "section_content": "Outlines the division of financial responsibility between the insurance holder and the company in cases of autonomous accidents."
                },
                {
                "section_title": "Pricing and Payment",
                "section_content": "Provides a breakdown of premium calculations, discounts, and payment schedules."
                }
            ],
            "metadata" : {
                "price" : 100, -- how much the user will pay per month
                "AI_safety_score" : 90 -- how safe the autodrive of their car is.
                "driver_behaviour" : -- description of the driver behaviour given the user's data.,
                "deductible" : -- how much the customer will pay out of pocket
                

            }
            }
        """,
        ),
        ("human", prompt),
    ]
    ai_msg = LLM_CHAT.invoke(messages)
    return ai_msg


def complete(prompt: str, json_formatting: bool = True) -> dict:
    """Does what the user says!"""

    true_json_format = """
     Please come up 3 different insurance policies, one named "Total insurance", the second "Economy insurance"
            and the third "Balanced insurance". 
            In each policy, there are different sections,
            each section should address different aspects of the policy, and the title is the name of the insurance.
    Please format your response in JSON, including distinct sections with titles and detailed content. Each section should address different aspects of the policy. The JSON below is supposedto be followed by each one of them, that is each should have metadata, title, sections, etc, in separate JSONs. Also, in each JSON you will have a field called "type", that should be "economy", "balanced" or "total_insurance".:

            {
            "title": "Customized AV Insurance Policy",
            "type" : "" -- "economy", "balanced" or "total_insurance"
            "sections": [
                {
                "section_title": "Coverage and Clauses",
                "section_content": "Details the specific coverage items and clauses relevant to autonomous operation and user control scenarios."
                },
                {
                "section_title": "Liability and Responsibilities",
                "section_content": "Outlines the division of financial responsibility between the insurance holder and the company in cases of autonomous accidents."
                },
                {
                "section_title": "Pricing and Payment",
                "section_content": "Provides a breakdown of premium calculations, discounts, and payment schedules."
                }
            ],
            "metadata" :         ```{
            "vehicle_maker": "Ford",
            "vehicle_model": "Expedition",
            "vehicle_year":  2009,
            "liability_coverage": {
                "bodily_injury_liability_per_person": 100,000,
                "bodily_injury_liability_per_accident": 300,000,
                "property_damage_liability_per_accident": 50,000,
            },
            "comprehensive_coverage": {
                "deductible": 1,000
            },
            collision_coverage": {
                "included": True,
                "deductible": 1,000
            },
            "personal_injury_protection": {
                "medical_expenses_limit":10,000,
                "lost_wages_limit":5,000,
            },
            "uninsured/underinsured_motorist_coverage": {
                "bodily_injury_per_person": 100,000,
                "bodily_injury_per_accident": 300,000,
                "property_damage_per_accident": 25,000,
                "deductible": 500
            },
            "av_specific_coverage": {
                "coverage_limit": 50,000,
                "deductible": 2,000
            },
            "premium_details": {
                "annual_premium": 1,200,
                "discounts": "10% discount for JD degree holders, 5% loyalty discount for renewal without autonomous operation-related claims",
                "payment_options": "Annually"},
            "AI_safety_score" : 90 -- how safe the autodrive of their car is.
            "driver_behaviour" : -- description of the driver behaviour given the user's data.,
                }
            }"""

    messages = [
        (
        "system",
        f"""As an insurance specialist for autonomous vehicles (AV), your task is to draft tailored insurance policies based on a user's profile and their specific AV model. Consider that the AV can operate independently without the user's direct control, which may lead to autonomous accidents. Your objective is to create the most advantageous insurance policy that maximizes revenue and minimizes risks for the insurance company, while also ensuring it is competitive and appealing enough to retain the customer over other providers.

        Here's a good example of a policy. Make sure to, in your asnwer, have every single field/title present in the example below: 
        ```
            **Insurance Policy Proposal for 1995 GMC Yukon (Autonomous Vehicle)**

            **Policyholder:** Male, 43 years old, Married, High School Education

            **Vehicle Details:**
            - Make: GMC
            - Model: Yukon
            - Year: 1995

            **Previous Accident History:**
            - Injuries: Yes (Details not specified)
            - Crash Speed: 60 mph
            - Conditions: Cloudy and Rainy Weather

            **Coverage Details:**

            1. **Liability Coverage:**
            - Bodily Injury Liability: $250,000 per person / $500,000 per accident
            - Property Damage Liability: $200,000 per accident

            2. **Comprehensive Coverage:**
            - Collision: Included
            - Non-collision (fire, theft, vandalism): Included
            - Deductible: $1,000

            3. **Personal Injury Protection (PIP):**
            - Medical expenses: Up to $100,000
            - Lost wages: Up to $50,000
            - Deductible: $500

            4. **Uninsured/Underinsured Motorist Coverage:**
            - Bodily Injury: $100,000 per person / $300,000 per accident
            - Property Damage: $100,000 per accident

            5. **AV-Specific Coverage:**
            - Autonomous Vehicle System Malfunction: Covers damages and liabilities caused by system failures or software malfunctions in the AV system.
            - Cybersecurity Breach: Coverage for damages due to hacking or unauthorized access to the vehicle’s autonomous systems.
            - Deductible: $1,500

            6. **Additional Options:**
            - Roadside Assistance: Included
            - Rental Reimbursement: Up to $50 per day for a maximum of 30 days

            **Premium Details:**
            - Monthly Premium: $350
            - Payment Options: Monthly, Quarterly, Semi-Annually, Annually (5% discount on annual payments)

            **Terms and Conditions:**
            - The policyholder is required to ensure that all software updates for the AV system are installed within 30 days of release.
            - The vehicle must undergo an annual inspection by a certified AV technician to ensure that the autonomous systems are functioning correctly.
            - Failure to comply with the above conditions may result in voidance of certain coverages.

            **Discounts Available:**
            - Safe Driver Discount: 10% off for no claims in the past three years.
            - Multi-Vehicle Discount: 5% off if insuring more than one vehicle.
            - Education Discount: 3% off for policyholders with a college degree or higher.

            This policy is designed to offer comprehensive protection for both conventional and autonomous driving risks, tailored specifically to the needs and history of the policyholder. It balances competitive pricing with robust coverage to ensure both customer satisfaction and minimized risk exposure for the insurance company.```
        {true_json_format if json_formatting else ""}

        Do not add anything else to the policy that is not pertinent to the contract. For example, sentences like "Thank you for providing the necessary details for the insurance policy. Based on the information provided, here is a tailored insurance policy for a 1995 GMC Yukon operated as an autonomous vehicle (AV) by a 43-year-old male with a high school education level, who is married and has a history of previous accidents involving injuries and crashes at 60 mph under cloudy and rainy conditions."  are not needed.
        """,
        ),
        ("human", prompt),
    ]
    ai_msg = LLM_CHAT.invoke(messages)
    return ai_msg


def prompt_optimization(prompt: str) -> dict:
    messages = [
        (
            "system",
            """You're a specialist in prompt engineering for LLMs. Optimize the user prompt
            for optimal results with LLMs.
            """,
        ),
        ("human", prompt),
    ]
    ai_msg = LLM_CHAT.invoke(messages)
    return ai_msg

if __name__ == '__main__':
    result = prompt_optimization("")