import streamlit as st
import pandas as pd
from stqdm import stqdm
import plotly.express as px

from inbxo import Questions as Q

# import src.viz_interface as interface
# from bokeh.models import Label

app_text = {
    "title": "Inbxo",
    "footer": "Built by [Travis Hoppe](https://github.com/thoppe/inbxo)",
}

default_textbox = """student@cuny.edu\nprovost@unr.edu"""

st.set_page_config(layout="wide")
st.title(app_text["title"])
text_input = st.text_area("Enter a list of emails:", value=default_textbox, height=300)
# st.button("COMPUTE!")

lines = [line.strip() for line in text_input.split("\n")]
lines = [line.split("@")[-1] for line in lines]
lines = [line for line in lines if line.strip()]
domains = pd.Series(lines).value_counts()
domains = domains[:50]

with st.status(f"Computing {len(domains)} email domains"):
    data = []
    for domain in stqdm(domains.index, st_container=st.sidebar):
        result = Q["email"](domain)
        result["domain"] = domain
        data.append(result)

df = pd.DataFrame(data).set_index("domain")
st.write(df.index)
st.write(domains)


df = pd.concat([domains, df], axis=1)
dx = df.dropna(subset=["is_academic"])
dx = dx[dx.is_academic]
with st.status(f"Computing {len(dx)} academic institutions"):
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
]

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
        st.plotly_chart(fig, use_container_width=True)


st.write(df)
data = df["State"].value_counts().sort_values(ascending=False)
data = data.reset_index()
st.write(data)

fig = px.bar(data, y="count", x="State")
st.plotly_chart(fig, use_container_width=False)

st.write(app_text["footer"])
