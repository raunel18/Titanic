import streamlit as st
import pickle
 
# UI: User Interface, how things look like.
# UX: User Experinece, how does the user feel interacting with the app
 
# Set the title and display an image for branding
st.title ('Titanic Survival Prediction App!')
from PIL import Image
import io
 
img = Image.open("image.png")


img_bytes = io.BytesIO()
img.save(img_bytes, format="PNG")
st.image(img_bytes, caption="Predict Survival on the Titanic")
 
#st.image('image.png', caption = 'Predict Survival on the Titanic')
 
# Load the pretrained model
with open ('titanicpickle.pkl', 'rb') as pickleFile:
    model = pickle.load(pickleFile)
   
# Function to make prediction
def PredictionFunction(Pclass, Sex, Age, SibSp, Parch, Fare, Embarked):
    try:
        prediction = model.predict([[Pclass, Sex, Age, SibSp, Parch, Fare, Embarked]])
        return 'Survived' if prediction[0] == 1 else 'Did not Survive'
    except Exception as e:
        return f'Error:{str(e)}'
   
# Sidebar for Instructions
st.sidebar.header('How to Use!')
st.sidebar.markdown(""""
1.Enter the Passenger Details in the form
2. Click 'Predict' to see the Survival Result.
3.Adjust Values to Test Different Scenarios.
""")
st.sidebar.info('Example: A 30 years old male, 3rd class, 20$ fare, traveling alone from port southemptom.')

# Main input
def main():
    st.subheader('Enter Passenger Details:')
    col1, col2 = st.columns(2)
    #organise inputs in Colunms
    with col1:
        Pclass = st.selectbox('Passenger Class:', options=[1,2,3], format_func = lambda X:f'class{X}')
        sex = st.radio('Sex', options= ['male', 'female'])
        Age = st.slider('Age:', min_value=0, max_value=100, value = 30)
    with col2:
        SibSp = st.slider('Sibling/Spouses Aboard:', min_value=0, max_value =10, value=0)
        Parch = st.slider('Parents/Children Aboard:',min_value=0, max_value=10, value= 0)
        Fare = st.slider('Fare($):', min_value=0.0, max_value=500.0, value=50.0, step= 0.1)
        Embarked = st.radio('Port of Embarked:', options=['C', 'Q', 'S'], format_func= lambda X :f'port{X}')
        #convert Categorical inputs to numerical value
        Sex = 1 if sex == 'female'else 0
        Embarked ={'C':0, 'Q': 1, 'S': 2}[Embarked]

        
        # Button for prediction
    if st.button('Predict'):
              result = PredictionFunction(Pclass, Sex, Age, SibSp, Parch, Fare, Embarked)
    
              if result == 'Survived':
                 st.markdown("🎉 **Congratulations! The Passenger Survived.**")
              else:
                 st.markdown("😢 **Unfortunately, the Passenger Did Not Survive.**")

    # Run the main function
if __name__== '__main__':
  main()