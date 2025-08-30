import gradio as gr

initial_contacts = [
  {"id": "1", "name": "John Smith", "phone": "555-1234", "email": "john@example.com", "address": "123 Main St"},
  {"id": "2", "name": "Jane Doe", "phone": "555-5678", "email": "jane@example.com", "address": "456 Oak Ave"},
  {"id": "3", "name": "Alex Johnson", "phone": "555-9012", "email": "alex@example.com", "address": "789 Pine Rd"},
  {"id": "4", "name": "Sarah Williams", "phone": "555-3456", "email": "sarah@example.com", "address": "101 Maple Dr"},
  {"id": "5", "name": "Jane Doe", "phone": "555-0000", "email": "jane2@example.com", "address": "999 Elm St"},
]

def get_list_for_display(contacts):
  name_table = [[contact["name"]] for contact in contacts]
  return name_table

# see note 3
def show_contact(dataframe, app_state, event: gr.SelectData):
    if not event.selected:
        return -1
    row_index = event.index[0]    
    app_state['selected_index'] = row_index
    return app_state  

# see note 6    
def get_selected_contact_display(app_state):
    selected_index = app_state.get("selected_index")
    if selected_index == -1:
        return "", "", "", ""
    else:
        contact = app_state.get('contacts')[selected_index]
        return contact.get("name", ""), contact.get("phone", ""), contact.get("email", ""), contact.get("address", "")

with gr.Blocks() as app:
  gr.Markdown("# Contact Manager")
  
  #see note 1
  app_state = gr.State({     
      "contacts": initial_contacts,
      "selected_index": -1
  })

  with gr.Row():
    with gr.Column(scale=1):
      gr.Markdown("## Contacts")
      df_table = gr.Dataframe(
        value=get_list_for_display(initial_contacts),
        headers=["Name"],
        datatype=["str"],
        interactive=False,
        label="Select a contact"
      )
    with gr.Column():
      gr.Markdown("## Details")
      
      # see note 4
      contact_name = gr.Textbox(label="Name")
      phone = gr.Textbox(label="Phone")
      email = gr.Textbox(label="Email")
      address = gr.Textbox(label="Address")


  # see note 2
  df_table.select(show_contact, inputs=[df_table, app_state], outputs=[app_state])

  # see note 5
  app_state.change(
    fn=get_selected_contact_display,
    inputs=[app_state],
    outputs=[contact_name, phone, email, address]
  )

app.launch(debug=True)

