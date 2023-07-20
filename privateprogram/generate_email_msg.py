import pandas as pd
import datetime as dt

replace_words = ["[STRATEGY_NAME]", "[BEGIN_DATE]", "[END_DATE]", "[CUSTOMER_NAME]", "[SERVICE_FEE]", "[PERFORMANCE_FEE]", "[TOTAL]", "[EVIDENCE_DATE]" ]

f = open("email_message_template.txt", 'r', encoding="utf-8")
msg_template = f.read()

src_df = pd.read_excel("performance_report.xlsx")
src_df = src_df.reset_index()  
print(src_df)

for index, row in src_df.iterrows():
    msg = msg_template
    strategy = row["strategy"][:-3]
    msg = msg.replace("[CUSTOMER_EMAIL]", row["email"])
    msg = msg.replace("[STRATEGY_NAME]", strategy)
    msg = msg.replace("[BEGIN_DATE]", str(row["start date"].strftime("%d/%m/%Y")))
    msg = msg.replace("[END_DATE]", str(row["due day"].strftime("%d/%m/%Y")))
    msg = msg.replace("[CUSTOMER_NAME]", row["name"])
    msg = msg.replace("[SERVICE_FEE]", "{:,.2f}".format(round(row["Service Fee"],2)))
    msg = msg.replace("[PERFORMANCE_FEE]", "{:,.2f}".format(round(row["Perf Fee"],2)))
    msg = msg.replace("[TOTAL]", "{:,.2f}".format(round(row["Total"],2)))
    msg = msg.replace("[EVIDENCE_DATE]", (dt.datetime.now() +dt.timedelta(days=4)).strftime("%d/%m/%Y"))

    f = open(f"result/2023 2-4/2023-07-18/{row['name']}_{strategy}.txt", "w", encoding="utf-8")
    f.write(msg)
    f.close()