import streamlit as st
import pandas as pd
from stqdm import stqdm
import plotly.express as px
import us as US_CONVERT

from inbxo import Questions as Q


app_text = {
    "title": "Inbxo ✨📬",
    "subtext": "Runs basic analysis on a list of emails. Only email domains are analyzed.",
    "footer": "Built with 💜 by [Travis Hoppe](https://github.com/thoppe/inbxo).",
}

st.set_page_config(layout="wide", page_title=app_text["title"])
st.title(app_text["title"])
st.markdown(f"_{app_text['subtext']}_")

with open("resources/default_emails.txt") as FIN:
    default_textbox = FIN.read()
text_input = st.text_area("Enter a list of emails:", value=default_textbox, height=200)

lines = [line.strip() for line in text_input.split("\n")]
lines = [line for line in lines if "@" in line]
lines = [line.split("@")[-1] for line in lines]
lines = [line for line in lines if line.strip()]
domains = pd.Series(lines).value_counts()

with st.status(f"Found {len(lines)} email addresses"):
    pass

with st.status(f"Computing {len(domains)} unique email domains"):
    data = []
    for domain in stqdm(domains.index, st_container=st.sidebar):
        result = Q["email"](domain)
        result["domain"] = domain
        data.append(result)

df = pd.DataFrame(data).set_index("domain")
df = pd.concat([domains, df], axis=1)
dx = df.dropna(subset=["is_academic"])
dx = dx[dx.is_academic]

with st.status(f"Computing {len(dx)} unique academic institutions"):
    data = []
    for domain in stqdm(dx.index, st_container=st.sidebar):
        result = Q["academic"](domain)
        result["domain"] = domain
        data.append(result)

dx = pd.DataFrame(data).set_index("domain")
del dx["expanded_name"]
df = pd.concat([df, dx], axis=1)

df = df.rename(columns={"country_of_origin_ISO_3166_alpha2": "country"})

cols = st.columns([1, 1, 1])

dx = df.dropna(subset=["is_university"])

fields = ["is_university", "is_R1", "is_minority_serving_institution"]
colors = [
    px.colors.sequential.RdBu,
    px.colors.sequential.turbid,
    px.colors.sequential.dense,
] * 3

for col, field, color in zip(cols, fields, colors):
    with col:
        fig = px.pie(
            dx,
            names=field,
            title=field,
            height=300,
            width=200,
            color_discrete_sequence=color,
        )
        fig.update_layout(
            margin=dict(l=20, r=20, t=30, b=0),
        )
        fig.update_traces(textinfo="label+value", hoverinfo="label+value+percent")
        st.plotly_chart(fig, use_container_width=True)


st.write("### Enhanced data")
df = df.set_index("domain_name")
# df.index.name = "doma"
st.write(df)

########################

data = df["State"].value_counts().sort_values(ascending=False)
data = data.reset_index()

########################


def state_name_to_abbr(state_name):
    state = US_CONVERT.states.lookup(state_name)
    return state.abbr if state else None


data = pd.DataFrame(data)
data["State2"] = data["State"].apply(state_name_to_abbr)

# Create choropleth map
fig = px.choropleth(
    data,
    locations="State2",  # State column
    locationmode="USA-states",  # To map to US states
    color="count",  # Column with the counts
    scope="usa",  # Focus on USA
    color_continuous_scale="Cividis",  # Color scale for counts
    labels={"count": "Count"},  # Label for color bar
    range_color=[0, data["count"].max()],
)

cols = st.columns([1, 1])
cols[0].write("### US State coverage")
cols[0].plotly_chart(fig, use_container_width=True)

########################

del data["State2"]
cols[1].write("### US State counts")
data = data.set_index("State")
cols[1].write(data)

########################
data = data.reset_index()
fig = px.bar(data, y="count", x="State")
st.plotly_chart(fig, use_container_width=False)

########################

f_schema = "inbxo/schema.py"
with open(f_schema) as FIN:
    code_block = FIN.read()
with st.expander("🔽 Expand to show GPT schema"):
    st.code(code_block)

########################

st.write(app_text["footer"])

########################


