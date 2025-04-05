import streamlit as st
st.title("Welcome to")
st.markdown("""
            ## **Digital 101** **:rainbow[Revision]**
            """)
st.write(
    """
    This is the perfect place to revisit and strengthen your understanding 
    of everything you’ve learned so far in Digital 101.

  <!--  This app also includes an **Internet Time Machine** that lets you explore 
    blogs which were deleted by the author and are no longer accessible through the course.
    -->
    """,unsafe_allow_html=True
)
st.markdown("[**View my dataset**](https://github.com/ByteJoseph/digital101/tree/master/dataset)")
if st.button("Revise Topics",icon=":material/menu_book:",):
    st.switch_page("./pages/2_learn.py")
    pass