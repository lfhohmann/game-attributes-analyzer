import plotly.graph_objects as go
from st_aggrid import AgGrid
import streamlit as st
import pandas as pd

PAGE_CONFIG = {
    "page_title": "Weapons",
    "page_icon": "🎮",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

DATASET = {
    "id": "14u0uzmMO29R3q_YSLMumbvkXzPRrW1IlpsJ0vNnEJxw",
    "name": "attibutes",
}

DATASET_URL = f"https://docs.google.com/spreadsheets/d/{DATASET['id']}/gviz/tq?tqx=out:csv&sheet={DATASET['name']}"

GRAPH = {
    "font": {"size": 30, "color": "white"},
    "gridcolor": "rgba(64,64,64,255)",
    "plot_bgcolor": "rgba(32,32,32,255)",
    "margin": {"l": 20, "r": 0, "t": 50, "b": 20},
    "height": 500,
    "width": 1000,
}


def load_data(url: str) -> pd.DataFrame:
    df = pd.read_csv(url, index_col=0)

    for col in ["Category", "Hold to Shoot", "Tracers", "Recoil Pattern"]:
        df[col] = df[col].astype("category")

    return df


def comparator(df):
    attributes = st.multiselect(
        "Attributes",
        df.columns[2:],
        [
            "Bullets",
            "Damage",
            "Headshot Multiplier",
            "Fire Rate",
            "Armor Penetration",
            "Tagging Power",
            "Mobility",
            "Bullet Range",
            "Reserve Ammo",
            "Magazine Size",
            "Damage Falloff @ 500U",
        ],
        key="comparator_attributes",
    )
    weapons = st.multiselect(
        "Weapons",
        df["Name"],
        ["G3SG1", "SCAR-20", "AWP", "Galil AR"],
        key="comparator_items",
    )

    df = df.loc[df["Name"].isin(weapons)][["Name"] + attributes]

    for col in df.columns:
        if df[col].dtype in ["category"]:
            df = df.drop(col, axis="columns")

        elif df[col].dtype in ["int64", "float64"]:
            delta = df[col].max() / 100

            if delta > 0:
                df[col] = df[col] / delta

            else:
                df[col] = 100

    # print(df)

    fig = go.Figure()

    for weapon in weapons:
        data = df.loc[df["Name"] == weapon]
        data = data.drop(["Name"], axis="columns").values
        # print(data[0])

        fig.add_trace(
            go.Scatterpolar(
                r=data[0],
                theta=attributes,
                fill="toself",
                name=weapon,
            )
        )

    fig.update_layout(
        height=GRAPH["height"],
        width=GRAPH["width"],
        margin=GRAPH["margin"],
    )

    st.plotly_chart(fig)


def correlate(df):
    attributes = st.multiselect(
        "Attributes",
        df.columns[2:],
        [
            "Bullets",
            "Damage",
            "Headshot Multiplier",
            "Fire Rate",
            "Armor Penetration",
            "Tagging Power",
            "Mobility",
            "Bullet Range",
            "Reserve Ammo",
            "Magazine Size",
            "Damage Falloff @ 500U",
        ],
        key="correlate_attributes",
    )

    # df = df.loc[df["Name"].isin(weapons)][["Name"] + attributes]

    df = df[attributes].corr()

    fig = go.Figure()

    fig.add_trace(
        go.Heatmap(
            z=df.to_numpy(),
            x=df.columns,
            y=df.columns,
            hoverongaps=False,
        )
    )

    fig.update_layout(
        height=GRAPH["height"] + 250,
        width=GRAPH["width"],
        margin=GRAPH["margin"],
    )

    st.plotly_chart(fig)


def main():
    st.set_page_config(**PAGE_CONFIG)

    df = load_data(DATASET_URL)

    st.title(f"Table")
    df = AgGrid(df, editable=True, theme="dark")["data"]

    st.markdown(
        f"[Google Sheet Source](https://docs.google.com/spreadsheets/d/{DATASET['id']})"
    )

    st.title(f"Compare")
    comparator(df)

    st.title("Correlations")
    correlate(df)

    st.sidebar.title("READ ME")
    st.sidebar.markdown(
        "This is a simple tool to import data from a Google spreasheed and analyze the attributes of different weapons."
    )

    st.sidebar.title("Export Data")
    st.sidebar.download_button(
        "Download CSV", df.to_csv(index=False), file_name="weapons_attributes.csv"
    )
    st.sidebar.download_button(
        "Download HTML", df.to_html(index=False), file_name="weapons_attributes.html"
    )

    st.sidebar.title("Author")
    st.sidebar.markdown("[Lucas Hohmann](https://github.com/lfhohmann)")


if __name__ == "__main__":
    main()
