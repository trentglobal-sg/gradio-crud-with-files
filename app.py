import gradio as gr
initial_contacts = contacts = [
    {"id": "1", "name": "John Smith", "phone": "555-1234", "email": "john@example.com", "address": "123 Main St"},
    {"id": "2", "name": "Jane Doe", "phone": "555-5678", "email": "jane@example.com", "address": "456 Oak Ave"},
    {"id": "3", "name": "Alex Johnson", "phone": "555-9012", "email": "alex@example.com", "address": "789 Pine Rd"},
    {"id": "4", "name": "Sarah Williams", "phone": "555-3456", "email": "sarah@example.com", "address": "101 Maple Dr"},
    {"id": "5", "name": "Jane Doe", "phone": "555-0000", "email": "jane2@example.com", "address": "999 Elm St"},
]

def get_list_for_display(contacts):
  name_table = [[contact["name"]] for contact in contacts]
  return name_table

def show_contact(dataframe, app_state, event: gr.SelectData):
    if not event.selected:
        return "", "", "", "", -1
    row_index = event.index[0]
    contact = app_state.get('contacts')[row_index]
    app_state['selected_index'] = row_index
    return contact.get("name", ""), contact.get("phone", ""), contact.get("email", ""), contact.get("address", ""), app_state  

def modify_contact(name, phone, email, address, app_state):
    selected_index = app_state.get('selected_index')
    print(f"[MODIFY] Index: {selected_index}")
    idx = selected_index
    if idx == -1:
        return name, phone, email, address, idx, get_list_for_display()
    modified_contact = {
        "id": idx,
        "name": name,
        "phone": phone,
        "email": email,
        "address": address
    }
    app_state.get('contacts')[idx] = modified_contact    
    return app_state


def save_new_contact(name, phone, email, address, app_state):
    new_id = str(max([int(c["id"]) for c in contacts] + [0]) + 1)
    new_contact = {
        "id": new_id,
        "name": name,
        "phone": phone,
        "email": email,
        "address": address
    }
    app_state.get('contacts').append(new_contact)    
    return '', '', '', '', gr.update(visible=False), app_state

def delete_contact(app_state):
    idx = app_state.get("selected_index")
    if idx == -1:
        return app_state
    app_state['contacts'].pop(idx)
    app_state['selected_index'] = -1
    
    # After deletion, clear fields and reset selection
    return app_state



with gr.Blocks() as app:
    app_state = gr.State({
      "selected_index": -1,
      "contacts": contacts
    })  

    gr.Markdown("# Contact Manager")
    add_contact_btn = gr.Button("Add New Contact")

    with gr.Group(visible=False) as add_contact_dialog:
        gr.Markdown("### Add New Contact")
        with gr.Column():
            new_name = gr.Textbox(label="Name")
            new_phone = gr.Textbox(label="Phone")
            new_email = gr.Textbox(label="Email")
            new_address = gr.Textbox(label="Address")
            with gr.Row():
                save_btn = gr.Button("Save")
                cancel_btn = gr.Button("Cancel")

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("## Contacts")
            df_table = gr.Dataframe(
                value=get_list_for_display(app_state.value.get('contacts')),
                headers=["Name"],
                datatype=["str"],
                interactive=False,
                label="Select a contact"
            )

        with gr.Column():
            gr.Markdown("## Details")
            contact_name = gr.Textbox(label="Name")
            phone = gr.Textbox(label="Phone")
            email = gr.Textbox(label="Email")
            address = gr.Textbox(label="Address")
            modify_btn = gr.Button("MODIFY")
            delete_btn = gr.Button("DELETE")

            modify_btn.click(
                fn=modify_contact,
                inputs=[contact_name, phone, email, address, app_state],
                outputs=[app_state]
            )

            delete_btn.click(
                fn=delete_contact,
                inputs=[app_state],
                outputs=[app_state]
            )


    def show_add_contact_dialog():
        return gr.update(visible=True)

    def hide_add_contact_dialog():
        return gr.update(visible=False)

    def get_selected_contact_display(app_state):
        selected_index = app_state.get("selected_index")
        if selected_index == -1:
            return "", "", "", ""
        else:
            contact = app_state.get('contacts')[selected_index]
            return contact.get("name", ""), contact.get("phone", ""), contact.get("email", ""), contact.get("address", "")

    app_state.change(
        fn=lambda x: get_list_for_display(x.get('contacts')),
        inputs=[app_state],
        outputs=[df_table]
    )    

    app_state.change(
        fn=get_selected_contact_display,
        inputs=[app_state],
        outputs=[contact_name, phone, email, address]
    )

    add_contact_btn.click(
        fn=show_add_contact_dialog,
        inputs=[],
        outputs=[add_contact_dialog]
    )

    cancel_btn.click(
        fn=hide_add_contact_dialog,
        inputs=[],
        outputs=[add_contact_dialog]
    )

    save_btn.click(
        fn=save_new_contact,
        inputs=[new_name, new_phone, new_email, new_address, app_state],
        outputs=[new_name, new_phone, new_email, new_address, add_contact_dialog, app_state]
    )

    df_table.select(
        fn=show_contact,
        inputs=[df_table, app_state],
        outputs=[contact_name, phone, email, address, app_state]  
    )

app.launch(debug=True)