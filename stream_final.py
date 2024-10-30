import streamlit as st
import pandas as pd
import time
import pickle
from utils import utils
import plotly.express as px
from main import ALL_MODEL_PREDICTION,ALL_MODEL_PREDICTION_METABOLISUM

##-----------------------leading the models---------------------------

@st.cache_resource
def LOAD_TOX_MODELS():
    dict={  'Hepatotoxicity': pickle.load(open('models/Hepatotoxicity.pkl', 'rb')),
            'Mutagenicity': pickle.load(open('models/Mutagenicity.pkl', 'rb')),
            'Cardiotoxicity': pickle.load(open('models/Cardiotoxicity.pkl', 'rb')),
            'Carcinogenicity': pickle.load(open('models/Carcinogenicity.pkl', 'rb')),
            'Nephrotoxicity': pickle.load(open('models/Nephrotoxicity.pkl', 'rb')),

            'CYP3A4_Inhibitor': pickle.load(open('models/CYP3A4_Inhibitor.pkl', 'rb')),
            'CYP2D6_Inhibitor': pickle.load(open('models/CYP2D6_Inhibitor.pkl', 'rb')),
            'CYP2C9_Inhibitor': pickle.load(open('models/CYP2C9_Inhibitor.pkl', 'rb'))
    }

    return dict

 # ----load-models----
model_dict = LOAD_TOX_MODELS()

#----------------------------------------------------------------------------#

###navigation pages
nav = st.sidebar.radio("Navigation",["Home","Toxicity","Metabolism","Combine"])

#----------------------------------------------------------------------------#
###navigation page insite the home
if nav == "Home":
    st.title("Toxicity and Metabolism Prediction") 
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
        #------------------------------------------------------triel------------------
        #new_dict = utils.LOAD_MODEL('models', toxicity_name)
        models = {key: model_dict[key] for key in toxicity_name if key in model_dict}
        df = ALL_MODEL_PREDICTION(smi_list, models)
        #df = ALL_MODEL_PREDICTION(smi_list, new_dict)
        #--------------------------------------------------------------------
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

            # # who v/s fare barplot 
            # fig = px.bar(unpivoted_df, x="Toxicity", y="values", color="Class", barmode='group', title="Toxicity Prediction", text="values")
            # fig.update_layout(autosize=True, width=900, height=500, title_x=0.4) 
            # # Display the grouped bar plot in Streamlit
            # st.plotly_chart(fig, use_container_width=True)

            # Define the color map for toxicity prediction
            color_map_toxicity = {
                'Non-Toxic': '#28A745',        # Green for non-toxic compounds
                'Toxic': '#FF0000',            # Bright red for toxic compounds
                'Not_calculate': '#C0C0C0'      # Light gray for not assessed cases
            }

            # Create the bar plot with custom colors for toxicity
            fig = px.bar(
                unpivoted_df, 
                x="Toxicity",            # Use "toxicity" for x-axis, ensuring it reflects the correct column
                y="values", 
                color="Class", 
                barmode='group', 
                title="Toxicity Prediction", 
                text="values",
                color_discrete_map=color_map_toxicity  # Custom color mapping for toxicity
            )

            # Update layout and display plot
            fig.update_layout(autosize=True, width=900, height=500, title_x=0.4,xaxis_title="Toxicity prediction",yaxis_title="Values",legend_title="Class" )
            # Display the grouped bar plot in Streamlit
            st.plotly_chart(fig, use_container_width=True)

### ============================================== metabolisum ===================================================== ##

if nav == "Metabolism":

    st.title("Metabolism Prediction") 
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
        #---------------------------------------------------------
        #new_dict = utils.LOAD_MODEL('models', metabolism_name)
        models = {key: model_dict[key] for key in metabolism_name if key in model_dict}
        df = ALL_MODEL_PREDICTION_METABOLISUM(smi_list, models)
        #---------------------------------------------------------
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
            
            # ----------code for plot --------
            # # who v/s fare barplot 
            # fig = px.bar(unpivoted_df, x="metabolism", y="values", color="Class", barmode='group', title="Metabolism Prediction", text="values")
            # fig.update_layout(autosize=True, width=900, height=500, title_x=0.4) 
            # # Display the grouped bar plot in Streamlit
            # st.plotly_chart(fig, use_container_width=True)

            color_map = {
                'Non-Inhibitor':  '#28A745',   # Green for non-toxic
                'Inhibitor': '#FF0000',        # Bright red for toxic
                'Not_calculate': '#C0C0C0'    # Light gray for not calculated
            }

            # Create the bar plot with custom colors
            fig = px.bar(
                unpivoted_df, 
                x="metabolism", 
                y="values", 
                color="Class", 
                barmode='group', 
                title="Metabolism Prediction", 
                text="values",
                color_discrete_map=color_map  # Custom color mapping
            )

            # Update layout and display plot
            fig.update_layout(autosize=True, width=900, height=500, title_x=0.4)
            st.plotly_chart(fig, use_container_width=True)


### ============================================== combine_both ===================================================== ##


