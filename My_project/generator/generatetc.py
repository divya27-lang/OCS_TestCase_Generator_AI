from langchain_openai import ChatOpenAI
from openpyxl import Workbook


def create_generator(retriever):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    def qa_chain(query: str):
        docs = retriever.get_relevant_documents(query)

        context = "\n\n".join(d.page_content for d in docs)
        print(context)
        prompt = f"""
Using the context below, generate OCS test cases based on the requirements.

Return output STRICTLY as TAB-SEPARATED values.
Do not add explanations.

Based on the query find the testcases in the 'context' and generate the testcases according to the query
Columns:
TC_ID	A_Party	B_Party	Call_Type	Duration_BytesUsed	Roaming_Location	Called_Country	B_Party_Type	Expected_Results	Expected_Data_Free_Units	OCS_Response	Tags	Documentation
for example:
Domestic-PLAN-001	4.47301E+11	+447786941146	mo-voice	30	UK	UK	Mobile	10	0	2001	Sanity
Domestic-PLAN-002	4.47301E+11	447786941146	mo-sms		UK	UK	Mobile	0	0	2001	Sanity
Domestic-PLAN-003	4.47301E+11	447786941146	mms		UK	UK	Mobile	95	0	2001	Sanity
Domestic-PLAN-004	4.47301E+11		data	50000	UK			0	50000	2001	Sanity


Context:
{context}

Question:
{query}

Based on the query find the testcases in the 'context' and generate the testcases according to the query
"""

        response = llm.invoke(prompt)
        text = response.content.strip()

        # ---------- Save to Excel ----------
        wb = Workbook()
        ws = wb.active
        ws.title = "TestCases"

        rows = text.split("\n")
        for row in rows:
            ws.append(row.split("\t"))

        wb.save("testcases.xlsx")

        return text

    return qa_chain
