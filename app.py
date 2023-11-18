import cohere
import streamlit as st

co = cohere.Client(os.getenv('COHERE_API_KEY'))
cohere_model_id = 'command-nightly'

def generate_ans(qstn):

  response = co.generate(model=cohere_model_id,prompt=qstn)

  bot_answer = response.generations[0].text
  bot_answer = bot_answer.replace("\n\n--","").replace("\n--","").strip()

  return bot_answer


# The front end code starts here

st.title("Question & answer bot with Cohere")

form = st.form(key="user_settings")
with form:
  cohere_api_key = st.text_input('Cohere API Key:', type='password')
  cohere_model_id = st.text_input('Cohere Model Id:')

  if not cohere_api_key and not cohere_model_id:
    st.info("Please add your Cohere API key and Custom model key or use 'medium/xlarge' to continue.")
    update_api_keys = form.form_submit_button("Update keys")
    st.stop()

  co = cohere.Client(cohere_api_key)

  st.write("Enter your qstn [Example: Who is the PM of UK] ")

  qstn_input = st.text_input("Question", key = "qstn_input")
    
  generate_button = form.form_submit_button("Answer Question")

  if generate_button:
    if qstn_input == "":
      st.error("Question field cannot be blank")
    else:
      my_bar = st.progress(0.05)
      st.subheader("Answer from bot:")

      for i in range(1):
          st.markdown("""---""")
          ans = generate_ans(qstn_input)
          st.markdown("##### " + ans)
          st.write(ans)
          my_bar.progress((i+1)/1)