if nav == "Combine":

    st.title("METTOX Prediction") 
    ## Insert SMILES in text area
    text = st.text_area('Please Provide molecular SMILES')
    ### Convert SMILES into list
    smi_list = list(str(num) for num in text.strip().split())
    ### Create the checkbox of each hepatotoxicity
    st.sidebar.subheader('METTOX:')
    hepatotoxicity = st.sidebar.checkbox('Hepatotoxicity')
    mutagenicity = st.sidebar.checkbox('Mutagenicity')
    cardiotoxicity = st.sidebar.checkbox('Cardiotoxicity')
    carcinogenicity = st.sidebar.checkbox('Carcinogenicity')
    nephrotoxicity = st.sidebar.checkbox('Nephrotoxicity')
    CYP3A4_Inhibitor = st.sidebar.checkbox('CYP3A4_Inhibitor')
    CYP2D6_Inhibitor = st.sidebar.checkbox('CYP2D6_Inhibitor')
    CYP2C9_Inhibitor = st.sidebar.checkbox('CYP2C9_Inhibitor')
    # neurotoxicity = st.sidebar.checkbox('Neurotoxicity')
    
    ### Store the toxicity values inside the list
    TOX_name = []
    MET_name = []
    if hepatotoxicity:
        TOX_name.append('Hepatotoxicity')
    if mutagenicity:
        TOX_name.append('Mutagenicity')
    if carcinogenicity:
        TOX_name.append('Carcinogenicity')
    if cardiotoxicity:
        TOX_name.append('Cardiotoxicity')
    if nephrotoxicity:
        TOX_name.append('Nephrotoxicity')
    if CYP3A4_Inhibitor:
        MET_name.append('CYP3A4_Inhibitor')
    if CYP2D6_Inhibitor:
        MET_name.append('CYP2D6_Inhibitor')
    if CYP2C9_Inhibitor:
        MET_name.append('CYP2C9_Inhibitor')

    ## Button for prediction
    if st.button('Predict'):
        start_time = time.time()  # Start the timer
        #------------------------------------------------------triel-----------------
        TOX_models = {key: model_dict[key] for key in TOX_name if key in model_dict}
        MET_models = {key: model_dict[key] for key in MET_name if key in model_dict}

        MET_df = ALL_MODEL_PREDICTION_METABOLISUM(smi_list, MET_models)
        TOX_df = ALL_MODEL_PREDICTION(smi_list, TOX_models)

        # Drop 'SMILES' column from MET_df if it exists
        if 'SMILES' in MET_df.columns:
            MET_df.drop(columns='SMILES', inplace=True)

        # Combine both DataFrames with error handling
        if not TOX_df.empty and not MET_df.empty:
            # Both DataFrames have data
            df = pd.concat([TOX_df, MET_df], axis=1)
        elif not TOX_df.empty:
            # Only Toxicity DataFrame has data
            df = TOX_df
            st.warning("Metabolism predictions are not available.")
        elif not MET_df.empty:
            # Only Metabolism DataFrame has data
            df = MET_df
            st.warning("Toxicity predictions are not available.")
        else:
            # Both DataFrames are empty
            df = pd.DataFrame()
            st.error("No predictions were made for either Toxicity or Metabolism.")

        #--------------------------------------------------------------------
        end_time = time.time()  # End the timer
        elapsed_time = end_time - start_time  # Calculate elapsed time

        ## Progress bar
        bar = st.progress(50)
        time.sleep(3)
        bar.progress(100)

        print(TOX_name)

        if len(TOX_name) == 0 and len(MET_name) == 0:
            st.error('Please select at least one toxicity or metabolism')
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
            st.markdown(""" **Below Table shows the summarized report of METTOX:**""")
            ## Summarization of 
            summary = utils.SUMMARY_TABLE_METTOX(df)
            st.table(summary) 

            st.markdown(""" """) 
            st.markdown(""" ###### The graphical representation of model is:""")  
            # Read a titanic.csv file from seaborn library
            unpivoted_df = summary.melt(id_vars='Class', var_name='Toxicity', value_name='values')

            # # who v/s fare barplot 
            # fig = px.bar(unpivoted_df, x="Toxicity", y="values", color="Class", barmode='group', title="Toxicity Prediction", text="values")
            # fig.update_layout(autosize=True, width=900, height=500, title_x=0.4) 
            # # Display the grouped bar plot in Streamlit
            # st.plotly_chart(fig, use_container_width=True)

            # Define the color map for toxicity prediction
            color_map_toxicity = {
                'Non-Toxic': '#28A745',        # Green for non-toxic compounds
                'Toxic': '#FF0000',            # Bright red for toxic compounds
                'Not_calculate': '#C0C0C0'      # Light gray for not assessed cases
            }

            # Create the bar plot with custom colors for toxicity
            fig = px.bar(
                unpivoted_df, 
                x="Toxicity",            # Use "toxicity" for x-axis, ensuring it reflects the correct column
                y="values", 
                color="Class", 
                barmode='group', 
                title="METTOX Prediction", 
                text="values",
                color_discrete_map=color_map_toxicity  # Custom color mapping for toxicity
            )

            # Update layout and display plot
            fig.update_layout(autosize=True, width=900, height=500, title_x=0.4,xaxis_title="METTOX prediction",yaxis_title="Values",legend_title="Class" )
            # Display the grouped bar plot in Streamlit
            st.plotly_chart(fig, use_container_width=True)


   