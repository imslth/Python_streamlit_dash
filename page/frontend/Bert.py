import pandas
import streamlit as st
import seaborn as sns


def main(content):
    df = (
        pandas.DataFrame(content, columns=["Ключевые слова", "Актуальность"])
        .sort_values(by="Актуальность", ascending=False)
        .reset_index(drop=True)
    )
    df.index += 1

    cmGreen = sns.light_palette("green", as_cmap=True)
    cmRed = sns.light_palette("red", as_cmap=True)
    df = df.style.background_gradient(
        cmap=cmGreen,
        subset=[
            "Актуальность",
        ],
    )
    format_dictionary = {
        "Актуальность": "{:.1%}",
    }
    df = df.format(format_dictionary)
    st.table(df)


if __name__ == '__main__':
    main()
