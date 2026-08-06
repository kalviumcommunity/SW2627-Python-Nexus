import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(
    layout="wide"
)


st.title(
"Remote Work Blockers Analytics Dashboard"
)



df=pd.read_csv(
"data/remote_work_blockers.csv"
)



# -----------------------------
# KPI SECTION
# -----------------------------

st.header("Business Health Overview")


col1,col2,col3,col4,col5=st.columns(5)



with col1:
    st.metric(
        "Total Tickets",
        len(df)
    )


with col2:

    closed=len(
        df[df.Status=="Closed"]
    )

    st.metric(
        "Closed Tickets",
        closed
    )


with col3:

    st.metric(
        "Programs Impacted",
        df["Program Name"].nunique()
    )


with col4:

    avg_response=df[
        "First Response Time"
    ].notna().mean()*100


    st.metric(
        "Response SLA %",
        f"{avg_response:.1f}%"
    )


with col5:

    st.metric(
        "Blocker Types",
        df["Project Phase"].nunique()
    )



st.divider()



# -----------------------------
# TREND SECTION
# -----------------------------


st.header(
"Ticket Trends"
)



df["Created Time"]=pd.to_datetime(
df["Created Time"]
)


monthly=(
df.groupby(
df["Created Time"].dt.month
)
.size()
)



fig,ax=plt.subplots()

ax.plot(
monthly.index,
monthly.values,
marker="o"
)

ax.set_title(
"Monthly Ticket Creation Trend"
)

ax.set_xlabel(
"Month"
)

ax.set_ylabel(
"Tickets"
)


st.pyplot(fig)



# -----------------------------
# SEGMENT ANALYSIS
# -----------------------------


st.header(
"Blocker Distribution"
)


phase_count=(
df.groupby(
"Project Phase"
)
.size()
.sort_values()
)



fig,ax=plt.subplots()


phase_count.plot(
kind="barh",
ax=ax
)


ax.set_title(
"Tickets by Project Phase"
)


ax.set_xlabel(
"Tickets"
)


st.pyplot(fig)



# -----------------------------
# DETAIL SECTION
# -----------------------------


st.header(
"Ticket Explorer"
)


phase_filter=st.sidebar.selectbox(
"Select Phase",
["All"]+
list(df["Project Phase"].unique())
)


filtered=df


if phase_filter!="All":

    filtered=df[
        df["Project Phase"]
        ==
        phase_filter
    ]



st.write(
f"Showing {len(filtered)} tickets"
)


st.dataframe(
filtered
)



csv=filtered.to_csv(
index=False
)


st.download_button(
"Download CSV",
csv,
"filtered_tickets.csv"
)