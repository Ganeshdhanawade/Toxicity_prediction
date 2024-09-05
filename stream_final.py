import streamlit as st
import time
from utils import utils
import plotly.express as px
from main import ALL_MODEL_PREDICTION,ALL_MODEL_PREDICTION_METABOLISUM
#----------------------------------------------------------------------------#

###navigation pages
nav = st.sidebar.radio("Navigation",["Home","Toxicity","Metabolism"])

#----------------------------------------------------------------------------#
###navigation page insite the home
if nav == "Home":
    st.title("Toxicity and Metabolisum Prediction") 
    ##insert image
    st.image("images/toxicity.jpg",width=500)
    ##subheader
    st.subheader("Predicting Drug Toxicity with AI")
    ##write containt insite the text
    st.markdown("""
The medical field constantly strives to develop potent life-saving drugs, but a hidden enemy lurks within their potential—toxicity. The six horsemen of drug-induced toxicity, namely hepatotoxicity (liver damage), cardiotoxicity (heart damage), carcinogenicity (cancer-causing), mutagenicity (genetic mutation), neurotoxicity (nervous system damage), and nephrotoxicity (kidney damage), can cast a long shadow over even the most promising medications.

Traditionally, identifying and assessing these toxicities has been a laborious and expensive process, relying heavily on animal testing and clinical trials. But in recent years, a powerful knight has emerged to challenge this entrenched system: Machine learning and deep learning.

**From Pixels to Predictions:**

Imagine feeding a deep learning model mountains of data, including chemical structures, molecular properties, and known toxicity profiles of countless drugs. This digital alchemist then weaves intricate connections within its artificial neurons, discerning subtle patterns and hidden relationships between molecular features and toxic effects. As the model trains, it becomes adept at predicting the potential of unseen drugs to inflict each of the six horsemen's wrath.

**Benefits of the Machine Learning Shield:**

* Faster and Cheaper: Predicting toxicity with machine learning eliminates the need for lengthy animal testing and clinical trials, significantly reducing the time and cost of drug development.
* More Accurate: By analyzing vast datasets, machine learning models can identify subtle toxicity patterns invisible to traditional methods, potentially leading to safer and more effective drugs.
* Personalized Medicine: Machine learning can personalize drug prescriptions by predicting individual patient responses and tailoring treatment regimens to minimize toxicity risks.

""")
    
### ============================================= Toxicity ============================================= ###
    
if nav == "Toxicity":

    st.title("Toxicity Prediction") 
    ## Insert SMILES in text area
    text = st.text_area('Please Provide molecular SMILES')
    ### Convert SMILES into list
    smi_list = list(str(num) for num in text.strip().split())
    ### Create the checkbox of each hepatotoxicity
    st.sidebar.subheader('Toxicity:')
    hepatotoxicity = st.sidebar.checkbox('Hepatotoxicity')
    mutagenicity = st.sidebar.checkbox('Mutagenicity')
    cardiotoxicity = st.sidebar.checkbox('Cardiotoxicity')
    carcinogenicity = st.sidebar.checkbox('Carcinogenicity')
    nephrotoxicity = st.sidebar.checkbox('Nephrotoxicity')
    # neurotoxicity = st.sidebar.checkbox('Neurotoxicity')
    
    ### Store the toxicity values inside the list
    toxicity_name = []
    if hepatotoxicity:
        toxicity_name.append('Hepatotoxicity')
    if mutagenicity:
        toxicity_name.append('Mutagenicity')
    if carcinogenicity:
        toxicity_name.append('Carcinogenicity')
    if cardiotoxicity:
        toxicity_name.append('Cardiotoxicity')
    # if neurotoxicity:
    #     toxicity_name.append('Neurotoxicity')
    if nephrotoxicity:
        toxicity_name.append('Nephrotoxicity')

    ## Button for prediction
    if st.button('Predict'):
        start_time = time.time()  # Start the timer
        new_dict = utils.LOAD_MODEL('models', toxicity_name)
        df = ALL_MODEL_PREDICTION(smi_list, new_dict)
        end_time = time.time()  # End the timer
        elapsed_time = end_time - start_time  # Calculate elapsed time

        ## Progress bar
        bar = st.progress(50)
        time.sleep(3)
        bar.progress(100)

        if len(toxicity_name) == 0:
            st.error('Please select at least one toxicity')
        else:
            ## Display elapsed time
            st.markdown(f"**Model prediction time:** {elapsed_time:.2f} seconds")

            ## Show df in tables
            st.table(df.head(10))
            
            ## Set download option
            col1, col2, col3 = st.columns([2, 1, 1])
            with col3:
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download",
                    data=csv,
                    file_name='data.csv',
                    mime='text/csv',
                )
                
            ## Insert the space of model    
            st.markdown(""" """)
            st.markdown(""" **Below Table shows the summarized report of Toxicity:**""")
            ## Summarization of 
            summary = utils.SUMMARY_TABLE(df)
            st.table(summary) 

            st.markdown(""" """) 
            st.markdown(""" ###### The graphical representation of model is:""")  
            # Read a titanic.csv file from seaborn library
            unpivoted_df = summary.melt(id_vars='Class', var_name='Toxicity', value_name='values')

            # who v/s fare barplot 
            fig = px.bar(unpivoted_df, x="Toxicity", y="values", color="Class", barmode='group', title="Toxicity Prediction", text="values")
            fig.update_layout(autosize=True, width=900, height=500, title_x=0.4) 
            # Display the grouped bar plot in Streamlit
            st.plotly_chart(fig, use_container_width=True)

