import streamlit as st
st.title("Welcome to")
st.markdown("""
            ## **Digital 101** **:rainbow[Revision]**
            """)
st.write(
    """
    This is the perfect place to revisit and strengthen your understanding 
    of everything you’ve learned so far in Digital 101.
    <p>
    You can view my dataset <a href="https://github.com/ByteJoseph/digital101/tree/master/dataset"><b>here</b></a>.
    </p>
  <!--  This app also includes an **Internet Time Machine** that lets you explore 
    blogs which were deleted by the author and are no longer accessible through the course.
    -->
    """,unsafe_allow_html=True
)

st.balloons()
if st.button("Revise Topics",icon=":material/menu_book:",type="primary"):
    st.switch_page("./pages/2_learn.py")
    pass
st.markdown("---")
#removed st.markdown("<p style='text-align: center;'>Made with 💛 by <a href='https://github.com/ByteJoseph'><b>Joseph</b></a></p>", unsafe_allow_html=True)
