import streamlit as st
from sqlexpress.parsers import QueryParser


### Data

if 'queries' not in st.session_state:
    st.session_state['queries'] = {}


## Callbacks

def add_query() -> None:
    st.session_state['queries'][st.session_state['add_table']] = \
        st.session_state['add_query']
    
def delete_query(table_name: str) -> None:
    del st.session_state['queries'][table_name]
    
def update_query(old_name: str, new_name: str, new_query: str) -> None:
    delete_query(old_name)
    st.session_state['queries'][new_name] = new_query
    

### Layout

st.set_page_config(layout='wide')
st.title('SQL Express')

col1, col2, col3 = st.columns([1,1,1])

with col1:
    st.subheader('1. Upload New Query')
    with st.form(key='upload', clear_on_submit=True):
        st.text_input(label='Table Name', key='add_table')
        st.text_area(label='Query', key='add_query', height=300)
        st.form_submit_button('Add', on_click=add_query)
        
with col2:
    st.subheader('2. Review Uploaded Queries')    
    for i, (name, query) in enumerate(st.session_state['queries'].items()):
        with st.expander(label=name.replace('`', '')):
            new_name = st.text_input(label='Table Name', key=4*i, value=name)
            new_query = st.text_area('Query', key=4*i+1, value=query, height=300)
            st.button('Delete', key=4*i+2, on_click=delete_query, args=(name, ))
            st.button('Update', key=4*i+3, on_click=update_query, args=(name, new_name, new_query))

with col3:
    st.subheader('3. Visualize Relationships')    
    generate = st.button('Generate Output')    
    if generate:        
        digraph = 'digraph {\n'
        digraph += '    rankdir=LR;\n'
        digraph += '    node [ shape=box ];\n'
        for target, query in st.session_state['queries'].items():
            parser = QueryParser(raw=query, target=target)
            source_tables = parser.extract_sources()
            for table in source_tables:
                digraph += f'   "{table}" -> "{target}"\n'                
        digraph += '}\n'
        print(digraph)
        st.graphviz_chart(digraph)
        