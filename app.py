from shiny import App, ui, render

app_ui = ui.page_fluid(
    ui.card(
        ui.card_header("Client IP Information"),
        ui.output_text("forwarded_for"),
        ui.output_text("remote_addr"),
    )
)

def server(input, output, session):
    @render.text
    def forwarded_for():
        # Get the X-Forwarded-For header from the request
        x_forwarded_for = session.get_request_header("X-Forwarded-For", "Not available")
        return f"X-Forwarded-For: {x_forwarded_for}"
    
    @render.text
    def remote_addr():
        # Also display the remote address
        remote_addr = session.client_address or "Not available"
        return f"Remote Address: {remote_addr}"

app = App(app_ui, server)
