from .Databased import Base
import streamlit as st
from keybert import KeyBERT


@st.cache(allow_output_mutation=True)
def load_model():
    return KeyBERT("distilbert-base-nli-mean-tokens")


@st.cache
def load_projects(table, date_present):
    data = Base().all_project(table=table,
                              date_present=date_present)
    return data


@st.cache
def load_yandex_related(table, date_present, project):
    data = Base().read_all(table=table,
                           date_present=date_present,
                           project=project)
    return data


@st.cache
def load_yandex_all(table, date_present, date_past, project):
    data = Base().read_all(table=table,
                           date_present=date_present,
                           date_past=date_past,
                           project=project)
    return data


@st.cache
def load_yandex_all_rating(table, project, coordinates):
    data = Base().all_rating(table=table, project=project, coordinates=coordinates)
    return data


@st.cache
def load_yandex_aspect(table, date_present, date_past, project, coordinates):
    data = Base().read_all(table=table,
                           date_present=date_present,
                           date_past=date_past,
                           project=project,
                           coordinates=coordinates)
    return data


@st.cache
def load_aspect_count(table, project, coordinates):
    data = Base().read_count_reviews(table=table,
                                     project=project, coordinates=coordinates)
    return data


@st.cache
def load_yandex_related_rating(table, project, coordinates, date_present):
    data = Base().rating_related(table=table,
                                 project=project, coordinates=coordinates, date_present=date_present)
    return data


@st.cache
def load_yandex_count_votes_reviews(table, project, coordinates):
    data = Base().count_all_votes_reviews(table=table,
                                          project=project, coordinates=coordinates)
    return data


@st.cache
def load_reviews(table, project, coordinates):
    data = Base().reviews_all(table=table,
                              project=project, coordinates=coordinates)
    return data


@st.cache
def load_reviews_wordcloud(project, coordinates):
    data = Base().reviews(table=f'{st.session_state.option}_reviews',
                          project=project,
                          coordinates=coordinates)
    return data


def load_maps(date_present):
    data = Base().maps(date_present=date_present)
    return data