### ============================================== metabolisum ===================================================== ##

if nav == "Metabolism":

    st.title("Metabolisum Prediction") 
    ## Insert SMILES in text area
    text = st.text_area('Please Provide molecular SMILES')
    ### Convert SMILES into list
    smi_list = list(str(num) for num in text.strip().split())
    ### Create the checkbox of each hepatotoxicity
    st.sidebar.subheader('Metabolism:')
    CYP3A4_Inhibitor = st.sidebar.checkbox('CYP3A4_Inhibitor')
    CYP2D6_Inhibitor = st.sidebar.checkbox('CYP2D6_Inhibitor')
    CYP2C9_Inhibitor = st.sidebar.checkbox('CYP2C9_Inhibitor')
 
    
    ### Store the toxicity values inside the list
    metabolism_name = []
    if CYP3A4_Inhibitor:
        metabolism_name.append('CYP3A4_Inhibitor')
    if CYP2D6_Inhibitor:
        metabolism_name.append('CYP2D6_Inhibitor')
    if CYP2C9_Inhibitor:
        metabolism_name.append('CYP2C9_Inhibitor')
   

    ## Button for prediction
    if st.button('Predict'):
        start_time = time.time()  # Start the timer
        new_dict = utils.LOAD_MODEL('models', metabolism_name)
        df = ALL_MODEL_PREDICTION_METABOLISUM(smi_list, new_dict)
        end_time = time.time()  # End the timer
        elapsed_time = end_time - start_time  # Calculate elapsed time

        ## Progress bar
        bar = st.progress(50)
        time.sleep(3)
        bar.progress(100)

        if len(metabolism_name) == 0:
            st.error('Please select at least one type of metabolism')
        else:
            ## Display elapsed time
            st.markdown(f"**Model prediction time:** {elapsed_time:.2f} seconds")

            ## Show df in tables
            st.table(df.head(10))
            
            ## Set download option
            col1, col2, col3 = st.columns([2, 1, 1])
            with col3:
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download",
                    data=csv,
                    file_name='data.csv',
                    mime='text/csv',
                )
                
            ## Insert the space of model    
            st.markdown(""" """)
            st.markdown(""" **Below Table shows the summarized report of metabolism:**""")
            ## Summarization of 
            summary = utils.SUMMARY_TABLE_METABOLISM(df)
            st.table(summary) 

            st.markdown(""" """) 
            st.markdown(""" ###### The graphical representation of model is:""")  
            # Read a titanic.csv file from seaborn library
            unpivoted_df = summary.melt(id_vars='Class', var_name='metabolism', value_name='values')

            # who v/s fare barplot 
            fig = px.bar(unpivoted_df, x="metabolism", y="values", color="Class", barmode='group', title="Metabolism Prediction", text="values")
            fig.update_layout(autosize=True, width=900, height=500, title_x=0.4) 
            # Display the grouped bar plot in Streamlit
            st.plotly_chart(fig, use_container_width=True)


   